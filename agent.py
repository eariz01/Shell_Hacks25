import json
from pathlib import Path

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

# ---------- Load synthetic transactions ----------
TRANSACTION_FILE = Path("synthetic_transactions.json")
with open(TRANSACTION_FILE, "r", encoding="utf-8") as f:
    transactions = json.load(f)

# ---------- Aggregate spending by category ----------
spending_by_category = {}
for txn in transactions:
    if txn["type"] == "debit":  # only spent amounts
        cat = txn["merchantCategory"]
        amt = txn["amount"]
        spending_by_category[cat] = spending_by_category.get(cat, 0) + amt

# ---------- Score each card ----------
def score_card(card, spending_by_category):
    rewards = card.get("rewards", {})
    score = 0.0
    for category, spent in spending_by_category.items():
        rate = rewards.get(category, rewards.get("Other", 0.0))
        score += spent * rate
    score -= card.get("annual_fee", 0)  # subtract annual fee for net estimate
    return score

card_scores = []
for card in CARD_CATALOG:
    score = score_card(card, spending_by_category)
    card_scores.append((card["name"], score))

# ---------- Recommend top cards ----------
card_scores.sort(key=lambda x: x[1], reverse=True)

print("\n===== Top Credit Card Recommendations =====")
for name, expected_rewards in card_scores[:5]:
    print(f"{name}: Estimated net rewards ${expected_rewards:.2f}")

print("\n===== Spending Summary by Category =====")
for cat, amt in spending_by_category.items():
    print(f"{cat}: ${amt:.2f}")
