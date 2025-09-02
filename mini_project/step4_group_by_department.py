import pandas as pd

df = pd.read_csv("employees_enriched.csv")

dept_summary = df.groupby("Department").agg(
    Avg_Salary=("Salary","mean"),
    Total_Salary=("Salary","sum"),
    Employee_Count=("EmpID","count")
).reset_index().sort_values("Department")

dept_summary.to_csv("dept_summary.csv", index=False)
print("✅ Department summary -> dept_summary.csv")
print(dept_summary)
