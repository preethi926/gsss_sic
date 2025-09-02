import pandas as pd

df = pd.read_csv("employees_enriched.csv")

job_summary = df.groupby("JobTitle").agg(
    Avg_Salary=("Salary","mean"),
    Total_Salary=("Salary","sum"),
    Employee_Count=("EmpID","count")
).reset_index().sort_values("Avg_Salary", ascending=False)

job_summary.to_csv("job_summary.csv", index=False)
print("✅ Job title summary -> job_summary.csv")
print(job_summary)