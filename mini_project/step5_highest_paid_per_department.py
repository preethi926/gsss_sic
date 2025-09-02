import pandas as pd

df = pd.read_csv("employees_enriched.csv")

idx = df.groupby("Department")["Salary"].idxmax()
highest_paid = df.loc[idx, ["Department","EmpID","Name","JobTitle","Salary"]].sort_values("Department")

highest_paid.to_csv("highest_paid.csv", index=False)
print("✅ Highest paid per dept -> highest_paid.csv")
print(highest_paid)
