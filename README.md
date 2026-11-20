# NIGHTFANG

A modular, autonomous security capability pack for **Hermes** — transforms your host runtime into an advanced, continuous penetration testing and vulnerability hunting engine. Deploy via Telegram, Discord, Web UI, or CLI.

```
Python ≥3.9   │   Hermes Agent   │   MITRE ATT&CK Mapping   │   SOP-05 Compliant
```

---

## Quick Start

```powershell
git clone https://github.com/mshrinath/nightfang.git
cd nightfang
.\install\install.ps1              # Windows
./install/install.sh               # Linux / macOS
nightfang.cmd --test               # Verify installation
```

Once connected, the operator interface lives in your Hermes channel:

| Command | Description |
| :--- | :--- |
| `/hunt <target>` | Seed target; launch autonomous hunting loop |
| `/queue` | View pending tasks, completed jobs, HITL approvals |
| `/autonomy [tier]` | Check or switch: `reactive` · `semi_autonomous` · `full_autonomous` |
| `approve <REQ_ID>` | Authorise exploit PoC (`/go <id>` is alias) |
| `deny <REQ_ID>` | Cancel exploit PoC (`/hold <id>` is alias) |
| `/scope [view\|set <t>]` | Inspect or update authorised targets |
| `/findings` | Table of discovered vulnerabilities |
| `/report [executive\|full]` | Generate markdown deliverable |
| `/stop` | Emergency halt for all active scans |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Host Runtime (Hermes)                    │
│          Model Selection · Token Efficiency · Scheduling        │
│          Long-Term Memory · Channel Adaptors                    │
├───────────┬───────────┬───────────┬─────────────────────────────┤
│ Telegram  │  Discord  │    CLI    │       Web UI                │
└───────────┴───────────┴───────────┴─────────────────────────────┘
                            │ manifest.yaml load
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NIGHTFANG Capability Pack                  │
│                     Security Orchestration Layer                │
├───────────────────┬───────────────────┬─────────────────────────┤
│     Agents        │      Skills        │        Workflows         │
│   46 specialists   │     42 domains     │       26 playbooks      │
│   (entrypoint+dele)│ (loaded on-demand) │  (modular execution)    │
├───────────────────┴───────────────────┴─────────────────────────┤
│               Autonomous Hunter Engine Daemon                   │
│   PriorityDAG Queue · Recursive Lead Gen · Self-Healing Backoff │
│   Execution Policy Gateway (6-stage verification)               │
│   Container / Subprocess Sandbox Isolation                      │
└────────────────────────────────────────────┬────────────────────┘
                                             │ findings.json
                                             ▼
                              ┌──────────────────────────┐
                              │ Shared Finding Schema     │
                              │ schemas/finding.md        │
                              │ CVSS v4.0 · ATT&CK mapped │
                              └──────────────────────────┘
