# 🛡️ Veridian Corp — Autonomous IT Support Agent
## 10-Slide Evaluation Presentation Deck

> **💡 Note for Evaluators**: This entire 10-slide deck is embedded and interactively viewable directly inside the running Streamlit prototype at `http://localhost:8501` under **Tab 6: "📊 10-Slide Presentation Deck"** with a live slide navigator!

---

### **Slide 1: Title & Executive Summary**
* **Project Title**: Veridian Corp Autonomous IT Support Agent
* **Subtitle**: Grounded Enterprise Triage, Policy Conflict Resolution, and Compliance Auditing
* **Track**: Agentic AI Factory — Assignment 2 (Internal Service Agent)
* **Candidate**: Sai Nayan Mamilla
* **Core Technology**: Hybrid ReAct Agent + Groq `openai/gpt-oss-120b` + Deterministic Policy Engine
* **Key Achievement**: 100% resolution accuracy across all 15 official test requests (`REQ-01` to `REQ-15`), zero hallucinated policies, deterministic conflict resolution, and automated audit logging.

---

### **Slide 2: The Enterprise Problem & Operational Bottlenecks**
* **The Problem**: IT service desks are flooded with tier-1 requests (password resets, Wi-Fi credentials, printer jams) that distract engineers from critical security threats and compliance audits.
* **Why Generic Chatbots Fail**:
  * Hallucinate policies or approve unapproved software.
  * Miss conflicting organizational rules across departments (e.g. IT policies vs Finance asset refresh cycles).
  * Fail to intervene in active security risks (e.g. employees forwarding phishing emails).
* **Our Mission**: Build an autonomous ReAct IT agent strictly bounded by corporate knowledge base policies (`KB-01` to `KB-10`), asset lifecycle mandates, and historical ticket precedents (`TK-1042` to `TK-1051`).

---

### **Slide 3: System Architecture & ReAct Loop**
* **Architecture Diagram**:
  * **Input Layer**: Employee Ticket / Interactive Portal (Streamlit).
  * **Reasoning Layer**: ReAct Loop (Intent Recognition $\rightarrow$ KB Retrieval $\rightarrow$ Historical Precedent Match $\rightarrow$ Diagnostic Check).
  * **Model**: Groq LPU with `openai/gpt-oss-120b` for low-latency contextual dialogue.
  * **Policy Enforcement Layer**: Deterministic Policy Engine (Validates device age, quotas, contractor status, and approval hierarchies).
  * **Action Layer**: Automated Resolution vs. Human Escalation (IT Security, Finance, Manager).
  * **Governance Layer**: Persistent Audit Trail (`audit_trail.json`).
* **Modular Engineering**: Built with modular single-responsibility Python scripts (`config.py`, `data_pack.py`, `policy_engine.py`, `tools.py`, `prompts.py`, `parser.py`, `llm.py`, `agent.py`, `memory.py`, `app.py`).

---

### **Slide 4: Grounded Knowledge Base & Precedent Data Pack**
* **Veridian Corporate Knowledge Base**:
  * `KB-01`: Password Reset (Self-service vs >5 failed attempts manual unlock).
  * `KB-02`: VPN Access (Full-time automatic / Contractor manager sign-off / 90-day renewal).
  * `KB-03`: Laptop Replacement (3 years of service or verified failure).
  * `KB-04`: Software Installation (Catalog self-service vs Non-catalog 3–5 day Security review).
  * `KB-05`: Printer Troubleshooting (Print spooler restart & asset tagging).
  * `KB-06`: Email Quota (25GB default, manager approval needed up to 50GB cap).
  * `KB-07`: Guest Wi-Fi (Front-desk kiosk, 24-hour validity, no ticket needed).
  * `KB-08`: Expense Software (Granted by Finance, not IT).
  * `KB-09`: Security Incidents (Phishing reporting to `security@...`, strict DO NOT FORWARD rule).
  * `KB-10`: Work-from-Home (>3 days/week, Manager & Finance approval required).
  * `ASSET-POL`: Finance & Asset Management Policy (Mandates 4-year hardware refresh).
* **Ticketing Queue History**: 10 active/closed precedent tickets used for case-law reasoning (`TK-1042` to `TK-1051`).

---

### **Slide 5: Resolving Policy Conflicts (KB-03 vs. Finance Asset Policy)**
* **The Conflict Scenario**:
  * `KB-03` states laptops are eligible for replacement after **3 years**.
  * `Finance Asset Policy (Q2 2026)` mandates a **4-year refresh cycle** and requires Finance sign-off for out-of-cycle replacements.
