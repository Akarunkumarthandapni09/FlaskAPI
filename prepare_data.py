# prepare_data.py
import pandas as pd

# Load Excel file
df = pd.read_excel("request_types_approvals.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Rename for consistency
df = df.rename(columns={
    "Request Type": "request_type",
    "Description": "description",
    "Approvals Needed From": "approval_flow"
})

# Normalize arrows and spaces
df['approval_flow'] = df['approval_flow'].str.replace('→','->').str.strip()
df['description'] = df['description'].str.strip()

# Drop rows with missing values
df = df.dropna(subset=['request_type', 'description', 'approval_flow'])

# Save cleaned version for training
df.to_csv("request_types_approvals_clean.csv", index=False)
print("✅ Cleaned data saved to request_types_approvals_clean.csv")
