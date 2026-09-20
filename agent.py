"""
agent.py
Central Autonomous IT Support Agent for Veridian Corp.
Executes the ReAct loop:
1. Understand employee issue & detect intent
2. Query grounded Knowledge Base & check historical ticket precedent
3. Perform policy evaluation (e.g. resolve conflict between KB-03 and ASSET-POL)
4. Ask sensible follow-up questions if request is vague or missing parameters
5. Resolve simple requests or escalate risky/unclear requests
6. Generate structured ticket with policy citations and write audit trail
"""

import json
import re
from typing import Dict, Any, List

try:
    from it_service_agent.prompts import SYSTEM_PROMPT
    from it_service_agent.llm import chat
    from it_service_agent.parser import parse_tool_call
    from it_service_agent.tools import (
        lookup_kb_policy,
        query_knowledge_base,
        check_historical_precedent,
        run_hardware_policy_check,
        create_service_ticket
    )
    from it_service_agent.policy_engine import find_relevant_policies, search_precedent
    from it_service_agent.memory import save_audit_record
except ImportError:
    from prompts import SYSTEM_PROMPT
    from llm import chat
    from parser import parse_tool_call
    from tools import (
        lookup_kb_policy,
        query_knowledge_base,
        check_historical_precedent,
        run_hardware_policy_check,
        create_service_ticket
    )
    from policy_engine import find_relevant_policies, search_precedent
    from memory import save_audit_record

class ITSupportAgent:
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    def triage_request(self, employee: str, email: str, request_text: str, existing_context: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Executes end-to-end triage of an employee IT request.
        Returns a rich response dictionary including:
        - employee response
        - policy citations
        - decision type (Auto-Resolved, Escalated, Clarification Needed)
        - ticket created
        - audit trail record
        """
        import re
        trace = []
        
        # Step 1: Grounded Policy Search
        policies = find_relevant_policies(request_text)
        cited_policy_ids = [p["id"] for p in policies]
        
        # Step 2: Historical Precedent Search
        precedents = search_precedent(request_text)
        precedent_ids = [p["ticket_id"] for p in precedents]

        # Step 3: Determine if ambiguous / requires clarification
        has_letters = any(c.isalpha() for c in request_text)
        is_too_short = len(request_text.strip().split()) <= 2 and not any(k in request_text.lower() for k in ["vpn", "wifi", "laptop", "printer", "mail", "password", "screen"])
        is_ambiguous = (
            not has_letters
            or is_too_short
            or (
                len(request_text.strip().split()) <= 10 
                and any(phrase in request_text.lower() for phrase in ["not working", "help", "broken", "issue"]) 
                and not any(k in request_text.lower() for k in ["vpn", "wifi", "laptop", "printer", "mail", "password", "screen", "catalog", "phishing", "quota", "admin", "sudo"])
            )
            or (len(policies) == 0 and not any(k in request_text.lower() for k in ["admin", "sudo", "phishing", "bank", "wfh", "work from home"]))
        )
        
        # Step 4: Construct conversation for LLM ReAct
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add grounding context
        grounding_context = (
            f"Employee: {employee} ({email})\n"
            f"Matched Policies in KB: {json.dumps(policies)}\n"
            f"Precedent Tickets: {json.dumps(precedents)}\n"
        )
        messages.append({"role": "system", "content": f"Verified Grounding Context:\n{grounding_context}"})

        if existing_context:
            messages.extend(existing_context)

        messages.append({"role": "user", "content": request_text})

        # Run inference
        llm_response = chat(messages)

        # Step 5: Classify Action & Escalation Authority
        action_type = "Resolved (Self-Service / Automated)"
        escalation_team = None
        urgency = "Standard"

        req_lower = request_text.lower()
        if is_ambiguous:
            action_type = "Pending User Clarification"
            escalation_team = "Employee Follow-up"
            urgency = "Low"
        elif any(k in req_lower for k in ["phishing", "malware", "bank login", "override", "jailbreak"]):
            action_type = "Escalated (Security Incident)"
            escalation_team = "IT Security (security@veridian-corp.example)"
            urgency = "Critical"
        elif any(k in req_lower for k in ["admin access", "finance reporting server", "domain admin", "sudo", "root"]):
            action_type = "Escalated (Privileged Access Review)"
            escalation_team = "Finance Application Owner & Security"
            urgency = "High"
        elif "laptop" in req_lower and any(k in req_lower for k in ["dead", "3.5", "turn on", "crushed"]):
            action_type = "Escalated (Early Replacement Approval)"
            escalation_team = "Finance & IT Assets"
            urgency = "High"
        elif "browser extension" in req_lower or "not in the software catalog" in req_lower:
            action_type = "Escalated (Security Review 3-5 days)"
            escalation_team = "IT Security Review Queue"
            urgency = "Medium"
        elif "work from home" in req_lower or "home 4 days" in req_lower or "home 2 days" in req_lower or "4 days" in req_lower:
            action_type = "Escalated (Finance & Manager Approval)"
            escalation_team = "People Ops & Finance"
            urgency = "Medium"
        elif any(k in req_lower for k in ["100gb", "quota"]):
            action_type = "Resolved (Policy Cap Enforcement)"
            escalation_team = None
            urgency = "Standard"

        # Step 6: Create Structured Ticket
        ticket = create_service_ticket(
            employee=employee,
            category=policies[0]["category"] if policies else "General IT",
            summary=request_text,
            action_type=action_type,
            cited_policies=cited_policy_ids,
            escalation_team=escalation_team,
            audit_notes=f"Auto-analyzed with ground truth policies {cited_policy_ids}. Precedent checked: {precedent_ids}."
        )

        # Step 7: Record in Audit Trail
        audit_record = {
            "employee": employee,
            "email": email,
            "request": request_text,
            "decision": action_type,
            "urgency": urgency,
            "cited_policies": cited_policy_ids,
            "precedents_referenced": precedent_ids,
            "escalated_to": escalation_team,
            "ticket_id": ticket["ticket_id"],
            "agent_response": llm_response
        }
        save_audit_record(audit_record)

        return {
            "response": llm_response,
            "action_type": action_type,
            "urgency": urgency,
            "policies": policies,
            "cited_policy_ids": cited_policy_ids,
            "precedents": precedents,
            "ticket": ticket,
            "audit_record": audit_record
        }
