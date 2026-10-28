# Customer Shopping Behavior Analysis

**Uncovering insights from 3,900 customer transactions to guide strategic business decisions**

![Dashboard Screenshot](assets/Screenshot%202026-10-28%20191301.png)

---

## Project Overview

This project demonstrates an end-to-end data analytics workflow using Python, SQL, and Power BI. It analyzes customer shopping behavior to identify purchasing patterns, customer segments, and insights that can support better business decisions.

**Dataset:** 3,900 customer transactions across 18 fields, covering demographics, purchase details, and shopping behavior.

**Key Finding:** Subscribers spend less on average than non-subscribers ($59.49 vs $59.87), but Loyal customers (3+ previous purchases) make up 79.9% of the customer base — retention drives revenue.

---

## Business Objectives

- Understand customer purchasing patterns and preferences.
- Analyze customer segments and shopping frequency.
- Explore relationships between discounts, promotions, and purchasing behavior.
- Develop interactive visualizations to communicate findings.
- Provide data-driven insights to support business decisions.

---

## Tools and Technologies

- **Python:** Data cleaning, transformation, and exploratory data analysis.
- **Pandas:** Data manipulation and analysis.
- **Matplotlib and Seaborn:** Data visualization.
- **MySQL:** Database storage and SQL analysis.
- **Power BI:** Interactive dashboard development.
- **Jupyter Notebook:** Python analysis environment.

---

## Project Files

| File | Description |
|------|-------------|
| `data/customer_shopping_behavior.csv` | Raw dataset (3,900 rows, 18 columns) |
| `data/customer_shopping_behavior_cleaned.csv` | Cleaned dataset (regenerated from the notebook) |
| `notebook/customer trends cleaning.ipynb` | Python data cleaning and exploratory analysis |
| `sql/customer-shopping-behavior.sql` | 10 SQL queries for business analysis |
| `reports/Customer Shopping Behavior Analysis.pdf` | Full written report with findings |
| `reports/Customer-Shopping-Behavior-Analysis.pptx` | Project presentation |
| `dashboard/customer_behavior_dashboard.pbix` | Interactive Power BI dashboard |
| `assets/Screenshot 2026-10-28 191301.png` | Dashboard screenshot (featured above) |
| `Business Problem Document.pdf` | Business problem definition |

---

## Data Cleaning (Python/Pandas)

| Step | Action | Result |
|------|--------|--------|
| Missing values | 37 nulls in `Review Rating` filled with category median | 0 nulls remaining |
| Column names | Standardized to snake_case | 18 columns → 17 after drop |
| Feature: `age_group` | Quartile bins: Young Adults, Adult, Middle_aged, Senior | Created |
| Feature: `purchase_frequency_days` | Mapped from frequency text to days | Created |
| Redundant column | `promo_code_used` dropped (perfectly correlated with `discount_applied`) | Removed |
| Duplicates | 0 found | None removed |

---

## SQL Analysis — 10 Business Questions

| # | Question | Key Result |
|---|----------|------------|
| Q1 | Total revenue by gender | Male: $157,890 \| Female: $75,191 |
| Q2 | Discount customers above average spend | 839 customers (avg = $59.76) |
| Q3 | Top 5 products by review rating | Gloves 3.86, Sandals 3.84, Boots 3.82... |
| Q4 | Standard vs Express shipping avg purchase | Express: $60.48 \| Standard: $58.46 |
| Q5 | Subscribers vs non-subscribers | Subscribers: $59.49 avg \| Non-subscribers: $59.87 avg |
| Q6 | Top 5 products by discount rate | Hat 50%, Sneakers 49.66%, Coat 49.07%... |
| Q7 | Customer segments | Loyal: 3,116 \| Returning: 701 \| New: 83 |
| Q8 | Top 3 products per category | See SQL file for full results |
| Q9 | Repeat buyers (>5 purchases) by subscription | Non-subscribers: 2,518 \| Subscribers: 958 |
| Q10 | Revenue by age group | Young Adults: $62,143 \| Adult: $55,978 \| Middle_aged: $59,197 \| Senior: $55,763 |

