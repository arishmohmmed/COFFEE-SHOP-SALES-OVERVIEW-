
import pandas as pd
from dateutil import parser

# --- CONFIG ---
INPUT_CSV = "coffee_shop_messy_dataset_50000plus.csv"
OUTPUT_EXCEL = "coffee_shop_cleaned_final.xlsx"

# Gender mapping you provided
GENDER_MAP = {
    "Keerthi": "Female", "Priya": "Female", "Nisha": "Female",
    "Sanjay": "Male", "Monish": "Male", "Aishwarya": "Female",
    "Arun": "Male", "Divya": "Female", "Harish": "Male",
    "Meena": "Female", "Ananya": "Female", "Karthik": "Male",
    "Rahul": "Male", "Rohit": "Male", "Vignesh": "Male"
}
lower_gender_map = {k.lower(): v for k, v in GENDER_MAP.items()}

# 1. Load data
df = pd.read_csv(INPUT_CSV, low_memory=False)
print(f"Original shape: {df.shape}")

# 2. Remove columns: delivery, tax, coupon, feedback, employee, loyalty points, total amounts
# Keeping Rating, Discount_Amount, Total_Amount for later calculations
cols_to_remove = ['Delivery_Minutes', 'Tax_5%', 'Coupon_Code', 'Feedback', 'Employee', 'Loyalty_Points']
df = df.drop(columns=[c for c in cols_to_remove if c in df.columns])

# If you want STRICT removal including Total_Amount, uncomment next line:
# df = df.drop(columns=['Total_Amount'], errors='ignore')

# 3. Remove null values in Customer_Name and Gender
df = df.dropna(subset=['Customer_Name', 'Gender'])

# 4. Customer_Type: walk_in / walk-in -> New (case-insensitive)
def clean_customer_type(x):
    if pd.isna(x):
        return x
    s = str(x).strip().lower()
    if s in ['walk-in', 'walk_in', 'walk in', 'walkin']:
        return 'New'
    return x

df['Customer_Type'] = df['Customer_Type'].apply(clean_customer_type)

# 5. Rating: fill null by mean
if 'Rating' in df.columns:
    df['Rating'] = df['Rating'].fillna(df['Rating'].mean())

# 6. Date parsing: robust parser for mixed formats -> dd-mm-yy
def robust_parse(s):
    if pd.isna(s):
        return pd.NaT
    s = str(s).strip()
    for dayfirst in [False, True]:
        try:
            dt = parser.parse(s, dayfirst=dayfirst)
            if 2020 <= dt.year <= 2026:
                return dt
        except:
            continue
    return pd.NaT

df['Order_Date_parsed'] = df['Order_Date'].apply(robust_parse)
df['Order_Date'] = df['Order_Date_parsed'].dt.strftime('%d-%m-%y')
df = df.drop(columns=['Order_Date_parsed'])

# 7. Whole numbers: Rating, Discount_Amount, Total_Amount, Quantity, Unit_Price
for col in ['Rating', 'Discount_Amount', 'Total_Amount', 'Quantity', 'Unit_Price']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).round().astype(int)

# 8. Gender correction using name mapping
df['Gender'] = df.apply(lambda r: lower_gender_map.get(str(r['Customer_Name']).strip().lower(), r['Gender']), axis=1)

# 9. Sort by Order_ID ascending
df = df.sort_values(by='Order_ID', ascending=True)

# 10. Proper case conversion (except Order_ID, Customer_ID, Order_Date)
proper_cols = ['Customer_Name', 'Gender', 'Customer_Type', 'City', 'Branch', 'Product', 'Category', 'Payment_Method', 'Order_Type']
for col in proper_cols:
    if col in df.columns:
        mask = df[col].notna()
        df.loc[mask, col] = df.loc[mask, col].astype(str).str.strip().str.lower().str.title()

# Re-apply gender mapping after proper case
df['Gender'] = df.apply(lambda r: lower_gender_map.get(str(r['Customer_Name']).strip().lower(), r['Gender']), axis=1)
df['Gender'] = df['Gender'].astype(str).str.title()

# 11. Create Total_Sales and Payment_Amount
# Total_Sales = Quantity * Unit_Price
# Payment_Amount = Total_Sales - Discount_Amount
df['Total_Sales'] = df['Quantity'] * df['Unit_Price']
df['Payment_Amount'] = df['Total_Sales'] - df['Discount_Amount']

# Make them whole numbers
df['Total_Sales'] = df['Total_Sales'].astype(int)
df['Payment_Amount'] = df['Payment_Amount'].astype(int)

# 12. Fill remaining nulls with mode (whole excel)
for col in df.columns:
    if df[col].isna().sum() > 0:
        mode_val = df[col].mode(dropna=True)
        if not mode_val.empty:
            df[col] = df[col].fillna(mode_val.iloc[0])

print(f"Final shape: {df.shape}, Nulls: {df.isna().sum().sum()}")

# 13. Save to Excel
df.to_excel(OUTPUT_EXCEL, index=False)
print(f"Saved to {OUTPUT_EXCEL}")
