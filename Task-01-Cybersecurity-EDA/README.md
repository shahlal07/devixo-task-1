# Task 01 — Python Programming, Data Analysis & Visualization

**Domain:** Cybersecurity
**Environment:** Jupyter Notebook (Python 3)
**Deadline:** 22 November 2026, 00:00 UTC (05:00 Pakistan Standard Time)
**Notebook:** [`notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb`](notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb)

## Objective

Perform a reproducible Exploratory Data Analysis (EDA) on the **UCI Phishing Websites dataset** using Python (Pandas, NumPy, Matplotlib, Seaborn). The analysis covers data validation, cleaning, statistical profiling, and visualization to identify key security features that differentiate phishing sites from legitimate ones.

## Dataset — UCI Phishing Websites

This dataset, donated by Mohammad & McCluskey (2012) to the UCI Machine Learning Repository (ID 327), contains 11,055 websites described by 30 rule-based security features. It is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

**DOI:** `10.24432/C51W2X`

| Verified fact | Value |
|---|---|
| **Shape** | 11,055 rows × 31 columns (30 features + `Class`) |
| **Missing values** | 0 of 342,705 cells |
| **Duplicate rows** | 5,206 (47.1%) repeated feature vectors |
| **Class balance** | 4,898 phishing (44.31%) / 6,157 legitimate (55.69%) |
| **Value domain** | features ∈ {-1,0,1}; target ∈ {-1,1} (binary) |

**Note on duplicates:** The dataset contains 5,206 rows that repeat a feature vector already present. Because the file lacks unique website identifiers, we cannot confirm if these represent redundant entries for the same website or different websites with identical security measurements. To remain scientifically defensible, the **primary analysis uses the full 11,055-row dataset**. A deduplicated subset (5,849 rows) is retained strictly for sensitivity analysis.

## Workflow

1.  **Data Loading:** Read `data/phishing_dataset.csv`.
2.  **Cleaning:** Rename 31 columns, audit for missing values (found: 0), and narrow data types to `int8` for efficiency.
3.  **Exploratory Data Analysis:** 
    *   Compute descriptive statistics (mean, median, mode, std).
    *   Derive `Risk_Signals` to visualize feature failure distributions.
    *   Generate 10 mandatory charts using Matplotlib/Seaborn.
4.  **Correlation Analysis:** Rank feature-to-class relationships using Pearson r.
5.  **Reporting:** Generate a 29-page PDF via `build_report.py` (HTML to headless Chrome).

## Deliverables

- `notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb`: Full EDA, cleaned and verified.
- `reports/Shahlal_Jaffir_Task1.pdf`: Final technical report.
- `visualizations/`: Generated PNG charts.
- `screenshots/`: Evidence of execution.
- `build_report.py`: Automated report generator.

## Author

Shahlal Jaffir — Devixo Solutions AI/ML Internship.
