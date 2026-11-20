# Roadmap — Devixo Cyber Red-Team AI

Ten-stage development plan. Each stage has an exit criterion; we do not start
the next stage until the previous one produces real, verifiable output.

## Stage 1 — Fundamentals & dataset understanding
- Study: networking basics, OWASP Top 10, CVE/NVD, CVSS
- Inventory candidate cybersecurity datasets (license + size checked first)
- **Exit:** `Research/cybersecurity/` notes + verified dataset shortlist

## Stage 2 — Dataset preparation
- Acquire small/medium datasets in Colab, profile, clean, document
- **Exit:** reproducible cleaning notebooks + dataset cards

## Stage 3 — Pretrained model experiments
- Test existing open models on security text tasks (classification, QA, summarization)
- Run in **Google Colab**; no multi-GB downloads locally
- **Exit:** experiment log with real metrics in `Research/model-experiments/`

## Stage 4 — Model evaluation for cyber reasoning
- Build a small labeled eval set (security questions, true/false vuln judgments)
- Compare candidates on accuracy, hallucination rate, refusal behavior
- **Exit:** evaluation table + chosen baseline model(s)

## Stage 5 — Lightweight fine-tuning (Colab)
- LoRA/QLoRA-style experiments on small models only
- **Exit:** fine-tuned checkpoint + before/after eval numbers

## Stage 6 — Tool-using agent architecture
- Planner → tool → observation loop with structured output
- Design: allow-list targets, human approval gates, audit logging
- **Exit:** architecture doc + minimal agent running on scripted tasks

## Stage 7 — Authorized tool integration
- Wrap safe, read-only tools first (DNS/HTTP recon, header checks, scanners in safe mode)
- Kali Linux on WSL2 provides tooling; agents call them only against authorized targets
- **Exit:** tool adapters with tests in `tests/`

## Stage 8 — Isolated lab evaluation
- Deliberately vulnerable local apps (e.g. DVWA-style labs) in WSL/VMs
- Measure: findings found, false positives, safety-rule violations (must be 0)
- **Exit:** lab evaluation report in `evaluation/`

## Stage 9 — Reliability, reporting, safety hardening
- Improve reasoning traces, severity scoring, report generation
- Adversarial testing of the agent's own safety boundaries
- **Exit:** safety test suite + report templates

## Stage 10 — Usable interface
- FastAPI + simple web UI for authorized assessments
- **Exit:** runnable app with auth and audit log

## Standing constraints
- Colab for anything heavy; local machine stays light
- No fabricated metrics — every number comes from a logged run
- Human approval for intrusive actions, always
