# Customer Shopping Behavior Analysis

## Project Overview

This project demonstrates an end-to-end data analytics workflow using Python, SQL, and Power BI. It analyzes customer shopping behavior to identify purchasing patterns, customer segments, and insights that can support better business decisions.

The project covers data cleaning, exploratory data analysis, SQL querying, dashboard development, and business reporting.

## Business Objectives

- Understand customer purchasing patterns and preferences.
- Analyze customer segments and shopping frequency.
- Explore relationships between discounts, promotions, and purchasing behavior.
- Develop interactive visualizations to communicate findings.
- Provide data-driven insights to support business decisions.

## Tools and Technologies

- **Python:** Data cleaning, transformation, and exploratory data analysis.
- **Pandas:** Data manipulation and analysis.
- **Matplotlib and Seaborn:** Data visualization.
- **MySQL:** Database storage and SQL analysis.
- **Power BI:** Interactive dashboard development.
- **Jupyter Notebook:** Python analysis environment.

## Project Files

| File | Description |
|---|---|
| `customer_shopping_behavior.csv` | Dataset used for the analysis |
| `customer trends cleaning.ipynb` | Python data cleaning and exploratory analysis |
| `customer-shopping-behavior.sql` | SQL queries for business analysis |
| `customer_behavior_dashboard.pbix` | Interactive Power BI dashboard |
| `Business Problem Document.pdf` | Business problem definition |
| `Customer Shopping Behavior Analysis.pdf` | Project report |
| `Customer-Shopping-Behavior-Analysis.pptx` | Project presentation |

## Project Workflow

### 1. Data Cleaning and Exploration

The Python notebook covers:

- Loading and inspecting the dataset.
- Checking for missing values and duplicate records.
- Handling missing values.
- Standardizing column names.
- Creating customer age groups.
- Converting shopping frequency into numerical day intervals.
- Preparing the data for further analysis.

### 2. SQL Analysis

The SQL script contains queries used to investigate customer shopping behavior and answer business questions.

The analysis can explore customer segments, purchase amounts, product categories, discounts, and shopping frequency.

### 3. Power BI Dashboard

The Power BI dashboard presents customer shopping insights through visualizations and summary metrics, helping users explore trends and compare customer groups.

Open `customer_behavior_dashboard.pbix` using Power BI Desktop.

### 4. Reporting and Presentation

The project report and presentation communicate the analysis, key findings, and potential business recommendations.

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

### Step 3: Run the notebook

Open `customer trends cleaning.ipynb` in Jupyter Notebook.

Ensure the dataset `customer_shopping_behavior.csv` is available at the path used in the notebook.

### Step 4: Configure MySQL

Install and start MySQL, then create the database required by the notebook.

Configure your database credentials using environment variables in a local `.env` file. Never commit `.env` or expose database passwords in notebooks.

Run the notebook cells in order to connect to MySQL and load the prepared data.

### Step 5: Run the SQL queries

Open `customer-shopping-behavior.sql` in MySQL Workbench or another compatible SQL client. Ensure the database and table exist before executing the queries.

### Step 6: Open the dashboard

Open `customer_behavior_dashboard.pbix` in Power BI Desktop. Configure the data source if necessary.

## Key Learning Outcomes

- Practical data cleaning and exploratory data analysis.
- Using SQL to investigate business questions.
- Connecting Python workflows with a relational database.
- Designing dashboards for communicating analytical insights.
- Translating data findings into business recommendations.

## About the Author

**Hassan Jumaa**

Data Analyst and Software Developer

LinkedIn: [Connect with me](https://www.linkedin.com/in/mrisa-juma-56a600416)

Thank you for exploring this project!