# AGENTS.md — Shared Workspace Protocol

This repository is the **working bridge** between the project owner and any AI agent
working on the Devixo internship and the Cyber Red-Team AI project.

It is **not** a submission repository. Submission happens separately (Google Drive
PDF + a dedicated public repo per task).

---

## Read this first

1. **`STATE.md`** — current status, verified numbers, decisions already made.
2. **`Task-01-Cybersecurity-EDA/ASSIGNMENT-REQUIREMENTS.md`** — the extracted official rubric.
3. The `README.md` in whichever folder you are about to touch.

Do not re-derive facts that `STATE.md` already records. If you believe a recorded fact
is wrong, verify it, then update `STATE.md` with the correction and the reason.

---

## Layout

```
Devixo/
├── STATE.md                      # single source of truth for current status
├── AGENTS.md                     # this file
├── README.md                     # workspace overview
├── environment/
│   └── setup-documentation.md    # machine audit, tooling, setup log
├── Task-01-Cybersecurity-EDA/    # internship assignment 01 (complete, local)
│   ├── ASSIGNMENT-REQUIREMENTS.md
│   ├── data/                     # dataset + provenance (committed, CC BY 4.0)
│   ├── notebooks/                # the deliverable notebook
│   ├── visualizations/           # 10 generated charts
│   ├── screenshots/              # 10 rendered evidence images
│   ├── reports/                  # final PDF report
│   └── build_report.py           # HTML → Chrome → PDF generator
├── Cyber-Red-Team-AI/            # long-term research project (docs only so far)
│   ├── docs/ROADMAP.md
│   ├── docs/SAFETY-METHODOLOGY.md
│   └── requirements.txt
└── Research/                     # notes: cybersecurity, ML, model experiments
```

---

## Conventions

**Writing**
- Markdown for docs, no proprietary formats unless the deliverable requires one.
- One topic per file. Cite sources with URL + access date.
- Never commit generated binaries you can rebuild from a script; commit the script.
- Keep files under a few MB. Datasets go in the cloud, not here.

**Commits**
- Imperative subject line, ≤ 72 chars: `Add X`, `Fix Y`, `Update Z`.
- Body: what changed and **why**. Reference the file or section affected.
- One logical change per commit. Do not mix unrelated work.
- Never commit secrets, tokens, `.env` files, or personal credentials.

**Branching (multi-agent work)**
- `main` is always readable and consistent.
- Work on `agent/<name>/<topic>`, e.g. `agent/chatgpt/redteam-arch`.
- Open a PR or leave a note in `STATE.md` describing the branch purpose.
- Rebase on `main` before pushing; do not force-push `main`.

---

## Safety rules (non-negotiable)

1. **Authorised testing only.** Security tooling may target systems we own, explicitly
   authorised environments, local virtual labs, or intentionally vulnerable training apps.
   Never public IPs, real organisations, or third-party accounts.
2. **No destructive or credential attacks** in autonomous operation. Human approval
   required for anything intrusive.
3. **No fabricated results.** Every metric, accuracy score or observation must come from
   an executed run. If you did not run it, do not report it as a result.
4. **Do not delete or overwrite** files you did not create without a backup and a note in
   `STATE.md`.
5. **Do not touch unrelated projects** on the owner's machine (other repos in
   `~/OneDrive/Documents/GitHub/`, `~/browser-control/`, etc.).
6. **Do not change system configuration** (PATH, WSL config, firewall, execution policy)
   without explicit approval.

---

## Environment facts

| Item | Value |
|---|---|
| Host | Windows 11 Pro, Dell Latitude 5300, i5-8365U, 16 GB RAM |
| GPU | Intel UHD 620 — **no CUDA**, no local training |
| Disk | 4 partitions, ~10 GB free on E: (project drive) — keep installs small |
| Python (Windows) | 3.14.10, bare (no scientific packages) |
| Python (Kali WSL) | 3.13.12 with pandas 2.3.3, numpy 2.3.5, matplotlib 3.10.7, seaborn 0.13.2 |
| WSL | Kali Linux (default) + Ubuntu 24.04; nmap, nikto, sqlmap, ffuf, gobuster, john, hydra, msfconsole installed |
| Editor | VS Code 1.130 at `E:\Microsoft VS Code` |
| Cloud | Google Colab is the designated heavy-compute environment |
| PDF toolchain | headless Chrome `--print-to-pdf` (no LaTeX/pandoc installed) |

**Practical rule:** execute notebooks in Kali WSL or Colab. Do not install a scientific
stack on Windows — it was tried and deliberately abandoned.

---

## How to verify work

```bash
# notebook executes clean (Kali)
cd /mnt/e/Devixo/Task-01-Cybersecurity-EDA
MPLBACKEND=Agg python3 <executor>        # see STATE.md for the current executor

# report rebuilds
python build_report.py --final           # Windows; needs Chrome

# repo health
git status --short && git log --oneline -5
```

Report results as observed output, not as intent.

---

## Current owner

GitHub: **shahlal07** · Internship: Devixo Solutions AI/ML · Domain: Cybersecurity.
