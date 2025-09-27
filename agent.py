import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()  # this reads .env into os.environ

#AI Things
from typing import Any
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
import asyncio
from google.adk.runners import Runner
from google.genai.types import Content, Part
from google.adk.tools.function_tool import FunctionTool
import re

session_service = InMemorySessionService()
MODEL = "gemini-2.0-flash-001"
APP_NAME = "cappy_app"
USER_ID = "local_user"
SESSION_ID = "main"



def extract_json_block(text: str) -> str:
    if not text:
        return ""
    s = text.strip()

    # 1) Strip Markdown code fences if present
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.DOTALL).strip()

    # 2) Fallback: pull out the first {...} block
    if not s.startswith("{"):
        i, j = s.find("{"), s.rfind("}")
        if i != -1 and j != -1 and j > i:
            s = s[i : j + 1].strip()

    return s



# ---------- Score each card ----------
def score_card(card, spending_by_category):
    rewards = card.get("rewards", {})
    score = 0.0
    for category, spent in spending_by_category.items():
        rate = rewards.get(category, rewards.get("Other", 0.0))
        score += spent * rate
    score -= card.get("annual_fee", 0)  # subtract annual fee for net estimate
    return score

def compare_cards(synthetic_transactions_json: str, credit_card_json: str) -> str:
    """
    Analyzes a customer's purchase history against a catalog of credit cards 
    to calculate the estimated annual net rewards for each. 
    
    This function should be called when the user asks for a credit card 
    recommendation based on their spending profile.

    Args:
        synthetic_transactions_json: A JSON string containing the user's categorized transaction history.
                            Must be an array of objects with 'category' and 'amount' fields.
        credit_card_json: A JSON string of the credit card catalog, including reward rates and fees.

    Returns:
        A JSON string containing the final comparison result, including the top 3 cards 
        and their calculated net rewards, which the AI should then use to generate a response.
    """
    
    # 1. Load Data: Deserialize the JSON strings passed by the agent
    purchases: list[dict[str, Any]] = json.loads(synthetic_transactions_json)
    card_catalog: list[dict[str, Any]] = json.loads(credit_card_json)

    # 2. Aggregate Spending
    spending_by_category = {}
    for txn in purchases:
        if txn.get("type") in ["debit", None]:
            cat = txn.get("merchantCategory") or txn.get("category")
            amt = txn.get("amount")
            if cat and isinstance(amt, (int, float)):
                spending_by_category[cat] = spending_by_category.get(cat, 0) + amt

        # 3. Score All Cards
    card_scores = []
    for card in card_catalog:
        # Use the dedicated helper logic
        net_rewards = score_card(card, spending_by_category)
        card_scores.append({
            "name": card["name"],
            "net_rewards": round(net_rewards, 2),
            "annual_fee": card["annual_fee"],
            "min_credit_score": card["min_credit_score"],
            "reward_structure": card["rewards"],
            "card_id": card["id"],
        })

        # 4. Finalize and Return
    card_scores.sort(key=lambda x: x["net_rewards"], reverse=True)
    

    return json.dumps({
        "top_recommendations": card_scores,   # sorted desc by net_rewards
        "spending_profile": spending_by_category
    })

compare_cards_tool = FunctionTool(compare_cards)


