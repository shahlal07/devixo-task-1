# Safety Methodology — Authorized Testing Only

This document defines the non-negotiable operating rules for the
Devixo Cyber Red-Team AI project.

## 1. Authorization boundary

Active testing may target **only**:

1. Systems we own
2. Environments where we hold explicit, documented permission
3. Local virtual labs (WSL2/VMs on this machine)
4. Intentionally vulnerable training applications

**Never** target: public IP addresses, real organizations, third-party
accounts, classmates'/colleagues' systems, or any system without permission.

Before any test, record: target, scope, owner, authorization evidence, date.

## 2. Action classes

| Class | Examples | Autonomy |
|---|---|---|
| **Read-only recon** | DNS lookup, HTTP header fetch, port scan of own lab | allowed with target allow-list |
| **Active scanning** | Vulnerability scanners, fuzzing | human approval per target |
| **Exploitation** | Payload delivery, exploit attempts | **manual only**, never autonomous |
| **Credential attacks** | Brute force, password spraying | **out of scope** for autonomous operation |
| **Persistence / exfiltration** | Backdoors, data staging | **out of scope** |
| **Destructive actions** | DoS, wiping, defacement | **strictly forbidden** |

## 3. Agent safety controls (design requirements)

- **Target allow-list** — the agent refuses any host not on the list
- **Human-in-the-loop** — intrusive actions pause for explicit approval
- **Read-only by default** — write actions are opt-in per session
- **Audit log** — every command, argument, and result is recorded
- **Rate limiting** — polite scanning, no flood behavior
- **Refusal tests** — the agent must decline out-of-scope requests; this is
  part of evaluation, not an edge case

## 4. Lab-only tooling policy

Tools live in `tools/` and run primarily in **Kali Linux (WSL2)**.
Tool adapters must:

1. Validate targets against the allow-list before execution
2. Use non-destructive flags by default
3. Capture stdout/stderr as evidence with timestamps
4. Time out and kill runaway processes

## 5. Data handling

- Evidence and reports may contain sensitive findings → treat as confidential
- Never commit credentials, exploit payloads for real systems, or raw
  customer-like data to Git
- Reports are written for the authorized owner only

## 6. Incident rule

If the agent ever touches an out-of-scope target: stop the session, log the
event, review the allow-list logic, and fix before continuing.
