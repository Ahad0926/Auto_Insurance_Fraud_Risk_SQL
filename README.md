# Auto Insurance Portfolio Risk Analysis (SQL-Based)

This project develops a SQL-powered risk scoring pipeline for an auto insurance portfolio using a synthetic dataset. The goal is to demonstrate SQL-first data modelling, risk flag creation, scoring logic, and risk-performance analysis. This project highlights how actuarial-style portfolio segmentation can be driven by SQL queries alone, transforming raw insurance data into actionable insights for fraud detection, underwriting, and pricing adjustments.

---

## Project Structure

- `datasets/`
  - `raw/`: Original Kaggle dataset (`Car_Insurance_Claim.csv`)
  - `processed/`: Cleaned, normalized CSVs split into:
    - `customers.csv`
    - `vehicles.csv`
    - `driving_history.csv`
    - `claims.csv`
  - `data_cleaning.ipynb`: Notebook to clean and split the raw data.

- `sql/`
  - `schema.sql`: SQL database schema (`CREATE TABLE` statements).
  - `risk_flags.sql`: Risk flag queries.
  - `risk_scoring.sql`: Combined risk scoring logic.
  - `risk_analysis.sql`: Exploratory risk and claim profiling queries.
  - `analytics.sql`: Portfolio performance and risk group summaries.

---

## Objectives

- Normalize an auto insurance claims dataset into a clean SQL database schema.
- Create risk factor flags using SQL logic to represent driver behaviour, demographics, and vehicle profiles.
- Calculate a risk score by summing binary risk flags for each customer.
- Analyze how risk scores correlate with actual claim-filing rates.
- Segment the portfolio into actionable risk tiers using only SQL.
- Provide descriptive and performance summaries for fraud detection and pricing teams.

---

## Data Sources

- [Kaggle: Car Insurance Data](https://www.kaggle.com/datasets/sagnik1511/car-insurance-data/data)
  - `Car_Insurance_Claim.csv`
- Cleaned and split into:
  - `customers.csv`
  - `vehicles.csv`
  - `driving_history.csv`
  - `claims.csv`

---

## Tools & Techniques

- MySQL Workbench for database design and queries.
- SQL techniques: `CASE WHEN`, `JOIN`, `GROUP BY`, Common Table Expressions (CTEs), and `CREATE VIEW`.
- Pandas for initial CSV cleaning and splitting.
- Modular query structure with reusable views for scoring.
- Risk thresholding informed by common insurance heuristics.

---

## Key Findings

| Risk Score | Total Customers | Claim Rate |
|------------|------------------|------------|
| 3+         | 304               | 63%        |
| 2          | 1,885             | 52%        |
| 1          | 3,071             | 27%        |
| 0          | 2,889             | 18%        |

- Customers with risk scores of 3 or higher had claim rates over three times higher than low-risk customers.
- Risk factors such as low credit score, DUIs, and high annual mileage with older vehicles strongly aligned with claim occurrence.
- Even basic SQL-driven risk scoring revealed clear segmentation of the insurance portfolio.

---

## Business Recommendations

- Use risk scores to flag high-risk customers for further claim investigation or pricing adjustments.
- Apply targeted fraud audits to customers with scores of 3+.
- Consider risk-based pricing adjustments for portfolios showing demographic or behavioural risk patterns.
- Use the SQL risk scoring pipeline as a low-overhead portfolio monitoring tool.

---

## How to Run the SQL Queries

1. Create the database schema using `sql/schema.sql`.
2. Import the four processed CSV files into their corresponding tables (`customers`, `vehicles`, `driving_history`, `claims`).
3. Run `risk_flags.sql` to generate the initial risk flag queries (optional for testing).
4. Run `risk_scoring.sql` to create the `risk_scores` view and calculate risk scores.
5. Run `risk_analysis.sql` for detailed segment profiling.
6. Execute queries from `analytics.sql` to generate portfolio summaries and risk group comparisons.

---

## Example Outputs

### Risk Score Correlation with Claim Rate

| risk_score | total_customers | total_claims | claim_rate |
|------------|------------------|--------------|------------|
|      4     |         1        |       0      |    0.00    |
|      3     |       303        |     191      |    0.63    |
|      2     |      1885        |     983      |    0.52    |
|      1     |      3071        |     836      |    0.27    |
|      0     |      2889        |     526      |    0.18    |

### High-Risk Customers

|    id    | risk_score | outcome |
|----------|------------|---------|
|  881409  |     4      |    0    |
|   54408  |     3      |    1    |
|   53008  |     3      |    1    |
|   3643   |     3      |    1    |
|   45797  |     3      |    1    |
|   25908  |     3      |    1    |
|   33610  |     3      |    1    |