```

Authorization / Scope Gate and Execution Policy Gateway are enforced at runtime — not conceptual labels. No capability routes unless both gates pass.

---

## Autonomous Execution Core

NIGHTFANG eliminates turn-by-turn halts through four subsystems:

1. **PriorityDAG Lead Queue** — DAG-managed task heap (`CRITICAL` > `HIGH` > `MEDIUM` > `LOW` > `INFORMATIONAL`). Prerequisite scans auto-unblock downstream validation.
2. **Recursive Lead Generator** — Reconnaissance output continuously parsed for subdomains, HTTP endpoints, API schemas, and open ports; feeds downstream specialists without manual prompting.
3. **Self-Healing Reflection** — Real-time handling of HTTP `429`, `503`, WAF triggers: pause traffic 30 s, halve rate ceilings, exponential-backoff re-queue.
4. **Non-Blocking Asynchronous HITL Queue** — Exploit PoCs requiring approval suspend into `hitl_queue.json` while the daemon continues scanning other targets in parallel.

### Autonomy Tiers ("Traffic Light" Model)

Set in `adapters/hermes/config.yaml` or toggled live via `/autonomy`:

| Tier | Behaviour |
| :--- | :--- |
| **REACTIVE** | Halts on every active probe (`MODERATE` / `LOUD`) for explicit confirmation. |
| **SEMI_AUTONOMOUS** *(default)* | Auto-runs GREEN (passive OSINT) and YELLOW (scanning/crawling). Emits non-blocking cards only for RED (exploit PoCs). |
| **FULL_AUTONOMOUS** | Auto-runs GREEN + YELLOW + safe non-destructive RED PoCs within scope, guarded by SOP-05 destructive filter. |

---

## Operator Interface & Approval Protocol

When an invasive action requires approval, NIGHTFANG emits a structured card for the active channel:

````
⚠️ [HITL APPROVAL GATE]
Target: api.target.corp
Tool:   sqlmap (Noise: LOUD)
Technique: SQL Injection Verification
Command: sqlmap -u "https://api.target.corp/v1/user?id=1" --batch
Action: [ APPROVE ] or [ DENY ]
Reply: approve REQ-9a3b8c
       deny    REQ-9a3b8c
````

- **Approve** → `approve REQ-<id>` (or `/go REQ-<id>`): gateway mints a 5-D unforgeable token and dispatches immediately.
- **Deny** → `deny REQ-<id>` (or `/hold REQ-<id>`): action aborted, recorded as unvalidated candidate.
- **Non-blocking**: hunter keeps discovering assets in the background while awaiting your response.

---

## Capabilities at a Glance

| Metric | Count |
| :--- | ---: |
| Agents (total) | 46 |
| ├ Direct entrypoint agents | 27 |
| └ Delegated specialist agents | 19 |
| Skill domains | 42 |
| Python scripts (all skills) | 72 |
| Execution workflows | 26 |
| Automated tests | 67 PASS |

---

## 46 Specialized Agents

### Direct Entrypoint Agents (27)

Cover all registered capabilities from `manifest.yaml`.

| Agent | Focus Area |
| :--- | :--- |
| `supervisor` | Dynamic orchestration, recursive decomposition, loop prevention |
| `recon` | Domain enumeration, WHOIS/DNS OSINT, attack-surface mapping |
| `scanner` | Web vuln analysis, API discovery, network port/service scan |
| `validation` | Benign PoC verification, 5-D HITL token enforcement |
| `reporter` | Executive deliverable compilation, risk communication |
| `cloud-security` | Multi-cloud IAM, storage permissions, IMDS SSRF audits |
| `container-breakout` | Container escapes, Kubernetes RBAC audits |
| `cicd-redteam` | Pipeline poisoning, runner isolation, secrets exposure |
| `ad-attacker` | AD enumeration, Kerberoasting, ADCS cert-template abuse |
| `wireless-pentester` | 802.11 WiFi, BLE GATT, RF protocol analysis |
| `mobile-pentester` | Android/iOS static/dynamic assessment (OWASP MASVS) |
| `iot-pentester` | Firmware extraction, hardware-bus debugging (UART/JTAG/SPI) |
| `scada-attacker` | ICS/SCADA and OT testing (Modbus, S7comm, IEC 62443) |
| `crypto-analyzer` | Crypto protocol auditing, TLS verification, JWT manipulation |
| `privesc-advisor` | Host privilege escalation (Linux SUID/caps & Windows LSASS/DPAPI) |
| `lateral-movement` | Internal pivoting, PtH, WMI/WinRM, data exfiltration |
| `forensics-analyst` | Volatility3 triage, artifact timelines, IR artefacts |
| `supply-chain-auditor` | SBOM generation (CycloneDX/SPDX), dependency confusion |
| `compliance-mapper` | NIST CSF 2.0, ISO 27001, SOC 2, PCI-DSS, CIS Controls |
| `cti-analyst` | Diamond Model attribution, STIX 2.1 IOC extraction |
| `purple-team-operator` | ATT&CK matrix emulation, defensive tuning loops |
| `ai-security` | Adversarial LLM tests, prompt injection, MCP auditing |
| `engagement-planner` | Scope boundaries, ROE validation, schedule planning |
| `evasion-specialist` | AMSI/ETW bypass analysis, EDR resilience evaluation |
| `c2-operator` | Covert C2 simulation, malleable profiles, egress analysis |
| `reverse-engineer` | Binary disassembly, decompilation, proprietary protocol RE |
| `database-attacker` | Relational/NoSQL security, privilege escalation, injection audit |
| `social-engineer` | Authenticated phishing templates, credential-harvest sim |

### Delegated Specialist Agents (19)

Invoked downstream by workflows or primary agents for lifecycle sub-tasks:

`detection-engineer` · `threat-modeler` · `code-auditor` · `risk-scorer` · `fix-verifier` · `malware-analyst` · `payload-crafter` · `traffic-analyzer` · `opsec-anonymizer` · `protocol-pentester` · `bug-bounty-agent` · `blue-team-agent` · `deception-agent` · `api-fuzzer` · `firmware-analyst` · `webshell-detector` · `zero-day-analyzer` · `config-drift-agent`

---

## 42 Security Skills

Each skill lives under `skills/<domain>/` and loads on demand. All scripts are read-only, passive analyzers or forensic collectors — no active exploitation.

```
active-directory   ai-security       api              attack-chain
bluetooth          c2-operations      cicd             cloud
coap               container          credential-access crypto
cti                defense-evasion    detection-engineering forensics
fuzzing-engine     grc                hunting           initial-access
iot                mobile             mqtt              network
osint              ot-ics             phishing          post-exploitation
privilege-escalation purple-team     recon            remediation
reporting          reverse-engineering secure-code-review supply-chain
supply-chain-registry threat-emulation utility
web                wireless
```

Total Python scripts across all skills: **72**.

---

## 26 Execution Workflows

Located in `workflows/`; each is a reusable playbook governing multi-agent task sequencing:

1. `dynamic-supervision.md` — Adaptive sense-plan-act-reflect loop (core orchestrator)
2. `standard-pentest.md` — Full 10-phase enterprise penetration test
3. `web-assessment.md` — Dedicated web application assessment
4. `api-assessment.md` — REST, GraphQL, gRPC security audit
5. `cloud-assessment.md` — Multi-cloud, container, and K8s audit
6. `ad-assessment.md` — Active Directory, Kerberos, ADCS audit
7. `ai-security-assessment.md` — LLM, agentic tool-use, MCP server eval
8. `purple-team.md` — Adversary emulation + detection engineering cycle
9. `cicd-assessment.md` — CI/CD pipeline and supply-chain build security
10. `mobile-assessment.md` — Android/iOS assessment (MASVS)
11. `wireless-assessment.md` — 802.11 WiFi, BLE, RF auditing
12. `iot-ics-assessment.md` — Safety-first IoT and OT/ICS testing
13. `supply-chain-assessment.md` — SBOM and dependency audit
14. `bug-bounty.md` — Fast-paced vulnerability hunting on web/API
15. `red-team.md` — Full-scope adversary simulation and covert egress
16. `reverse-engineering.md` — Binary analysis and protocol RE
17. `social-engineering.md` — Authorized phishing and awareness assessment
18. `thick-client-assessment.md` — Desktop/client binary review
19. `secure-code-review.md` — Static code review methodology
20. `devsecops-pipeline-review.md` — Secure SDLC integration
21. `firewall-assessment.md` — Firewall rule and policy audit
22. `threat-modeling.md` — STRIDE/LINDDUN pre-engagement modelling
23. `configuration-review.md` — Host and service hardening baseline
24. `osint-collection.md` — Open-source intelligence gathering
25. `forensic-investigation.md` — Incident-response artefact collection
26. `blockchain-assessment.md` — Smart-contract and chain analysis

---

## Automated Verification Suite

Built-in self-tests cover all core subsystems (no external test frameworks required):

```powershell
.\nightfang.cmd --test
# Ran 67 tests in X.XXXs — OK
```

| Suite | File | Coverage |
| :--- | :--- | :--- |
| **Execution Policy Gateway** | `tools/gateway.py` | 9 tests — scope checks, OPSEC enforcement, emergency stop, rate injection, 5-D HITL token validation, destructive payload filtering, rate ceilings |
| **Autonomous Hunter Daemon** | `tools/daemon.py` | 5 tests — priority queue ordering, semi-autonomous execution, non-blocking HITL queueing, token resumption, self-healing backoff |
| **Finding Schema Validator** | `schemas/validator.py` | 2 tests — valid finding acceptance + rejection of malformed records (CVSS v4.0 vector rules, evidence grounding, EPSS confidence consistency) |
| **Sandbox Runner** | `tools/sandbox.py` | 2 tests — subprocess fallback, process containment, timeout termination |

Full corpus regression under `tests/corpus/` validates against every schema violation branch.

---

## Repository Map

```
nightfang/
├── adapters/          # Hermes integration adapters
├── agents/            # 46 agent persona definitions (.md)
├── install/           # One-click installers (Windows/macOS/Linux)
├── integration/       # Integration test fixtures
├── references/        # Payloads index, SOP docs, ATT&CK mappings
├── schemas/           # Finding schema + JSON validator
├── skills/            # 42 skill domains (72 Python scripts total)
├── templates/         # Report and deliverable templates
├── tools/             # Runtime core: gateway, daemon, sandbox, auto_update
├── workflows/         # 26 execution playbooks
├── scripts/           # CLI entrypoint helpers
├── AGENTS.md          # Comprehensive agent taxonomy reference
├── PLAN.md            # Project roadmap
└── README.md          # This file
```

---

## References

- [MITRE ATT&CK](https://attack.mitre.org/) — technique mapping throughout findings
- [OWASP Top 10 / ASVS](https://owasp.org/www-project-application-verification-standard-guide/) — coverage guide
- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final) — technical security testing guide
- [PentestingEverything](https://github.com/m14r41/PentestingEverything) — methodological baseline
- [CWE / CVE](https://cwe.mitre.org/) — vulnerability classification used in reporting
- [EPSS](https://www.first.org/epss/) — exploit prediction scoring feed integrated in risk scoring

---

*Built for Hermes Agent · MIT license · 67 automated tests passing*