* **The Agent's Precedent-Grounded Solution**:
  * Consults historical ticket **`TK-1043` (S. Iyer, 3.2 yrs old)** which was approved with a Finance exception.
  * In `REQ-01` (Aditi Sharma, 3.5 yrs old, dead laptop): Agent identifies that while `KB-03` criteria is met, it is within the 4-year window, requiring **Finance sign-off** in addition to IT approval.
  * In `REQ-13` (Aman Gupta, 2.0 yrs old, flickering screen): Agent denies replacement but routes for **hardware screen repair**, protecting corporate capital.

---

### **Slide 6: Critical Security Guardrails & Threat Containment**
* **Case Study: REQ-08 (Ananya Reddy)**:
  * Employee message: *"I think I got a phishing email asking for my login — forwarding it to a few teammates to check."*
* **Agent's Immediate Interventions**:
  1. **Immediate Threat Halt**: Emphatically instructs employee **NOT to forward** the email, preventing viral credential harvesting.
  2. **Automated Incident Escalation**: Immediately logs a high-urgency ticket and routes to `security@veridian-corp.example` under `KB-09`.
  3. **Audit Compliance**: Precedent aligned with `TK-1048` (Phishing email under investigation).

---

### **Slide 7: Ambiguity Handling & Diagnostic Questioning**
* **Case Study: REQ-15 (Rahul Menon)**:
  * Employee message: *"hey can you help, its not working"*
* **Why Traditional LLMs Fail**: Standard chatbots hallucinate by guessing what is broken or giving generic answers.
* **The Agent's Triage Behavior**:
  * Flags request as `Pending User Clarification`.
  * Generates 3 targeted diagnostic questions:
    1. *What specific service, application, or hardware is malfunctioning?*
    2. *What exact error message or code is displayed?*
    3. *If related to hardware, what is your equipment Asset Tag?*

---

### **Slide 8: Complete 15-Request Evaluation Benchmark**
* **100% Grounded Triage Results**:
  * **Automated Self-Service Resolutions (8 requests)**: `REQ-02` (Guest Wi-Fi), `REQ-03` (Password unlock), `REQ-05` (VPN renewal), `REQ-06` (Printer spooler), `REQ-09` (Mailbox archive), `REQ-11` (Contractor VPN form), `REQ-12` (Expense tool check), `REQ-13` (Screen repair).
  * **Governance & Security Escalations (6 requests)**: `REQ-01` (Finance Early Laptop Refresh), `REQ-04` (Security Software Review), `REQ-07` (WFH Hardware Finance), `REQ-08` (Critical Phishing Containment), `REQ-10` (Admin Access Governance), `REQ-14` (Browser Extension Review).
  * **Diagnostic Clarification (1 request)**: `REQ-15` (Ambiguous Query Follow-up).

---

### **Slide 9: Interactive Prototype Features & Streamlit UI**
* **6 Rich Operational Panels**:
  1. **💬 Employee Support Portal**: Real-time conversational triage with official scenario loader and dynamic custom question testing.
  2. **⚡ Batch Request Triage**: One-click benchmark of all 15 requests with expandable deep-dive inspectors.
  3. **📑 Ticket Queue & Precedents**: Full visibility into historical case law (`TK-1042` to `TK-1051`).
  4. **📚 Knowledge Base & Policy Simulator**: Interactive simulator for hardware age conflicts and mailbox quota limits.
  5. **🛡️ Compliance Audit Trail**: Transparent, searchable audit log with timestamps, policy tags, and assigned escalation owners.
  6. **📊 10-Slide Presentation Deck**: Native in-app slide deck viewer for the viva / live defense.

---

### **Slide 10: Business Impact, Defense Preparation & Future Roadmap**
* **Measurable ROI**:
  * **53% of requests resolved autonomously** without IT engineer touch time.
  * **Zero compliance breaches**: 100% adherence to Security reviews (`KB-04`, `KB-09`) and Finance hardware refresh caps.
  * **Instant Time-to-Resolution**: Sub-second triage compared to multi-hour helpdesk backlog queues.
* **Prepared for Defense**:
  * Live interactive Streamlit prototype (`http://localhost:8501`).
  * In-app 10-slide deck and synchronized `presentation_deck.md`.
  * Clean, modular student-built codebase ready for GitHub submission.
  * Complete 30-case test coverage across official requests, edge cases, and natural user queries.
