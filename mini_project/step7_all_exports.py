# Runs steps 2 -> 6 in one go. Assumes employees.csv is present.
import subprocess, sys
steps = [
    "step2_clean_standardize.py",
    "step3_add_derived_column.py",
    "step4_group_by_department.py",
    "step5_highest_paid_per_department.py",
    "step6_group_by_jobtitle.py",
]
for s in steps:
    print(f"\n=== Running {s} ===")
    ret = subprocess.call([sys.executable, s])
    if ret != 0:
        print(f" {s} failed with code {ret}")
        sys.exit(ret)
print("\n✅ All outputs ready: cleaned_employees.csv, employees_enriched.csv, dept_summary.csv, highest_paid.csv, job_summary.csv")
