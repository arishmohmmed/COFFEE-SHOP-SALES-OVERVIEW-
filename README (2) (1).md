# ☕ Coffee Shop Sales Data Cleaning & Power BI Dashboard Project

> End-to-end data analytics project: From a **messy 50K+ rows dataset** to a **clean, analysis-ready dataset** using Python, and visualized with an interactive **Power BI Dashboard**.

### 📌 Project Overview
This project demonstrates a complete data cleaning and visualization workflow for a coffee shop chain operating across Chennai and nearby regions.

The raw dataset was highly inconsistent with mixed date formats, mislabeled genders, null values, inconsistent categories, and irrelevant columns. I cleaned it using **Python (Pandas + dateutil)** and then built a sales overview dashboard in **Power BI** to extract business insights.

---

### 📁 Files in this Repository

| File | Description |
|------|-------------|
| `coffee_shop_messy_dataset_50000plus_1.csv` | Original raw dataset - 50,580 rows, 25 columns |
| `Coffee-Shop-Cleaning-Code.py` | Python cleaning script |
| `Coffee-Shop-Cleaned-Strict-Mode-Filled_1.xlsx` | Final cleaned dataset - 48,661 rows, 20 columns |
| `Coffee Shop Sales Report.pbix` | Power BI file (if you add it) |

---

### 🗃️ Raw Data Issues Identified

The original dataset had **25 columns**:
`Order_ID, Order_Date, Customer_ID, Customer_Name, Age, Gender, Customer_Type, City, Branch, Product, Category, Quantity, Unit_Price, Discount_%, Discount_Amount, Tax_5%, Total_Amount, Payment_Method, Order_Type, Employee, Coupon_Code, Rating, Feedback, Loyalty_Points, Delivery_Minutes`

**Major issues:**
- Nulls in `Customer_Name` and `Gender`
- Mixed formats in `Order_Date` (`2025-01-02 21:51:00`, `19 Aug 2025 16:18`, `2024/02/25 13:09`, `10/03/2023`)
- Gender mislabeling (e.g., `Keerthi` marked as Male, `Sanjay` marked as Female)
- Inconsistent `Customer_Type`: `walk_in`, `walk-in`, `walk in`, `walkin`
- Inconsistent casing: `FOOD`, `food`, `Food`, `Dine In`, `DINE IN`, `UPI`, `Upi`
- Irrelevant columns for sales analysis: `Delivery_Minutes`, `Tax_5%`, `Coupon_Code`, `Feedback`, `Employee`, `Loyalty_Points`
- Nulls in `Rating`, `Quantity`, `Unit_Price` etc.
- Decimal values where whole numbers were expected

---

### 🐍 Data Cleaning Process - Using Python

**Tools Used:** `Python`, `Pandas`, `dateutil.parser`, `Excel`

The entire cleaning logic is in `Coffee-Shop-Cleaning-Code.py`. Here's what I did:

**1. Column Removal:**
```python
cols_to_remove = ['Delivery_Minutes', 'Tax_5%', 'Coupon_Code', 'Feedback', 'Employee', 'Loyalty_Points']
```
Kept only business-critical columns.

**2. Null Handling:**
- Dropped rows where `Customer_Name` or `Gender` was null (cannot impute identity)
- `Rating` -> filled with mean rating
- All other remaining nulls -> filled with **mode** (most frequent value)

**3. Customer Type Standardization:**
```python
walk_in / walk-in / walk in / walkin -> New
```
Case-insensitive mapping.

**4. Robust Date Parsing:**
Used `dateutil.parser` with both `dayfirst=True/False` to handle all formats:
```
2025-01-02 21:51:00 -> 02-01-25
19 Aug 2025 16:18 -> 19-08-25
2024/02/25 13:09 -> 25-02-24
```
Filtered valid years 2020-2026 and standardized to `dd-mm-yy`.

**5. Whole Number Conversion:**
Converted to integers: `Rating`, `Discount_Amount`, `Total_Amount`, `Quantity`, `Unit_Price`

**6. Gender Correction with Name Mapping:**
Created a name-based dictionary to fix mislabeled genders:
```python
GENDER_MAP = {
 "Keerthi": "Female", "Priya": "Female", "Sanjay": "Male", ...
}
```
This fixed errors like Keerthi=Male, Sanjay=Female observed in raw data.

**7. Sorting & Proper Case:**
- Sorted by `Order_ID` ascending
- Converted all categorical text to Proper Case: `Chennai`, `Triplicane`, `Beverage`, `Credit Card`, `Dine In`

**8. New Calculated Columns:**
```python
Total_Sales = Quantity * Unit_Price
Payment_Amount = Total_Sales - Discount_Amount
```
This replaced the inconsistent `Total_Amount` column.

**Result:** 50,580 → 48,661 clean rows, 20 columns, 0 nulls.

---

### 📊 Power BI Dashboard - Coffee Shop Sales Overview

Built in **Power BI Desktop** using the cleaned Excel file.

#### KPIs (Top Row):
- **15K Total Orders**
- **11K Total Customers**
- **4M Total Sales**
- **4.16 Average Rating**
- **3.92M Total Profit** (calculated via DAX)
- **8.15 Average Discount %**

#### Visuals Included:
1.  **Monthly Sales (Line Chart):** Shows sales trend from September to February - downward trend observed, highest in Sep-Oct.
2.  **Total Sales by Payment_Method (Bar):** UPI and Credit Card dominate (~1M each), followed by Cash & Debit Card, Wallet & Paytm least used.
3.  **Total Quantity by Category:** Beverage (15K+) sells more than Food (10K).
4.  **Total Sales by Gender (Donut):** Male 51.52% vs Female 47.13% vs Other 1.35%
5.  **Total Sales by Customer_Segment (Funnel):** New (2M) > Member (1M) > Regular (1M) - New customers drive max revenue.
6.  **Total Sales by Month (Bar):** September highest, February lowest.

#### Filters/Slicers:
- Year: 2023, 2024, 2025
- Branch: All branches
- Payment Method: Cash, Credit Card, Debit Card, Paytm, Upi, Wallet

Dashboard theme uses coffee-brown palette for brand consistency.

---

### 🛠️ Tech Stack

- **Data Cleaning:** Python, Pandas, NumPy, dateutil
- **Visualization:** Power BI (DAX, Power Query)
- **Data:** 50K+ Coffee Shop Sales Records

### ▶️ How to Run

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install pandas python-dateutil openpyxl
   ```
3. Run the cleaning script:
   ```bash
   python Coffee-Shop-Cleaning-Code.py
   ```
4. Open `Coffee-Shop-Cleaned-Strict-Mode-Filled_1.xlsx` in Power BI and load.

### 💡 Key Insights from Dashboard

- UPI is the preferred payment method in Chennai region.
- Beverage category is the volume driver.
- 2025 data shows peak performance in festive months (Sep-Oct).
- New customers contribute ~50% of total sales - strong acquisition but need retention strategy.
- Average rating 4.16 indicates good satisfaction despite high discounting (8.15% avg).

### 🚀 Future Improvements

- Add DAX measures for Profit %, YoY Growth
- Branch-wise profitability analysis
- RFM analysis for customer segmentation
- Forecast next quarter sales using Python

---

### 👤 Author
**Y Mohammed Arish** - Data Analyst Enthusiast
- Cleaned messy real-world dataset with Python
- Visualized insights with Power BI

If you found this useful, ⭐ star the repo!

---
*This README was generated for GitHub portfolio upload.*
