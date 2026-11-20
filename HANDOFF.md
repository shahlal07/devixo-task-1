# HANDOFF.md — Brief for Incoming Agents

Paste this file into any new agent session (ChatGPT, Claude, Gemini) to bring it up to
speed. It is self-contained: the repository is private, so an agent that cannot read it
should be given this text directly.

---

## 1. What this project is

Two connected objectives, owned by **Shahlal Jaffir** (GitHub `shahlal07`):

1. **Devixo Solutions AI/ML Internship** — assignments, currently Task 01.
2. **Devixo Cyber Red-Team AI** — a long-term authorised security-research agent project.

This repository (`shahlal07/devixo-workspace`, private) is the **working bridge** between
the owner and AI agents. It is deliberately **not** a submission repo.

## 2. What is already done

**Task 01 — Python Programming, Data Analysis & Visualization. Status: complete.**

Dataset: UCI **Phishing Websites** (Mohammad & McCluskey, 2012), DOI `10.24432/C51W2X`,
CC BY 4.0, Kaggle mirror `akashkr/phishing-website-dataset`. 11,055 × 31.

| Deliverable | Path |
|---|---|
| Notebook (94 cells, 33 code) | `Task-01-Cybersecurity-EDA/notebooks/Devixo_Task_01_Cybersecurity_EDA.ipynb` |
| Dataset (782 KB) | `Task-01-Cybersecurity-EDA/data/phishing_dataset.csv` |
| 10 required charts | `Task-01-Cybersecurity-EDA/visualizations/` |
| 10 screenshots | `Task-01-Cybersecurity-EDA/screenshots/` |
| PDF report (29 pages) | `Task-01-Cybersecurity-EDA/reports/Shahlal_Jaffir_Task1.pdf` |
| Extracted rubric | `Task-01-Cybersecurity-EDA/ASSIGNMENT-REQUIREMENTS.md` |
| Report generator | `Task-01-Cybersecurity-EDA/build_report.py` |

The notebook was **executed end-to-end in Kali WSL**: 33/33 code cells, 0 errors, 10 figures
saved. All reported numbers come from that run.

## 3. Verified numbers — do not re-derive

| Metric | Value |
|---|---|
| Raw shape | 11,055 × 31 |
| Missing cells | 0 of 342,705 |
| Duplicates | 5,206 (47.09%) → 5,849 unique |
| Balance raw | 44.31% phishing / 55.69% legitimate |
| Balance clean | 51.62% / 48.38% |
| Duplicates removed | 1,879 phishing / 3,327 legitimate |
| Target | binary only (−1 / 1); no "suspicious" class |

Top correlations with class: `SSLfinal_State` 0.693 · `URL_of_Anchor` 0.679 ·
`Prefix_Suffix` 0.381 · `having_Sub_Domain` 0.296 · `web_traffic` 0.282 · `SFH` 0.281.

18 of 30 features correlate below |r| = 0.10; 7 at |r| ≥ 0.24.

Key rates — `SSL_State = −1`: 61.7% of phishing vs 9.3% of legitimate.
`External_Anchor_URL = −1`: 65.7% vs 0.7%. `Has_Prefix_Suffix = −1`: 100% vs 75.2%.
Derived `Risk_Signals` mean: 10.50 phishing vs 8.10 legitimate (heavy overlap).

## 4. Decisions already made — do not re-litigate

1. **Phishing dataset chosen over Malicious URLs** because the rubric mandates scatter,
   line, pair and violin plots plus a heatmap; a URL-only dataset has no numeric columns
   and would fail 5 of the 10 required charts.
2. **Dataset committed to the repo** — rubric requires it; 782 KB; CC BY 4.0 allows it.
3. **Colab-first; no scientific install on Windows** — only ~10 GB free on the project
   drive. A Windows venv was attempted and deliberately abandoned.
4. **Execution happens in Kali WSL** (pandas/numpy/matplotlib preinstalled; only seaborn
   added, 1 MB).
5. **Screenshots are renders of the real executed cells**, not Colab UI captures.
6. **PDF built with HTML + headless Chrome** — no LaTeX/pandoc on the machine.
7. **This repo is a bridge, not a submission.**

## 5. What is pending

- Submission repo for Task 01 (public) — not created.
- Google Drive upload of the PDF, shared "Anyone with the link → Viewer".
- Both links pasted into the Devixo form. **Deadline 22 Nov 2026, 00:00 UTC.**
- PDF section 22 still shows `[GITHUB_REPOSITORY_URL]`.
- Roll number unknown — title page shows `—`.
- Cyber Red-Team AI: Stage 1 not started (no datasets, no models downloaded).

## 6. How to work here

- Read `STATE.md` first, then `AGENTS.md`.
- Work on `agent/<name>/<topic>`; never force-push `main`.
- Update `STATE.md` when you change something material.
- **Never fabricate results.** If you did not execute it, do not report a metric.
- Security testing only against owned/authorised/lab systems; no destructive or
  credential attacks autonomously.
- Do not install large packages or models on the owner's machine.

## 7. Environment facts

Windows 11 Pro · i5-8365U · 16 GB RAM · **Intel UHD 620, no CUDA** · ~10 GB free on E:.
Python 3.14.10 bare on Windows; Python 3.13.12 with pandas/numpy/matplotlib/seaborn in
Kali WSL. WSL also has nmap, nikto, sqlmap, ffuf, gobuster, john, hydra, msfconsole.
Heavy compute goes to Google Colab.
