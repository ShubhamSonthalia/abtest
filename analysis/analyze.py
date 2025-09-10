import pandas as pd
import math
from scipy.stats import norm
import os

csv_path = '../backend/events.csv'

if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    print("No event data found. Please generate some events before running analysis.")
    exit()

df = pd.read_csv(csv_path)

if df.empty:
    print("Event file is empty. Please generate some events before running analysis.")
    exit()

# Load event data
df = pd.read_csv("../backend/events.csv")

# Count users per variant
views = df[df["event_type"] == "view"].groupby("variant")["visitor_id"].nunique()
conversions = df[df["event_type"] == "conversion"].groupby("variant")["visitor_id"].nunique()

print("Views per variant:\n", views)
print("Conversions per variant:\n", conversions)

# Extract numbers
nA = views.get("A", 0)
nB = views.get("B", 0)
xA = conversions.get("A", 0)
xB = conversions.get("B", 0)

print(f"\nVariant A: {xA}/{nA} conversions")
print(f"Variant B: {xB}/{nB} conversions")

# Compute sample proportions
pA = xA / nA if nA > 0 else 0
pB = xB / nB if nB > 0 else 0
p_pool = (xA + xB) / (nA + nB)

# Standard error
se = math.sqrt(p_pool * (1 - p_pool) * (1/nA + 1/nB))

# z-statistic
z = (pB - pA) / se if se > 0 else 0
p_value = 2 * (1 - norm.cdf(abs(z)))

print("\n=== Statistical Test Results ===")
print("pA =", round(pA, 3), "pB =", round(pB, 3))
print("Pooled p =", round(p_pool, 3))
print("Standard Error =", round(se, 4))
print("z =", round(z, 3))
print("p-value =", round(p_value, 4))

if p_value < 0.05:
    print("Reject H0 → Statistically significant difference.")
else:
    print("Fail to reject H0 → No significant difference.")
