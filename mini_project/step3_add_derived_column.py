import pandas as pd

df = pd.read_csv("cleaned_employees.csv")

df["JoiningDate"] = pd.to_datetime(df["JoiningDate"], errors="coerce")
today = pd.to_datetime("today").normalize()
df["YearsOfService"] = ((today - df["JoiningDate"]).dt.days // 365).astype("Int64")

df.to_csv("employees_enriched.csv", index=False)
print("✅ Added YearsOfService -> employees_enriched.csv")
print(df[["EmpID","Name","Department","JobTitle","JoiningDate","YearsOfService"]].head())
