# Task 01 — Python Programming, Data Analysis & Visualization

**Domain:** Cybersecurity
**Environment:** Google Colab
**Deadline:** 22 November 2026, 00:00 UTC (05:00 Pakistan Standard Time)
**Notebook:** [`notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb`](notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb)

## Objective

Perform a complete, reproducible Exploratory Data Analysis (EDA) on a
**Kaggle cybersecurity dataset** (target: Malicious URLs, ≥ 500 records)
using Python, Pandas, NumPy, Matplotlib and Seaborn — with all required
visualization types, evidence-based insights, a professional PDF report,
and a GitHub repository with a README.

## Requirements checklist

> ✅ **Verified against the official documents** — see
> [`ASSIGNMENT-REQUIREMENTS.md`](ASSIGNMENT-REQUIREMENTS.md) for the full extracted rubric.

**Data work**
- [ ] Python 3.x (Jupyter or Colab)
- [ ] Kaggle dataset, ≥ 500 rows, multiple columns, numeric and/or categorical
- [ ] Load + display head / tail / random sample
- [ ] Structure analysis: rows, columns, names, dtypes, non-null, missing
- [ ] Shape + column classification (numerical / categorical / datetime)
- [ ] Missing values: count **and percentage**, handled with justification
- [ ] Duplicates: counted, removed, verified
- [ ] Data types corrected where wrong
- [ ] Columns renamed where unclear
- [ ] Invalid values identified and handled
- [ ] Cleaned dataset verified with evidence

**Analysis**
- [ ] Descriptive stats: mean, median, mode, min, max, range, std, variance
- [ ] Mean formula + interpretation
- [ ] Median vs mean (outlier reasoning)
- [ ] Mode (categorical)
- [ ] Standard deviation interpretation
- [ ] Correlation matrix + interpretation

**10 required visualizations** (each with title, x/y labels, figure size, interpretation)
- [ ] 1. Histogram
- [ ] 2. Bar Chart
- [ ] 3. Pie Chart
- [ ] 4. Scatter Plot
- [ ] 5. Line Chart
- [ ] 6. Box Plot
- [ ] 7. Correlation Heatmap
- [ ] 8. Count Plot
- [ ] 9. Pair Plot
- [ ] 10. Violin Plot

**Deliverables**
- [ ] ≥ 10 evidence-based insights
- [ ] 1–2 paragraph conclusion
- [ ] PDF report with all 20 required sections + title page (name, roll no., domain, date)
- [ ] Code / output / graph screenshots
- [ ] Public GitHub repo with code, notebook, dataset, README, images, PDF
- [ ] README: title, objective, dataset description + source, technologies, libraries, workflow, findings, how to run, author
- [ ] Google Drive PDF, "Anyone with the link → Viewer"
- [ ] PDF named `Name_RollNo_Task.pdf`
- [ ] Streamlit dashboard *(bonus / recommended)*

## Structure

```
Task-01-Cybersecurity-EDA/
├── notebooks/          # Devixo_Task_01_Cybersecurity_EDA.ipynb
├── data/               # README only — datasets stay in Colab/cloud
├── reports/            # PDF report
├── visualizations/     # Generated charts (PNG, not committed)
├── screenshots/        # Notebook / report screenshots
└── README.md
```

## Dataset — verified

**Phishing Websites** (Mohammad & McCluskey, 2012) — UCI ML Repository ID 327,
DOI `10.24432/C51W2X`, **CC BY 4.0**. Kaggle mirrors: `akashkr/phishing-website-dataset`,
`isatish/phishing-dataset-uci-ml-csv`.

| Verified fact | Value |
|---|---|
| Shape | 11,055 rows × 31 columns (30 features + `Result`) |
| Missing values | **0** of 342,705 cells |
| Duplicate rows | **5,206** (47.1%) — removed in cleaning |
| Class balance (raw) | 4,898 phishing (44.31%) / 6,157 legitimate (55.69%) |
| Class balance (cleaned) | 3,019 phishing (51.62%) / 2,830 legitimate (48.38%) |
| Value domain | features ∈ {-1,0,1}; target ∈ {-1,1} (binary, no "suspicious" class) |
| File committed | `data/phishing_dataset.csv` (782 KB) |

Full provenance and conversion log: [`data/README.md`](data/README.md).

**Why this dataset:** the ten required chart types include scatter, line, pair and
violin plots plus a correlation heatmap — all of which need multiple numeric
columns. This dataset provides 30 numeric security features, so every required
chart is meaningful, while staying in the cybersecurity domain.

## Status

- [x] Workspace structure created (2026-11-16)
- [x] Official requirements extracted from `AIML 1.pdf` + `Submission_Guidelines.pdf`
- [x] Dataset verified and committed (CC BY 4.0, attribution retained)
- [x] Notebook written — 94 cells (61 markdown / 33 code), 0 syntax errors
- [x] Notebook auto-exports all 10 charts as PNG + ZIP (one-click in Colab)
- [x] Report generator written (`build_report.py`, HTML → headless Chrome → PDF)
- [x] Report **draft** generated — 16 pages, all 20+ sections, placeholders marked
- [x] Notebook executed end-to-end — 33/33 code cells, 0 errors
- [x] 10 visualizations generated (`visualizations/`, 1.2 MB)
- [x] 10 screenshots captured from the real executed cells (`screenshots/`)
- [x] Final report generated — `reports/Shahlal_Jaffir_Task1.pdf`, 29 pages, 2.1 MB
- [ ] GitHub repository published
- [ ] Google Drive PDF link set to "Anyone with the link"
