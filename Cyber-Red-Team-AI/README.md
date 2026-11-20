# Devixo Cyber Red-Team AI

An **authorized** security-research agent project: an AI system that can
reason about cybersecurity, assist with penetration testing and defensive
assessments, evaluate vulnerabilities, and produce technical reports —
within strict safety boundaries.

> ⚠️ **Authorization scope.** All active testing is limited to systems we
> own, explicitly authorized environments, local virtual labs, and
> intentionally vulnerable training applications. Never target public IPs,
> real organizations, third-party accounts, or any system without
> permission. Destructive actions, exploitation, credential attacks,
> persistence, and data exfiltration require explicit human approval and
> never run autonomously.

## Vision

1. Cybersecurity knowledge and reasoning
2. Network and service reconnaissance
3. Web application security assessment
4. Vulnerability identification (OWASP Top 10, CVE intelligence)
5. Safe security-tool orchestration
6. Evidence collection and severity assessment (CVSS-style)
7. Technical report generation and recommendations
8. Multi-step agent workflows

## Roadmap (stages)

| Stage | Focus | Status |
|---|---|---|
| 1 | Understand datasets + cybersecurity fundamentals | planned |
| 2 | Prepare & clean cybersecurity datasets | planned |
| 3 | Experiment with existing pretrained models | planned |
| 4 | Evaluate models for cybersecurity reasoning | planned |
| 5 | Lightweight fine-tuning experiments (Colab) | planned |
| 6 | Tool-using agent architecture | planned |
| 7 | Integrate authorized security assessment tools | planned |
| 8 | Evaluate in isolated cybersecurity labs | planned |
| 9 | Improve reasoning, reliability, reporting, safety | planned |
| 10 | Usable interface | planned |

Details: [`docs/ROADMAP.md`](docs/ROADMAP.md)

## Repository layout

```
Cyber-Red-Team-AI/
├── docs/           # architecture, safety methodology, research plans
├── datasets/       # README only — large data stays in Colab/cloud
├── notebooks/      # experiments
├── src/            # core library code
├── agents/         # agent definitions / workflows
├── tools/          # tool integrations (recon, scanning — authorized use only)
├── evaluation/     # benchmarks, scoring, red-team eval harness
├── tests/          # unit tests
└── requirements.txt
```

## Planned technology stack

Python, Pandas/NumPy, Scikit-learn, PyTorch / Hugging Face Transformers
(experimentation on Google Colab), FastAPI (later), Git/GitHub,
Kali Linux on WSL2 for authorized tooling.

**Not planned locally:** large model hosting, Docker sprawl, local GPU
training (this machine has integrated graphics only).

## Safety design principles

- Human-in-the-loop approval gates for intrusive actions
- Allow-list of targets (explicitly authorized hosts only)
- Read-only by default; write/exploit actions opt-in and logged
- Full audit trail of every command executed
- Refusal of scope-creep requests outside the authorization boundary

## Status

- [x] Workspace + documentation skeleton (2026-11-16)
- [ ] Stage 1 — dataset & fundamentals research
- [ ] Architecture design document
- [ ] First evaluation harness