card_agent = LlmAgent(
    model=MODEL,
    name="Cappy",
    description="Credit card expert that ranks cards based on the user's spending profile.",
    instruction=(
        "You are Cappy. When purchase history and a card catalog are available, "
        "CALL the compare_cards tool with those two JSON strings. "
        "Then produce a final JSON object EXACTLY matching this schema:\n"
        "{\n"
        '  "recommendations": [\n'
        '    {"card_id": string, "name": string, "net_rewards": number, "reason": string},\n'
        '    {"card_id": string, "name": string, "net_rewards": number, "reason": string},\n'
        '    {"card_id": string, "name": string, "net_rewards": number, "reason": string}\n'
        "  ]\n"
        "}\n"
        "When selecting cards, make sure that the cards are not derivatives of eachother"
        "That means you can NOT select one version of the card, the student version of that same card, or the Good credit of each card, you must decide which of those derivatives is the best match"
        "If you select two derivative credit cards of eachother, select the next best option of a different variety"
        "Rules: pick the top 3 by net_rewards from the tool output;"
        "You should have 3 reasons for every card"
        "First line of reasoning: You first want to cite why the card is a strong match with the shopping profile."
        "Second line of reasoning:  Next, you want to explain its placement within the rankings among the cards, and why it outperforms other cards."
        "Finally, you must add an further justification as to why it is a good fit for the customer, providing the reasons that it will benefit the customers lifestyle"
        "The reasonings for each individual cardmust all be seperated as a list in the format: Reason #X, in which X is a place holder for 1, 2, 3"
        "grounded in the spending profile and card features (categories, fees). Do NOT include any extra text—JSON ONLY."
        "Output MUST be raw JSON only (no code fences, no prose, no backticks)."
    ),
    tools=[compare_cards_tool],
)




# ---------- Expanded CARD_CATALOG ----------
CARD_CATALOG = [
    {
        "id": "quicksilver",
        "name": "Quicksilver®",
        "category": "cashback",
        "annual_fee": 0,
        "min_credit_score": "Good-Excellent",
        "features": ["unlimited-1.5pct"],
        "rewards": {"Dining": 0.015, "Grocery Stores": 0.015, "Retail": 0.015, "Travel": 0.015, "Gas": 0.015, "Entertainment/Streaming": 0.015, "Other": 0.015},
    },
    {
        "id": "quicksilverone",
        "name": "QuicksilverOne®",
        "category": "cashback",
        "annual_fee": 39,
        "min_credit_score": "Fair-Good",
        "features": ["unlimited-1.5pct", "automatic-credit-line-review"],
        "rewards": {"Dining": 0.015, "Grocery Stores": 0.015, "Retail": 0.015, "Travel": 0.015, "Gas": 0.015, "Entertainment/Streaming": 0.015, "Other": 0.015},
    },
    {
        "id": "savor",
        "name": "Savor®",
        "category": "cashback",
        "annual_fee": 0,
        "min_credit_score": "Excellent",
        "features": ["dining", "entertainment", "grocery"],
        "rewards": {"Dining": 0.03, "Grocery Stores": 0.03, "Retail": 0.01, "Travel": 0.01, "Gas": 0.01, "Entertainment/Streaming": 0.03, "Other": 0.01},
    },
    {
        "id": "savorone",
        "name": "SavorOne®",
        "category": "cashback",
        "annual_fee": 0,
        "min_credit_score": "Good-Excellent",
        "features": ["dining", "entertainment", "grocery"],
        "rewards": {"Dining": 0.03, "Grocery Stores": 0.03, "Retail": 0.01, "Travel": 0.01, "Gas": 0.01, "Entertainment/Streaming": 0.03, "Other": 0.01},
    },
    {
        "id": "4",
        "name": "VentureOne Rewards",
        "category": "travel",
        "annual_fee": 0,
        "min_credit_score": "Excellent",
        "features": ["Enjoy a $100 credit to use towards flights, stays and rental cars booked through Capital One Travel during your first cardholder year","1.25x-miles", "5x-miles at transfer-partners"],
        "rewards": {"Dining": 0.015, "Grocery Stores": 0.015, "Retail": 0.015, "Travel": 0.015, "Gas": 0.015, "Entertainment/Streaming": 0.015, "Other": 0.015},
    },
    {
        "id": "3",
        "name": "Venture Rewards",
        "category": "travel",
        "annual_fee": 95,
        "min_credit_score": "Good-Excellent",
        "features": ["Earn 75,000 bonus miles once you spend $4,000 on purchases within the first 3 months from account opening 2","2 miles per dollar spent", "5 miles per dollar on hotels and rental cars booked through Capital One Travel"],
        "rewards": {"Dining": 0.02, "Grocery Stores": 0.02, "Retail": 0.02, "Travel": 0.02, "Gas": 0.02, "Entertainment/Streaming": 0.02, "Other": 0.02},
    },
    {
        "id": "2",
        "name": "Venture X Rewards",
        "category": "premium travel",
        "annual_fee": 395,
        "min_credit_score": "Excellent",
        "features": ["Earn 75,000 bonus miles once you spend $4,000 on purchases within the first 3 months from account opening","10x miles on hotels and rental booked through Capital One Travel","5x miles on flights and vacations booked through Capital One travel","lounge-access", "travel-credits", "2x-miles"],
        "rewards": {"Dining": 0.02, "Grocery Stores": 0.02, "Retail": 0.02, "Travel": 0.02, "Gas": 0.02, "Entertainment/Streaming": 0.02, "Other": 0.02},
    },
    {
        "id": "1",
        "name": "Platinum Mastercard",
        "category": "credit-building",
        "annual_fee": 0,
        "min_credit_score": "Fair",
        "features": ["credit-builder"],
        "rewards": {"Dining": 0.0, "Grocery Stores": 0.0, "Retail": 0.0, "Travel": 0.0, "Gas": 0.0, "Entertainment/Streaming": 0.0, "Other": 0.0},
    },
    {
        "id": "secured",
        "name": "Secured Mastercard®",
        "category": "credit-building",
        "annual_fee": 0,
        "min_credit_score": "Poor-Fair",
        "features": ["secured-credit-line"],
        "rewards": {"Dining": 0.0, "Grocery Stores": 0.0, "Retail": 0.0, "Travel": 0.0, "Gas": 0.0, "Entertainment/Streaming": 0.0, "Other": 0.0},
    },
    {
        "id": "journey",
        "name": "Journey Student",
        "category": "student",
        "annual_fee": 0,
        "min_credit_score": "Student",
        "features": ["student", "on-time-payment-bonus"],
        "rewards": {"Dining": 0.01, "Grocery Stores": 0.01, "Retail": 0.01, "Travel": 0.01, "Gas": 0.01, "Entertainment/Streaming": 0.01, "Other": 0.01},
    },
]



