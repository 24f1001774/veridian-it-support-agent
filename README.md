# 🛡️ Veridian Corp — Autonomous IT Support Agent
### Built for AIONOS • Agentic AI Factory (Internal Service Agent Track)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-groq%2Fcompound--mini-orange?style=for-the-badge)](https://groq.com)
[![Architecture](https://img.shields.io/badge/Design-ReAct_Pattern-green?style=for-the-badge)](https://github.com)
[![Status](https://img.shields.io/badge/Evaluation-15%2F15_Benchmark_Passed-success?style=for-the-badge)](https://github.com)

---

## ⚡ Quickstart: How to Run the Project (Under 60 Seconds)

### Step 1: Navigate to the Agent Directory
```bash
cd it_service_agent
```

### Step 2: Install Dependencies & Run Streamlit
```bash
# Optional: Activate your virtual or conda environment
conda activate default  # or source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the interactive agent portal
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🎯 Executive Problem Statement
Enterprise IT helpdesks face high ticket volumes where simple issues (password resets, guest Wi-Fi passes, printer spooler restarts) slow down the resolution of critical security threats (phishing attempts) and policy-restricted requests (unapproved software, out-of-cycle laptop replacements, privileged admin access).

Standard chat bots hallucinate policies and lack compliance guardrails.

**The Veridian IT Support Agent** solves this by implementing an **Autonomous ReAct (Reason + Act) Agent** that:
1. **Strictly grounds all answers** in Veridian's corporate Knowledge Base (`KB-01` to `KB-10`), the Asset Management Policy, and ticketing queue history (`TK-1042` to `TK-1051`).
2. **Resolves policy conflicts**: Resolves the direct tension between `KB-03` (laptop replacement eligible after 3 years) and the `Asset Management Policy` (4-year refresh cycle requiring Finance sign-off).
3. **Escalates high-risk requests**: Immediately flags phishing (`KB-09`) with an alert *not to forward*, routes unapproved tools (`KB-04`) to IT Security, and requires justification for admin privileges (`TK-1050`).
4. **Clarifies ambiguous intent**: Proactively asks diagnostic questions for vague tickets (`REQ-15`) rather than guessing.
5. **Maintains a full audit trail**: Automatically records structured tickets with cited policy IDs and human escalation authorities.

---

## 🏗️ System Architecture & Modular Design

To maintain clean engineering standards and student-built readability, the codebase is partitioned into distinct single-responsibility modules:

```
it_service_agent/
├── config.py              # Environment configuration and model parameters
├── data_pack.py           # Ground truth Knowledge Base, 15 Employee Requests & Ticket Queue
├── policy_engine.py       # Deterministic rule engine & policy conflict resolver
├── tools.py               # IT Service tools (KB lookup, precedent check, ticket generation)
├── prompts.py             # System prompts and triage instructions
├── parser.py              # Action & JSON payload extractor
├── llm.py                 # LLM API connector with offline grounded fallback engine
├── agent.py               # Central ReAct orchestrator coordinating triage & decisions
├── memory.py              # Session history and persistent compliance audit trail
├── app.py                 # Streamlit UI (6 Tabs: Chat, Batch Triage, Precedents, KB Engine, Audit Trail, 10-Slide Deck)
├── requirements.txt       # Project dependencies
└── presentation_deck.md   # 10-Slide presentation deck (also rendered interactively in Tab 6 of app.py)
```

> **💡 Note for Evaluators**: The mandatory **10-Slide Presentation Deck** is built directly into the running Streamlit web app under **Tab 6 ("📊 10-Slide Presentation Deck")** with an interactive slide navigator, so you can present or review the slides without switching out of the prototype! It is also available as a standalone markdown document in `presentation_deck.md`.

---

## 📊 Complete Benchmark: All 15 Employee Requests (REQ-01 to REQ-15)

| Request ID | Employee | Issue Summary | Grounded Policy | Agent Decision | Escalated Team |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Aditi Sharma | Dead laptop, 3.5 yrs old | `KB-03`, `ASSET-POL` | **Escalated** (Early Replacement Approval) | Finance & IT Assets |
| **REQ-02** | Vikram Chawla | Guest Wi-Fi access tomorrow | `KB-07` | **Resolved** (Self-Service Kiosk Guide) | None (Self-Service) |
| **REQ-03** | Karan Mehta | Account locked out (6 attempts) | `KB-01` | **Resolved** (Manual IT Unlock Queued) | None (IT Helpdesk) |
| **REQ-04** | Ritu Bhatia | Non-catalog data analysis tool | `KB-04` | **Escalated** (Security Review 3–5 Days) | IT Security Review Queue |
| **REQ-05** | Sanjay Oberoi | VPN credentials expired | `KB-02` | **Resolved** (90-Day Renewal Guidance) | None (Self-Service) |
| **REQ-06** | Meera Iyer | Printer false paper jam (3rd Fl) | `KB-05` | **Resolved** (Spooler Restart / Dispatch) | None (Hardware Tech) |
| **REQ-07** | Farhan Ali | WFH 4 days/week, requests monitor | `KB-10` | **Escalated** (Manager & Finance Sign-off) | People Ops & Finance |
| **REQ-08** | Ananya Reddy | Phishing email received & forwarding | `KB-09` | **CRITICAL ESCALATION** (Stop Forwarding!) | IT Security (`security@...`) |
| **REQ-09** | Rohit Desai | Mailbox full, cannot send mail | `KB-06` | **Resolved** (Archive Guidance / Quota Cap) | None (Self-Service) |
| **REQ-10** | Kavya Pillai | Urgent admin access to Finance server | `KB-08`, `TK-1050` | **Escalated** (Privileged Access Review) | Finance Owner & Security |
| **REQ-11** | Nikhil Bansal | VPN access for new contractor | `KB-02` | **Resolved** (Access Request Form Guidance) | Employee's Manager |
| **REQ-12** | Sneha Kulkarni| Cannot log into expense tool | `KB-08` | **Resolved** (Finance Account Verification) | Finance / IT Helpdesk |
| **REQ-13** | Aman Gupta | Laptop screen flickering (2 yrs old) | `KB-03`, `ASSET-POL` | **Resolved** (Hardware Repair Ticket) | IT Hardware Support |
| **REQ-14** | Tanya Chopra | Browser extension for productivity | `KB-04` | **Escalated** (Security Review 3–5 Days) | IT Security Review Queue |
| **REQ-15** | Rahul Menon | "hey can you help, its not working" | `General Triage` | **Clarification Needed** (Diagnostic Qs) | Employee Follow-up |

---

## ⚖️ Key Edge Cases & Policy Reasoning

1. **The Laptop Replacement Dilemma (`REQ-01` vs `REQ-13`)**:
   - `KB-03` states laptops are eligible for replacement after 3 years.
   - However, the `Finance & Assets Management Policy` mandates a **4-year refresh cycle**, requiring Finance sign-off for any earlier replacement.
   - Following historical precedent **`TK-1043` (S. Iyer, 3.2 yrs old, approved pending fulfillment)**, the agent flags Aditi's 3.5-year-old laptop as requiring **Finance approval** in addition to IT fulfillment.
   - For Aman Gupta (`REQ-13`, 2 years old), the agent recognizes that the device is not eligible for replacement and correctly routes it for **screen repair**, saving company hardware capital.

2. **Security Threat Containment (`REQ-08`)**:
   - Ananya Reddy states she is forwarding a suspected phishing email to teammates.
   - The agent intervenes immediately with high urgency, ordering the employee **not to forward** (to prevent contagion) and escalating directly to `security@veridian-corp.example` under `KB-09`.

3. **Ambiguous Query Handling (`REQ-15`)**:
   - Rather than making assumptions, the agent asks 3 structured diagnostic questions: application/service affected, error messages observed, and asset tag.

---

## 🔒 Enterprise Compliance & Audit Trail
Every decision made by the agent generates a persistent audit entry stored in `it_service_agent/audit_trail.json`. Each entry includes:
- Timestamp
- Requesting Employee & Email
- Identified Policy IDs (`KB-XX`)
- Precedents Referenced (`TK-XXXX`)
- Action Decision (`Resolved` vs `Escalated` vs `Clarification Needed`)
- Escalation Authority (e.g. IT Security, Finance, Manager)
