# Environment Setup Documentation

## System audit — 16 November 2026 (read-only)

### Hardware

| Item | Value |
|---|---|
| Machine | Dell Latitude 5300 |
| OS | Windows 11 Pro, build 26200, x64 |
| CPU | Intel Core i5-8365U @ 1.60 GHz — 4 cores / 8 threads |
| RAM | 15.8 GB (≈4 GB free at audit time) |
| GPU | Intel UHD Graphics 620 — **no dedicated NVIDIA GPU** |
| Storage | 1 SSD (477 GB), 4 visible partitions + 5 hidden |

### Disk (all partitions on the same physical SSD)

| Drive | Total | Free | Notes |
|---|---|---|---|
| C: | 230.4 GB | 24.2 GB | OS + user profile; npm global ≈ 7.1 GB |
| D: | 86.8 GB | 7.8 GB | 91 % used |
| E: | 45.4 GB | 10.4 GB | **Project drive (`E:\Devixo`)** |
| H: | 87.1 GB | 4.3 GB | 95 % used — avoid |

Total free at audit: **≈ 46.7 GB**. No large downloads without approval.

### Tooling found

| Tool | Version | Notes |
|---|---|---|
| Python | 3.14.10 | user install, `pip 26.2.2`, no scientific packages yet |
| Git | 2.55.0 | global `user.name` / `user.email` configured |
| GitHub CLI (`gh`) | 2.103.3 | authenticated repo management available |
| Node / npm | 24.18.0 / 11.16.0 | 10 global packages |
| VS Code | 1.130.0 | `E:\Microsoft VS Code`, added to **user PATH** 2026-11-16 (backup: `C:\Users\pc\.vscode-path-backup-20261116-165001.txt`) |
| OpenCode | 2.1.4 | running from a test build folder in `Downloads` (consider reinstalling to a stable path) |
| WSL | 3.0.5 | WSL2 features enabled |
| Kali Linux | Rolling (default distro) | already has nmap, nikto, sqlmap, ffuf, gobuster, john, hydra, msfconsole, python3, git — 12 GB used |
| Ubuntu 24.04 | 24.04.5 LTS | exists, 5.6 GB used — left untouched |
| Docker Desktop | 29.7.2 | installed, daemon **not running** — not used by this project |

Not installed: `uv`, `conda`. Execution policy: `RemoteSigned` (default, unchanged).

### Assignment document

`AIML 1.pdf` **was not found** on this machine — official visualization
requirements and marking criteria still pending delivery.

## Setup actions performed

| Date | Action | Reversible? |
|---|---|---|
| 2026-11-16 | Created `E:\Devixo` directory tree (18 folders) | yes (delete folders) |
| 2026-11-16 | Wrote root + sub-project READMEs, `.gitignore`, `requirements.txt` | yes (version control) |
| 2026-11-16 | Appended `E:\Microsoft VS Code\bin` to **user** PATH | yes (restore backup file) |

## Pending

1. Deliver `AIML 1.pdf` → extract exact 10 visualization types + rubric
2. Create project virtual environment + install scientific stack
   (`numpy pandas matplotlib seaborn jupyter scipy` ≈ 500–600 MB)
3. Verify dataset on Kaggle (license, columns, class balance)
4. Build `Devixo_Task_01_Cybersecurity_EDA.ipynb`
5. `git init` per sub-project after review

## Rules for this machine

1. No unnecessary software installs; estimate size before installing
2. No multi-GB local models; no local GPU training
3. No large datasets locally — Colab/cloud only
4. No Docker/heavy infra unless demonstrably necessary
5. One Python environment per project — no duplicates
6. Ask before changing security settings, firewalls, execution policies, WSL config
7. Never delete or overwrite existing files/configs without backup + approval
