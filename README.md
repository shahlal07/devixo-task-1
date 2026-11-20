# Devixo — Internship & AI Red-Team Workspace

Workspace for the **Devixo AI/ML internship** assignments and the long-term
**Devixo Cyber Red-Team AI** research project.

## Repository layout

| Folder | Purpose |
|---|---|
| [`Task-01-Cybersecurity-EDA/`](Task-01-Cybersecurity-EDA/) | Assignment 01 — Python, data analysis & visualization (Malicious URLs dataset, Google Colab) |
| [`Cyber-Red-Team-AI/`](Cyber-Red-Team-AI/) | Long-term authorized red-team / security-assessment agent project |
| [`Research/`](Research/) | Reading notes, cybersecurity research, ML and model-experiment notes |
| [`environment/`](environment/) | Local environment setup documentation and audit records |

## Environment summary

- **OS:** Windows 11 Pro (x64) — Dell Latitude 5300, 16 GB RAM, Intel UHD 620 (no dGPU)
- **Python:** 3.14.10 (project virtual environment created lazily per task)
- **Git:** 2.55.0 + GitHub CLI 2.103.3
- **Editor:** VS Code 1.130 (`E:\Microsoft VS Code`, on user PATH)
- **WSL2:** Kali Linux (default) + Ubuntu 24.04 — security tooling
- **Cloud:** Google Colab for dataset processing, EDA, and any GPU work

## Safety policy (red-team project)

All active security testing is restricted to:

1. Systems we own
2. Explicitly authorized environments
3. Local virtual labs
4. Intentionally vulnerable training applications

**Never** run attacks against public IPs, real organizations, third-party
accounts, or any system without written permission. Destructive actions,
exploitation, credential attacks, persistence, and data exfiltration stay
outside autonomous operation and require explicit human approval.

## Storage policy

- No large datasets stored locally — keep them in Google Colab / cloud storage
- No multi-GB model downloads on this machine
- No local GPU training (integrated graphics only)
- Verify free disk space before any substantial install

## Git

Git repositories are initialized per sub-project only after review.
Commit history is written only with explicit approval.
