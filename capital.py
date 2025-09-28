<<<<<<< HEAD
"""
generate_synthetic_transactions.py

Generates realistic synthetic transaction data for one customer across multiple accounts.
Outputs:
  - synthetic_transactions.json
  - synthetic_transactions.csv

Usage:
  pip install pandas
  python generate_synthetic_transactions.py
"""

=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

<<<<<<< HEAD
import pandas as pd  # used for easy CSV export

# ---------- Configuration ----------
NUM_ACCOUNTS = 3
=======
import pandas as pd

# ---------- Configuration ----------
NUM_ACCOUNTS_PER_USER = 3
USER_NAMES = ["Kyle", "Emilio", "Griffin", "Graham"]
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
DAYS_HISTORY = 180
AVG_TRANSACTIONS_PER_DAY = 0.8
START_DATE = datetime.now() - timedelta(days=DAYS_HISTORY)
CURRENCY = "USD"
<<<<<<< HEAD
OUTPUT_JSON = Path("synthetic_transactions.json")
OUTPUT_CSV = Path("synthetic_transactions.csv")
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
SEED = 42
# -----------------------------------

random.seed(SEED)

# ---------- Merchant catalog ----------
MERCHANT_CATALOG = [
<<<<<<< HEAD
    # Dining
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    ("Starbucks", "5814", "Dining", (3, 8), "in-store"),
    ("Chipotle", "5814", "Dining", (8, 15), "in-store"),
    ("McDonald's", "5814", "Dining", (5, 12), "in-store"),
    ("Panera Bread", "5814", "Dining", (6, 15), "in-store"),
<<<<<<< HEAD

    # Grocery Stores
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    ("Whole Foods Market", "5411", "Grocery Stores", (10, 120), "in-store"),
    ("Trader Joe's", "5411", "Grocery Stores", (10, 100), "in-store"),
    ("Walmart", "5411", "Grocery Stores", (5, 150), "in-store"),
    ("Kroger", "5411", "Grocery Stores", (10, 120), "in-store"),
<<<<<<< HEAD

    # Retail
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    ("Amazon", "5942", "Retail", (5, 500), "online"),
    ("Target", "5311", "Retail", (10, 300), "in-store"),
    ("Best Buy", "5732", "Retail", (20, 1000), "in-store"),
    ("Macy's", "5311", "Retail", (15, 600), "in-store"),
<<<<<<< HEAD

    # Travel
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    ("Delta Air Lines", "4511", "Travel", (150, 900), "online"),
    ("United Airlines", "4511", "Travel", (150, 900), "online"),
    ("Lyft", "4121", "Travel", (5, 60), "online"),
    ("Uber", "4121", "Travel", (5, 60), "online"),
    ("Marriott Hotels", "7011", "Travel", (100, 500), "online"),
<<<<<<< HEAD

    # Entertainment/Streaming
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    ("Spotify", "4899", "Entertainment/Streaming", (10, 15), "recurring"),
    ("Netflix", "4899", "Entertainment/Streaming", (8, 15), "recurring"),
    ("Disney+", "4899", "Entertainment/Streaming", (8, 15), "recurring"),
    ("Hulu", "4899", "Entertainment/Streaming", (8, 15), "recurring"),
<<<<<<< HEAD

    # Gas
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    ("Shell Oil", "5541", "Gas", (15, 70), "in-store"),
    ("ExxonMobil", "5541", "Gas", (15, 80), "in-store"),
    ("BP", "5541", "Gas", (15, 75), "in-store"),
    ("Chevron", "5541", "Gas", (15, 80), "in-store"),
]

<<<<<<< HEAD
# Recurring items
RECURRING_ITEMS = [
    ("Spotify", 30),
    ("Netflix", 30),
]

# Account types (checking and credit card only)
=======
RECURRING_ITEMS = [("Spotify", 30), ("Netflix", 30)]
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
ACCOUNT_TYPES = ["checking", "credit_card"]

# ---------- Helper functions ----------
def rnd_amount(low, high):
    return round(random.uniform(low, high), 2)

def mk_txn_id():
    return str(uuid.uuid4())

def mk_date(n_days_from_start):
    dt = START_DATE + timedelta(days=n_days_from_start, seconds=random.randint(0, 86400))
    return dt.isoformat(timespec="seconds")

def pick_account(accounts):
<<<<<<< HEAD
    # only choose checking or credit card
    weights = []
    for acc in accounts:
        if acc["type"] == "checking":
            weights.append(0.5)
        elif acc["type"] == "credit_card":
            weights.append(0.5)
