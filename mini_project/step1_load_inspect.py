import pandas as pd

df = pd.read_csv("employees.csv")
print("✅ Loaded employees.csv")
print("\n--- info() ---")
print(df.info())
print("\n--- head() ---")
print(df.head())
print("\n--- describe() ---")
print(df.describe())