async def main():
    # 1) Read raw JSON strings (not Python objects)
    TRANSACTION_FILE = Path("synthetic_transactions.json")
    transactions_json = TRANSACTION_FILE.read_text(encoding="utf-8")

    CARD_FILE = Path("credit_card.json")
    cards_json = CARD_FILE.read_text(encoding="utf-8")

    # (Optional) sanity checks
    print("Transactions file length:", len(transactions_json))
    print("Cards file length:", len(cards_json))

    # 2) Set up runner
    runner = Runner(agent=card_agent, app_name=APP_NAME, session_service=session_service)
    await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    # 3) Single, deterministic prompt that tells the agent to call the tool and THEN return JSON only
    directive = (
        "You have two JSON strings. Call the compare_cards tool with them exactly as strings, "
        "then return ONLY the final JSON per the schema (no other text).\n"
        f"synthetic_transactions_json={transactions_json}\n"
        f"credit_card_json={cards_json}\n"
    )
    msg = Content(role="user", parts=[Part(text=directive)])

    final_text = None
    async for ev in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=msg):
        if ev.is_final_response() and ev.content and ev.content.parts:
            final_text = ev.content.parts[0].text

    if not final_text:
        raise RuntimeError("Agent returned no response.")

    #AI Keeps giving data in Markdown, fixing that
    final_text = extract_json_block(final_text)

    # 4) Try to parse JSON; if it fails, print what the model returned so you can see the problem
    try:
        data = json.loads(final_text)
    except json.JSONDecodeError:
        print("---- MODEL RAW OUTPUT (not valid JSON) ----")
        print(final_text)  # helps you debug if the model added prose
        raise

    # 5) Validate schema
    assert "recommendations" in data and len(data["recommendations"]) == 3, "Agent must return exactly 3 recommendations."
    for r in data["recommendations"]:
        assert all(k in r for k in ("card_id", "name", "net_rewards", "reason")), "Missing keys in a recommendation."

    print(json.dumps(data, indent=2))
    OUTPUT_FILE = Path("recommendations.json")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