=======
    weights = [0.5 if acc["type"] in ("checking", "credit_card") else 0 for acc in accounts]
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
    total = sum(weights)
    r = random.random() * total
    cum = 0
    for i, w in enumerate(weights):
        cum += w
        if r <= cum:
            return accounts[i]
    return accounts[-1]

<<<<<<< HEAD
# ---------- Generate accounts ----------
def generate_accounts(n=NUM_ACCOUNTS):
    accounts = []
    for i in range(n):
        acc_type = ACCOUNT_TYPES[i % len(ACCOUNT_TYPES)]  # only checking/credit card
        accounts.append({
            "id": f"acct-{i+1}",
            "type": acc_type,
            "name": f"{acc_type.title()} Account #{i+1}",
=======
def generate_accounts(username, n=NUM_ACCOUNTS_PER_USER):
    accounts = []
    for i in range(n):
        acc_type = ACCOUNT_TYPES[i % len(ACCOUNT_TYPES)]
        accounts.append({
            "id": f"{username.lower()}-acct-{i+1}",  # account id includes username
            "type": acc_type,
            "name": f"{username}'s {acc_type.title()} Account #{i+1}",
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
            "currency": CURRENCY
        })
    return accounts

<<<<<<< HEAD
# ---------- Generate transactions ----------
=======
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
def generate_transactions_for_customer(accounts):
    transactions = []

    # Recurring transactions
    for merchant_name, freq_days in RECURRING_ITEMS:
        merchant = next((m for m in MERCHANT_CATALOG if m[0] == merchant_name), None)
        if not merchant:
            continue
        _, mcc, category, rng, _ = merchant
        acct = random.choice([a for a in accounts if a["type"] in ("checking", "credit_card")])
        offset = random.randint(0, freq_days - 1)
        for day in range(offset, DAYS_HISTORY, freq_days):
            txn = {
                "transactionId": mk_txn_id(),
                "accountId": acct["id"],
                "accountType": acct["type"],
                "date": mk_date(day),
                "amount": rnd_amount(rng[0], rng[1]),
                "currency": CURRENCY,
                "merchantName": merchant_name,
                "mcc": mcc,
                "merchantCategory": category,
                "type": "debit",
                "description": f"{merchant_name} {category} payment",
                "isRecurring": True,
            }
            transactions.append(txn)

    # One-off/random transactions
    num_days = DAYS_HISTORY
    expected_txns = max(1, int(num_days * AVG_TRANSACTIONS_PER_DAY))
    for _ in range(expected_txns):
        day = random.randint(0, num_days - 1)
        acct = pick_account(accounts)
        merchant = random.choice(MERCHANT_CATALOG)
        name, mcc, cat, rng, _ = merchant
        is_refund = random.random() < 0.05
        amount = rnd_amount(rng[0], rng[1])
        ttype = "credit" if is_refund else "debit"
        txn = {
            "transactionId": mk_txn_id(),
            "accountId": acct["id"],
            "accountType": acct["type"],
            "date": mk_date(day),
            "amount": amount,
            "currency": CURRENCY,
            "merchantName": name,
            "mcc": mcc,
            "merchantCategory": cat,
            "type": ttype,
            "description": f"{name} {cat}",
            "isRecurring": False,
        }
        transactions.append(txn)

    transactions.sort(key=lambda x: x["date"])
    return transactions

<<<<<<< HEAD
# ---------- Save outputs ----------
def save_outputs(transactions):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    df = pd.DataFrame(transactions)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {len(transactions)} transactions to {OUTPUT_JSON} and {OUTPUT_CSV}")

# ---------- Run ----------
if __name__ == "__main__":
    accounts = generate_accounts(NUM_ACCOUNTS)
    print("Generated accounts:", accounts)
    
    txns = generate_transactions_for_customer(accounts)
    save_outputs(txns)

    # ---------- TEST PRINT ----------
    print("\n===== TEST SUMMARY =====")
    print(f"Total accounts generated: {len(accounts)}")
    print(f"Total transactions generated: {len(txns)}")
    print("\nSample transactions (first 5):")
    for txn in txns[:5]:
        print(json.dumps(txn, indent=2))
=======
def save_outputs(transactions, username):
    json_path = Path(f"synthetic_transactions_{username}.json")
    csv_path = Path(f"synthetic_transactions_{username}.csv")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    pd.DataFrame(transactions).to_csv(csv_path, index=False)
    print(f"Wrote {len(transactions)} transactions to {json_path} and {csv_path}")

# ---------- Run ----------
if __name__ == "__main__":
    for username in USER_NAMES:
        print(f"\nGenerating data for {username}...")
        accounts = generate_accounts(username)
        txns = generate_transactions_for_customer(accounts)
        save_outputs(txns, username)
>>>>>>> 003eddc1b094243dd596aaf20ca0d84eaf191d4c
