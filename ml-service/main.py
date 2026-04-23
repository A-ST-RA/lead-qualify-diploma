import pandas as pd

df = pd.read_csv("leads.csv")

# print("\nAverage budget by deal result:")
# print(df.groupby("deal_won")["requested_budget"].mean())

# print("\nAverage time on site by deal result:")
# print(df.groupby("deal_won")["time_on_site_sec"].mean())

print("\nAverage viewed pricing by deal result:")
print(df.groupby("deal_won")["viewed_pricing"].mean())