# Verified Assignment Requirements — Task 01

Source: `C:\Users\pc\Downloads\AIML 1.pdf` (18 pages) + `Submission_Guidelines.pdf` (2 pages)
Extracted: 16 November 2026. **This replaces guesswork — every item below is from the official document.**

---

## 1. Task identity

| Field | Value |
|---|---|
| Program | Devixo Solutions — AI/ML Internship Program |
| Task | Task 01 — Python Programming, Data Analysis & Visualization |
| Level | Beginner to Intermediate |
| Unlock | 15 Nov 2026, 12:00 AM UTC |
| Deadline | **22 Nov 2026, 12:00 AM UTC** (05:00 PKT) |
| Submission | Report (Google Drive link) + GitHub repository link |

## 2. Required technologies

- **Language:** Python 3.x
- **Environment:** Jupyter Notebook **or** Google Colab
- **Mandatory libraries:** Pandas, NumPy, Matplotlib, Seaborn
- **Optional:** Streamlit (bonus dashboard)

## 3. Dataset rules (Kaggle)

- **Minimum 500 rows**
- Multiple columns/features
- Numerical and/or categorical variables
- Suitable for statistical analysis and visualization
- Must allow meaningful findings
- "Do not simply download the dataset and submit it" — own analysis required

Suggested ideas in the PDF: Student Performance, Netflix, Titanic, Employee Salary,
House Price, Laptop, Customer Churn, Sales, E-Commerce, Movie, Used Cars, Hotel
Booking. **"You may select any suitable dataset"** → a cybersecurity dataset is allowed
provided it meets the rules above.

## 4. Required workflow

Dataset Selection → Data Loading → Data Understanding → Data Cleaning →
EDA → Statistical Analysis → Data Visualization → Insights & Findings →
Conclusion → Project Documentation → GitHub Organization

## 5. Part 1 — Data loading & understanding

1. Import Pandas, NumPy, Matplotlib, Seaborn
2. Load dataset into a DataFrame
3. Display **first 5**, **last 5**, and a **random sample**
4. `info()`-style analysis: number of rows, number of columns, column names,
   data types, non-null values, missing values
5. Display dataset shape
6. Classify columns into **numerical**, **categorical**, **date/time** (if any)
   and explain the importance of each type

## 6. Part 2 — Data cleaning & preprocessing

1. **Missing values:** per column → count **and percentage**
2. **Handle missing values:** mean / median / mode / forward fill / backward fill /
   drop rows / drop columns — *must justify the choice, must not remove data silently*
3. **Duplicates:** count → remove → verify removal
4. **Data types:** detect wrong types (numbers as text, dates as strings, wrong
   categories) → correct them
5. **Rename columns** where unclear (e.g. `Emp_Sal_2024` → `Employee_Salary`);
   names must be clear, meaningful, consistent, easy to understand
6. **Invalid values:** negative salary, unrealistic age, invalid categories,
   impossible dates → explain how handled
7. **Verify cleaned dataset:** missing values, duplicates, dtypes, shape, basic stats
   — with evidence in the notebook

## 7. Part 3 — EDA & statistics

Descriptive statistics required: **mean, median, mode, minimum, maximum, range,
standard deviation, variance**

- Mean with formula `Mean = Σx / n` + interpretation
- Median + why it beats the mean when outliers exist
- Mode (especially for categorical data)
- Standard deviation + interpretation of variation
- **Correlation matrix** for suitable numerical variables, coefficients in [-1, +1],
  explain the most important correlations

## 8. Part 4 — ⚠️ THE 10 REQUIRED VISUALIZATIONS (exact list)

1. **Histogram**
2. **Bar Chart**
3. **Pie Chart**
4. **Scatter Plot**
5. **Line Chart**
6. **Box Plot**
7. **Correlation Heatmap**
8. **Count Plot**
9. **Pair Plot**
10. **Violin Plot**

*"Create at least 10 different visualizations"* — more allowed if meaningful.

Every visualization must have: **clear title, x-axis label, y-axis label,
appropriate figure size, readable text, meaningful variables, proper formatting,
suitable chart type**.

For important charts, write an interpretation: what the graph represents, what
pattern is visible, what the result means, why it matters.

## 9. Part 5 — Insights

**At least 10 meaningful insights**, based on the actual dataset. Suggested angles:
highest/lowest performing category, most common category, average/max/min values,
trends, strong/weak correlations, outliers, distribution patterns, unexpected
findings, real-world implications.