See `sql/customer-shopping-behavior.sql` for the full query set.

---

## Data-Quality Gate — Interview Checks

These are the specific checks an interviewer may ask about. Be ready to answer each one:

| Check | What It Proves | Status |
|-------|---------------|--------|
| No duplicate rows | Data integrity verified before analysis | 0 duplicates found |
| No nulls after cleaning | All gaps filled intentionally | 0 nulls in cleaned data |
| Column names standardized | snake_case for MySQL/Power BI compatibility | All columns renamed |
| Missing values documented | 37 `Review Rating` nulls filled with category median | Documented in notebook |
| Redundant column removed | `promo_code_used` perfectly correlated with `discount_applied` | Dropped, justified |
| Feature engineering | `age_group` and `purchase_frequency_days` created | Both added |
| SQL query correctness | All 10 queries run and return expected results | Verified against data |
| Database connection | MySQL connection via `.env` credentials | Working |
| Dashboard connection | Power BI connects to cleaned dataset | Configured |

---

## Key Statistics (for interview prep)

| Metric | Value |
|--------|-------|
| Total rows | 3,900 |
| Unique customers | 3,900 |
| Columns (raw) | 18 |
| Columns (cleaned) | 17 |
| Missing values (raw) | 37 in `Review Rating` |
| Missing values (cleaned) | 0 |
| Average purchase amount | $59.76 |
| Male revenue | $157,890 |
| Female revenue | $75,191 |
| Subscriber avg spend | $59.49 |
| Non-subscriber avg spend | $59.87 |
| Loyal customers | 3,116 (79.9%) |
| Returning customers | 701 (18.0%) |
| New customers | 83 (2.1%) |
| Top discount product | Hat (50% discount rate) |

---

## How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/Riq-wq/Customer-Shopping-Behavior-Analysis.git
cd Customer-Shopping-Behavior-Analysis
```

### Step 2: Set up Python

Install Python and Jupyter Notebook, then install the required libraries:

```bash
pip install pandas matplotlib seaborn sqlalchemy pymysql python-dotenv
```

### Step 3: Configure MySQL

Install and start MySQL, then create the database `customer_analysis`.

Configure your database credentials using environment variables in a local `.env` file (see `.env.example`). Never commit `.env` or expose database passwords in notebooks.

### Step 4: Run the notebook

Open `notebook/customer trends cleaning.ipynb` in Jupyter Notebook and run all cells. The notebook:

1. Loads `data/customer_shopping_behavior.csv`
2. Cleans the data (fills nulls, standardizes columns, engineers features)
3. Saves `data/customer_shopping_behavior_cleaned.csv`
4. Loads the cleaned data into MySQL table `customer_shopping_behavior`

### Step 5: Run the SQL queries

Open `sql/customer-shopping-behavior.sql` in MySQL Workbench or another compatible SQL client. Ensure the database and table exist before executing the queries.

### Step 6: Open the dashboard

Open `dashboard/customer_behavior_dashboard.pbix` in Power BI Desktop. Configure the data source if necessary.

### Step 7: View the reports

Open `reports/Customer Shopping Behavior Analysis.pdf` for the full written report.

Open `reports/Customer-Shopping-Behavior-Analysis.pptx` for the presentation.

---

## Key Learning Outcomes

- Practical data cleaning and exploratory data analysis.
- Using SQL to investigate business questions.
- Connecting Python workflows with a relational database.
- Designing dashboards for communicating analytical insights.
- Translating data findings into business recommendations.

---

## About the Author

**Hassan Jumaa**

Data Analyst and Software Developer

LinkedIn: [Connect with me](https://www.linkedin.com/in/mrisa-juma-56a600416)

Thank you for exploring this project!
