import pandas as pd
import numpy as np

df = pd.read_csv("employees.csv")

# Remove exact duplicate rows
df = df.drop_duplicates()

# If duplicate EmpID exists, keep first
df = df.drop_duplicates(subset=["EmpID"], keep="first")

# Handle missing values (if any)
if df["Salary"].isna().any():
    df["Salary"] = df["Salary"].fillna(df["Salary"].median())
if df["JobTitle"].isna().any():
    df["JobTitle"] = df["JobTitle"].fillna("Unknown")

# Standardize Department names
dep = df["Department"].astype(str).str.strip()
dep = dep.str.replace(r"(?i)^hr$", "HR", regex=True)\
         .str.replace(r"(?i)^it$", "IT", regex=True)\
         .str.replace(r"(?i)^finance$", "Finance", regex=True)\
         .str.replace(r"(?i)^sales$", "Sales", regex=True)
df["Department"] = dep

# Standardize Job Titles (covers common variants)
jt = df["JobTitle"].astype(str).str.strip()
jt = jt.replace({
    "Software Engg": "Software Engineer",
    "Sales Exec": "Sales Executive",
    "HR Exec": "HR Executive"
})
# Fix some HR casing variants
jt = jt.replace({r"(?i)^hr executive$": "HR Executive",
                 r"(?i)^hr manager$": "HR Manager"}, regex=True)
df["JobTitle"] = jt

df.to_csv("cleaned_employees.csv", index=False)
print("✅ Cleaned & standardized -> cleaned_employees.csv")
print(df.head())
