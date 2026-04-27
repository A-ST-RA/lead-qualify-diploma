import pandas as pd

df = pd.read_csv("leads_big.csv")

df["source"] = [
    "google_ads", "social", "organic", "referral", "email",
    "social", "google_ads", "referral", "email", "organic",
] * 4

df["industry"] = [
    "fintech", "education", "ecommerce", None, "fintech",
    "education", "ecommerce", "fintech", None, "education",
] * 4

df.to_csv("leads_big.csv", index=False)