Guiding questions (from the PDF): strongest relationship, highest/lowest average
category, most common category, significant outliers, positive/negative
relationships, greatest variation, major trend, unusual pattern, overall conclusion.

## 10. Part 6 — Conclusion

1–2 paragraphs summarising: dataset selected, its purpose, cleaning techniques,
EDA performed, statistical analysis, visualizations created, most important
findings, what was learned, real-world usefulness.

## 11. Bonus — Streamlit dashboard (optional, recommended)

Dataset overview, total records/columns, KPIs, filters, interactive charts,
summary statistics, correlation visualization, key insights.
Clean, interactive, easy to understand, properly labeled, connected to the dataset.

## 12. Recommended project structure (from PDF)

```
Task_01_AI_ML/
├── dataset/dataset.csv
├── notebook/Task_01_Data_Analysis.ipynb
├── images/visualization_01.png ...
├── report/Task_01_Report.pdf
├── app/app.py            (if Streamlit)
└── README.md
```

## 13. PDF report — 20 required sections

Title page must include: **Devixo Solutions, AI/ML Internship Program, Task 01,
Python Programming Data Analysis & Visualization, Student Name, Internship Domain,
Submission Date**.

1. Introduction
2. Objective
3. Dataset Name
4. Dataset Source
5. Dataset Description
6. Dataset Size
7. Features/Columns Description
8. Methodology
9. Data Loading
10. Data Cleaning
11. Exploratory Data Analysis
12. Statistical Analysis
13. Data Visualizations
14. **Code Screenshots**
15. **Output Screenshots**
16. **Graph Screenshots**
17. Major Findings
18. At Least 10 Insights
19. Conclusion
20. GitHub Repository Link

Formatting: professional, organised, no unnecessary blank space, no spelling
mistakes, supported by relevant screenshots, properly labelled, based on actual results.

## 14. GitHub repository must contain

Source code · Jupyter Notebook · **Dataset** · README.md · Visualization images ·
PDF Report · Streamlit app (if done)

README must explain: Project Title, Project Objective, Dataset Description,
Dataset Source, Technologies Used, Libraries Used, Project Workflow,
Major Findings, How to Run the Project, Student/Author Name.

## 15. Screenshots required

Code (loading, cleaning, EDA, statistical analysis, visualizations), outputs,
final results — clear, readable, relevant, properly placed, each demonstrating a
specific part of the work.

## 16. Submission guidelines (Submission_Guidelines.pdf)

Three deliverables:

1. **PDF report** — file name **`Name_RollNo_Task.pdf`** (e.g. `Ali_Khan_1234_Task1.pdf`)
   with sections: Title Page (task title, full name, roll number/ID, course/program,
   date), Introduction, Problem Statement, Tools and Technologies,
   Methodology/Implementation, Screenshots/Output (each with a caption),
   Challenges and Solutions, Conclusion, GitHub Link
2. **GitHub repo** — public, meaningful name (`task1-project-name`), contains all
   files + README.md
3. **Google Drive PDF** — sharing: **Anyone with the link → Viewer**

Both links pasted into the submission form. Final check: both links open in an
incognito window.

## 17. Completion standard (verbatim intent)

- Project must be your own work; do not copy another intern's project
- Do not submit code you do not understand
- Every graph and observation must be based on your selected dataset
- GitHub must contain actual project files; PDF must contain evidence of actual work
- Screenshots clear, readable, relevant
- Project organised professionally
- **Explain the analysis, not just display code and graphs**
- Be able to explain the project and methodology to a mentor

---

## ⚠️ Conflicts & risks identified

| # | Issue | Impact | Proposal |
|---|---|---|---|
| 1 | Assignment requires the **dataset inside the GitHub repo**, but our `.gitignore` excludes `data/*.csv` | Requirement breach if ignored | Decide after dataset choice: commit a compact dataset (GitHub allows < 100 MB/file) or commit a documented sample + full acquisition instructions |
| 2 | **Malicious URLs dataset** typically has only `URL` + `type` — no numeric features | **Cannot produce scatter, line, pair, violin, heatmap** meaningfully → fails 5 of 10 required charts | Either (a) use a phishing-website **feature** dataset (numeric columns ready-made), or (b) derive numeric URL features (length, dots, digits, special chars, path depth…) to enable all 10 charts |
| 3 | PDF says "minimum 500 rows"; a 651k-row dataset is fine but heavy for a repo | Repo size / GitHub limits | Sampling or feature-based smaller dataset solves this |
| 4 | Report needs student **name + roll number** for the title page and file naming | Cannot finalise report without it | User to supply |
