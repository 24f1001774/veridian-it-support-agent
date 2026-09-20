"""
tools.py
Standardized IT Helpdesk Agent tools.
Allows the agent to lookup policies, inspect historical tickets,
perform automated actions, or create escalations with full auditability.
"""

import json
from typing import Dict, Any, List

try:
    from it_service_agent.data_pack import KNOWLEDGE_BASE, TICKET_QUEUE
    from it_service_agent.policy_engine import (
        evaluate_hardware_request,
        evaluate_vpn_request,
        evaluate_mailbox_quota,
        find_relevant_policies,
        search_precedent
    )
except ImportError:
    from data_pack import KNOWLEDGE_BASE, TICKET_QUEUE
    from policy_engine import (
        evaluate_hardware_request,
        evaluate_vpn_request,
        evaluate_mailbox_quota,
        find_relevant_policies,
        search_precedent
    )

def lookup_kb_policy(policy_id: str) -> str:
    """Lookup specific policy from Knowledge Base by ID (e.g., KB-01, ASSET-POL)."""
    pid = policy_id.upper().strip()
    if pid in KNOWLEDGE_BASE:
        p = KNOWLEDGE_BASE[pid]
        return json.dumps({
            "status": "found",
            "id": p["id"],
            "title": p["title"],
            "category": p["category"],
            "policy": p["content"],
            "requires_approval": p["requires_approval"],
            "approval_authority": p["approval_authority"]
        }, indent=2)
    return json.dumps({"status": "not_found", "message": f"Policy {policy_id} does not exist in Veridian KB."}, indent=2)

def query_knowledge_base(query: str) -> str:
    """Semantic/keyword search across Veridian Corp knowledge base."""
    policies = find_relevant_policies(query)
    if not policies:
        return json.dumps({"status": "no_match", "message": "No direct policy match found. Request may need clarification."}, indent=2)
    
    results = [
        {
            "id": p["id"],
            "title": p["title"],
            "content": p["content"],
            "requires_approval": p["requires_approval"],
            "approval_authority": p["approval_authority"]
        }
        for p in policies
    ]
    return json.dumps({"status": "matches_found", "policies": results}, indent=2)

def check_historical_precedent(issue_keyword: str) -> str:
    """Find precedent from previous ticket decisions (TK-1042 to TK-1051)."""
    precedents = search_precedent(issue_keyword)
    return json.dumps({
        "status": "success",
        "count": len(precedents),
        "precedents": precedents
    }, indent=2)

def run_hardware_policy_check(age_years: float, issue: str) -> str:
    """Evaluate laptop/monitor replacement against KB-03 and Finance 4-year cycle."""
    eval_result = evaluate_hardware_request("laptop", age_years, issue)
    return json.dumps(eval_result, indent=2)

def create_service_ticket(
    employee: str,
    category: str,
    summary: str,
    action_type: str,
    cited_policies: List[str],
    escalation_team: str = None,
    audit_notes: str = ""
) -> Dict[str, Any]:
    """Generates an audit-ready structured ticket."""
    ticket = {
        "ticket_id": f"TK-AUTO-{hash(employee + summary) % 10000:04d}",
        "employee": employee,
        "category": category,
        "summary": summary,
        "action_type": action_type, # 'Resolved (Automated)' | 'Escalated (Human Required)' | 'Pending User Clarification'
        "cited_policies": cited_policies,
        "escalation_team": escalation_team or "None (Direct Resolution)",
        "audit_notes": audit_notes,
        "status": "Open" if action_type.startswith("Escalated") else "Resolved"
    }
    return ticket
