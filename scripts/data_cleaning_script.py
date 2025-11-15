import pandas as pd
import numpy as np

# --- 1. CONFIGURATION ---
INPUT_FILE = "../data/Churn_Modelling.csv"
OUTPUT_FILE = "../data/Bank_Churn_Model_Cleaned.csv"

# --- 2. LOAD DATA ---
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"Error: Input file not found at {INPUT_FILE}. Please ensure it is in the '../data/' directory.")
    exit()

# --- 3. POWER QUERY SIMULATION STEPS (Column Removal and Recoding) ---

# Drop irrelevant ID columns (as determined in the analysis phase)
df = df.drop(columns=['RowNumber', 'CustomerId', 'Surname'])

# Recode Binary Columns for Power BI visualization clarity
# Exited: 0 -> Retained, 1 -> Churned
df['Exited'] = df['Exited'].map({0: 'Retained', 1: 'Churned'})

# IsActiveMember: 0 -> Inactive, 1 -> Active
df['IsActiveMember'] = df['IsActiveMember'].map({0: 'Inactive', 1: 'Active'})

# HasCrCard: 0 -> No, 1 -> Yes (Though less critical for churn analysis, done for consistency)
df['HasCrCard'] = df['HasCrCard'].map({0: 'No', 1: 'Yes'})

# --- 4. FEATURE ENGINEERING (Creating Segmentation Bins for Power BI) ---

# A. Age Group (for Page 2 Segmentation)
bins_age = [18, 30, 45, 60, df['Age'].max() + 1] # +1 for inclusivity
labels_age = ['18-30 (Young)', '31-45 (Mid-Career)', '46-60 (High Risk)', '60+ (Retired)']
df['Age Group'] = pd.cut(
    df['Age'], 
    bins=bins_age, 
    labels=labels_age, 
    right=False,
    include_lowest=True
)
# Fill potential NaNs from edge cases with 'Unknown'
df['Age Group'] = df['Age Group'].cat.add_categories('Unknown').fillna('Unknown')

# B. Tenure Group (for Page 2 Segmentation)
bins_tenure = [0, 2, 5, 8, df['Tenure'].max() + 1]
labels_tenure = ['0-1 Year (New)', '2-4 Years (Early)', '5-7 Years (Stable)', '8+ Years (Loyalty)']
df['Tenure Group'] = pd.cut(
    df['Tenure'], 
    bins=bins_tenure, 
    labels=labels_tenure, 
    right=False,
    include_lowest=True
)
df['Tenure Group'] = df['Tenure Group'].cat.add_categories('Unknown').fillna('Unknown')

# --- 5. SAVE CLEANED DATA ---
df.to_csv(OUTPUT_FILE, index=False)

print("\n--- Data Cleaning Complete ---")
print(f"Cleaned data saved to: {OUTPUT_FILE}")
print(f"Final shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("\nReady to import 'Bank_Churn_Model_Cleaned.csv' into Power BI.")