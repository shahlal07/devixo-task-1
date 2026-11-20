# STATE.md — Current Status

Last updated: **20 November 2026** · Owner: Shahlal Jaffir · GitHub: shahlal07

This is the single source of truth. Update it whenever something material changes.
Agents: read this before acting, and append to **Decisions** when you make one.

---

## Snapshot

| Area | Status |
|---|---|
| Task 01 (Phishing EDA) | **Complete and verified** — awaiting submission |
| Task 01 GitHub submission repo | **Not created** (deliberately separate from this repo) |
| Task 01 Google Drive upload | **Pending** (owner action) |
| Cyber Red-Team AI | Stage 0 — docs and roadmap only, no code |
| Research notes | Empty scaffolding |

---

## Task 01 — completed work

**Deliverables (all committed in this repo):**

| Artifact | Path | Detail |
|---|---|---|
| Notebook | `Task-01-Cybersecurity-EDA/notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb` | 94 cells (61 markdown / 33 code) |
| Dataset | `Task-01-Cybersecurity-EDA/data/phishing_dataset.csv` | 782 KB, CC BY 4.0 |
| Charts | `Task-01-Cybersecurity-EDA/visualizations/` | 10 PNGs, 1.2 MB |
| Screenshots | `Task-01-Cybersecurity-EDA/screenshots/` | 10 PNGs |
| PDF report | `Task-01-Cybersecurity-EDA/reports/Shahlal_Jaffir_Task1.pdf` | 29 pages, 2.0 MB |
| Rubric extract | `Task-01-Cybersecurity-EDA/ASSIGNMENT-REQUIREMENTS.md` | from the official PDF |
| Report generator | `Task-01-Cybersecurity-EDA/build_report.py` | HTML → headless Chrome → PDF |

**Execution status:** the notebook was executed end-to-end in Kali WSL — 33/33 code
cells, 0 errors, 10 figures saved. This is verified, not assumed.

---

## Verified numbers (do not re-derive — these come from an executed run)

Dataset: UCI Phishing Websites, Mohammad & McCluskey 2012, DOI `10.24432/C51W2X`,
CC BY 4.0. Kaggle mirror: `akashkr/phishing-website-dataset`.

| Metric | Value |
|---|---|
| Raw shape | 11,055 × 31 (30 features + `Result`) |
| Missing cells | 0 of 342,705 |
| Duplicate rows | 5,206 (47.09%) → 5,849 unique rows |
| Class balance (raw) | 4,898 phishing (44.31%) / 6,157 legitimate (55.69%) |
| Class balance (clean) | 3,019 phishing (51.62%) / 2,830 legitimate (48.38%) |
| Duplicates by class | 1,879 phishing / 3,327 legitimate removed |
| Target domain | `{-1, 1}` only — no "suspicious" class |

**Correlation with class (Pearson r):**

`SSLfinal_State` 0.693 · `URL_of_Anchor` 0.679 · `Prefix_Suffix` 0.381 ·
`having_Sub_Domain` 0.296 · `web_traffic` 0.282 · `SFH` 0.281 ·
`Links_in_tags` 0.244 · `Request_URL` 0.238 · `Domain_registeration_length` −0.219 ·
`Google_Index` 0.118 · `Statistical_report` 0.108 · `having_IP_Address` 0.105

18 of 30 features correlate below |r| = 0.10; 12 below 0.05; 7 at |r| ≥ 0.24.

**Key cross-tabs:**

| Feature condition | Phishing | Legitimate |
|---|---|---|
| `SSL_State = -1` | 61.7% | 9.3% |
| `External_Anchor_URL = -1` | 65.7% | 0.7% |
| `Has_Prefix_Suffix = -1` | 100.0% | 75.2% |
| `Web_Traffic = 1` | 32.5% | 65.7% |
| `RightClick_Disabled = 1` | 94.9% | 95.3% |

**Derived `Risk_Signals` (count of −1 codes):** phishing mean 10.50 / median 10 /
IQR 8–12 / max 25 · legitimate mean 8.10 / median 7 / IQR 6–11 / max 19.
Heavy overlap — 64.1% of phishing and 42.1% of legitimate fall in the 7–11 band.

---

## Decisions log

| # | Decision | Reason |
|---|---|---|
| 1 | Use **Phishing Websites** dataset, not Malicious URLs | The rubric mandates scatter, line, pair and violin plots plus a heatmap; the URL dataset has no numeric columns, so 5 of 10 required charts would be meaningless |
| 2 | Commit the dataset into the repo | Rubric requires the dataset in the repository; file is only 782 KB and CC BY 4.0 permits it |
| 3 | Colab-first, no Windows scientific install | Disk is tight (~10 GB free on E:) and a local install was slow; abandoned after attempt |
| 4 | Execute the notebook in **Kali WSL** instead | pandas/numpy/matplotlib already present; only seaborn (1 MB) added. Zero Windows footprint |
| 5 | Screenshots rendered from real executed cells | Genuine code and output; authentic Colab UI captures not available without owner's session |
| 6 | Report built via HTML + headless Chrome | No LaTeX/pandoc/wkhtmltopdf installed; Chrome is present and produces clean PDFs |
| 7 | This repo is a **workspace bridge**, not a submission repo | Owner requirement: keep submission artifacts separate from the working bridge |
| 8 | Prose edits go through the `humanize` skill | Installed `ccf/humanize` (commit `db51ff3`) to `~/.config/opencode/skills/humanize` with a local override section: preserve meaning/numbers, clear student-level academic English, invent nothing, **no detector-evasion tuning**. Edit prose in `build_report.py`, then rerun `--final`; never hand-edit the PDF |

---

## Pending work

**Task 01 (owner actions)**
1. Push the submission repo separately: `gh repo create task1-phishing-website-eda --public --source=Task-01-Cybersecurity-EDA --push` (needs the nested `.git` restored or a fresh init).
2. Upload `Shahlal_Jaffir_Task1.pdf` to Google Drive, share **Anyone with the link → Viewer**.
3. Paste both links into the Devixo form. Deadline **22 Nov 2026 00:00 UTC**.

**Cyber Red-Team AI**
- Stage 1 not started: cybersecurity fundamentals notes, dataset shortlist with licence and size checks.
- No models, no datasets downloaded. Do not start large downloads on this machine.

---

## Known gaps / risks

1. `reports/Shahlal_Jaffir_Task1.pdf` section 22 still contains `[GITHUB_REPOSITORY_URL]` — the submission repo does not exist yet.
2. Screenshots are renders, not Colab UI captures. Rubric asks for evidence of work; content is genuine but the interface differs.
3. Roll number is unknown — title page shows `—`.
4. Nested repo history: `Task-01-Cybersecurity-EDA/.git` was moved to `.git-backup-task01/` when this workspace repo was created. Restore it before pushing a standalone submission repo, or re-init there.

---

## Conventions for updating this file

- Keep it factual. No aspirations in the Snapshot table.
- Verified numbers must cite how they were produced (executed notebook, script, command).
- When correcting a number, say what it was before and why it changed.
