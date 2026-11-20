# Data — Task 01

## Committed dataset

| Field | Value |
|---|---|
| **File** | `phishing_dataset.csv` |
| **Size** | 800,203 bytes (≈ 782 KB) |
| **Shape** | 11,055 rows × 31 columns (30 features + `Result`) |
| **Format** | CSV, comma-separated, header row, integer values |
| **Encoding** | ASCII / UTF-8 compatible |
| **Missing values** | none (verified: 0 empty cells of 342,705) |
| **Value domain** | all features ∈ {-1, 0, 1}; `Result` ∈ {-1, 1} |
| **Duplicates** | 5,206 exact duplicate rows (removed during cleaning) |

## Provenance — verified 16 November 2026

| Field | Value |
|---|---|
| **Dataset name** | Phishing Websites |
| **Authors** | Rami M. Mohammad, Lee McCluskey (University of Huddersfield) |
| **Year** | 2012 (donated to UCI in 2015) |
| **Original repository** | UCI Machine Learning Repository, dataset ID 327 |
| **DOI** | [10.24432/C51W2X](https://doi.org/10.24432/C51W2X) |
| **Original file** | `Training Dataset.arff` (782.1 KB) inside `phishing+websites.zip` |
| **License** | **CC BY 4.0** — redistribution permitted with attribution |
| **Data origin** | PhishTank archive, MillerSmiles archive, Google search operators |
| **Task type** | Binary classification (phishing vs legitimate) |

**Kaggle mirrors** (the assignment requires a Kaggle dataset; these host the same data):

- `akashkr/phishing-website-dataset` — `dataset.csv`, 855 KB, column descriptions included
- `isatish/phishing-dataset-uci-ml-csv`
- `odixe0502/uci-phishing-websites-onehot` (one-hot encoded variant, 68 columns)

## How this CSV was produced

Converted from the official `Training Dataset.arff` in the UCI archive:

1. Downloaded `https://archive.ics.uci.edu/static/public/327/phishing+websites.zip` (1,011,184 bytes)
2. Read the `@attribute` declarations to build the header row
3. Copied the `@data` section verbatim

**No value was modified, dropped, reordered or imputed.** The conversion is a pure
format change (ARFF → CSV). Verification after conversion:

- 11,055 data rows — matches the documented instance count
- 31 attributes — matches 30 features + `Result`
- 0 empty cells
- All values within {-1, 0, 1}

## Attribution (required by CC BY 4.0)

> Mohammad, R. M., & McCluskey, L. (2012). *Phishing Websites* [Dataset].
> UCI Machine Learning Repository. https://doi.org/10.24432/C51W2X

## Acquisition instructions (if the CSV is unavailable)

```python
# Option A — the notebook's built-in fallback (no credentials needed)
# downloads the official UCI archive and parses the ARFF automatically.

# Option B — Kaggle API (upload kaggle.json to Colab first)
!pip install -q kaggle
!mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d akashkr/phishing-website-dataset -p /content/data --unzip
```

## Known characteristics (verified, not assumed)

| Check | Result |
|---|---|
| Duplicate rows | **5,206** (47.1%) — 2,637 duplicate groups |
| Class balance (raw) | 4,898 phishing (44.31%) / 6,157 legitimate (55.69%) |
| Class balance (deduplicated) | 3,019 phishing (51.62%) / 2,830 legitimate (48.38%) |
| Missing values | 0 |
| Out-of-range values | 0 |
| "Suspicious" (0) class in target | **absent** — target is binary |
| Columns with spelling errors | 3 (`Shortining_Service`, `Domain_registeration_length`, `popUpWidnow`) |

These facts are re-verified inside the notebook, so the documentation stays honest
if the data is ever replaced.
