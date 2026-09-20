"""
policy_engine.py
Deterministic rule validation, policy citation, and edge-case conflict resolution.
Grounds decisions in Veridian Corp policies and precedent tickets.
"""

from typing import Dict, Any, List

try:
    from it_service_agent.data_pack import KNOWLEDGE_BASE, TICKET_QUEUE
except ImportError:
    from data_pack import KNOWLEDGE_BASE, TICKET_QUEUE

def evaluate_hardware_request(device_type: str, age_years: float, issue_description: str) -> Dict[str, Any]:
    """
    Evaluates hardware requests resolving the tension between:
    - KB-03: Eligible after 3 years or verified hardware failure; requires 2 weeks advance notice.
    - ASSET-POL: Standard 4-year refresh cycle. Replacements before 4 years require Finance sign-off + IT approval.
    """
    is_hardware_failure = any(term in issue_description.lower() for term in ["dead", "won't turn on", "wont turn on", "broken", "failure"])
    
    if age_years >= 4.0:
        return {
            "eligible": True,
            "requires_finance_approval": False,
            "action": "Standard 4-year refresh cycle fulfilled. Proceed with standard replacement.",
            "policies": ["KB-03", "ASSET-POL"],
            "escalate_to": "IT Procurement / Fulfillment"
        }
    elif age_years >= 3.0:
        # Conflicts with 4-year Finance policy!
        # Precedent TK-1043 shows S. Iyer (3.2 yrs old) was 'Approved — pending fulfillment' with Finance exception.
        return {
            "eligible": True,
            "requires_finance_approval": True,
            "action": (
                f"Device age ({age_years} yrs) meets KB-03 (>3 yrs) but is under Finance 4-year cycle. "
                "Per Asset Management Policy & precedent TK-1043, early replacement requires Finance sign-off in addition to IT approval."
            ),
            "policies": ["KB-03", "ASSET-POL"],
            "precedent": "TK-1043",
            "escalate_to": "Finance & IT Approval"
        }
    else:
        if is_hardware_failure:
            return {
                "eligible": False,
                "replacement_exception": True,
                "action": (
                    f"Device age ({age_years} yrs) is under 3 years. Verified hardware failure reported. "
                    "Per KB-03, requires diagnostic verification and Finance + IT approval for out-of-cycle replacement/repair."
                ),
                "policies": ["KB-03", "ASSET-POL"],
                "escalate_to": "IT Hardware Technician & Finance"
            }
        else:
            return {
                "eligible": False,
                "replacement_exception": False,
                "action": (
                    f"Device age ({age_years} yrs) is under refresh cycle (4 years). "
                    "Routine replacement not eligible. Route to IT technician for troubleshooting or repair."
                ),
                "policies": ["KB-03", "ASSET-POL"],
                "escalate_to": "IT Hardware Support (Repair Queue)"
            }

def evaluate_vpn_request(is_contractor: bool, is_expired: bool) -> Dict[str, Any]:
    """
    Evaluates VPN access per KB-02:
    - Full-time employees: Automatic access, 90-day renewal cycle.
    - Contractors: Requires manager approval submitted via access request form.
    """
    if is_contractor:
        return {
            "action": "Contractor VPN access requires manager approval submitted via the access request form.",
            "policies": ["KB-02"],
            "requires_approval": True,
            "escalate_to": "Employee's Manager"
        }
    elif is_expired:
        return {
            "action": "VPN credentials expire every 90 days. Full-time employees can self-renew credentials via the identity portal.",
            "policies": ["KB-02"],
            "requires_approval": False,
            "escalate_to": None
        }
    else:
        return {
            "action": "VPN access is automatically provisioned for full-time employees.",
            "policies": ["KB-02"],
            "requires_approval": False,
            "escalate_to": None
        }

def evaluate_mailbox_quota(requested_gb: float) -> Dict[str, Any]:
    """
    Evaluates mailbox quota per KB-06:
    - Default: 25GB.
    - Above 25GB: Requires manager approval.
    - Cap: Max 50GB.
    """
    if requested_gb <= 25:
        return {
            "allowed": True,
            "action": "Within default 25GB limit. No manager approval needed. Recommend archiving if full.",
            "policies": ["KB-06"]
        }
    elif requested_gb <= 50:
        return {
            "allowed": True,
            "action": f"Request for {requested_gb}GB exceeds 25GB default. Requires manager approval per KB-06 (Precedent TK-1045 approved at 35GB).",
            "policies": ["KB-06"],
            "precedent": "TK-1045",
            "escalate_to": "Manager"
        }
    else:
        return {
            "allowed": False,
            "action": f"Requested {requested_gb}GB exceeds hard company cap of 50GB. Policy strictly caps quota at 50GB.",
            "policies": ["KB-06"],
            "escalate_to": "Rejected / Manager Exception"
        }

def find_relevant_policies(text: str) -> List[Dict[str, Any]]:
    """Keywords and contextual matcher for Veridian Corp knowledge base."""
    t = text.lower()
    matches = []

    # Security / Phishing / Fraud / Prompt Injection Defense
    if any(k in t for k in ["phishing", "malware", "hacked", "suspicious email", "forwarding", "bank login", "gift card", "impersonat", "ceo", "override", "jailbreak", "unauthorized access"]):
        matches.append(KNOWLEDGE_BASE["KB-09"])

    # Password
    if any(k in t for k in ["password", "locked out", "lock out", "failed attempts", "cant login", "can't login", "unlock"]):
        matches.append(KNOWLEDGE_BASE["KB-01"])

    # Wi-Fi / Guest Network / Internet Access
    if any(k in t for k in ["wifi", "wi-fi", "internet", "guest access", "guest visiting", "clients", "visitor", "kiosk"]):
        matches.append(KNOWLEDGE_BASE["KB-07"])

    # VPN / Remote Access
    if any(k in t for k in ["vpn", "remote access", "contractor", "remote credentials", "credentials expired", "singapore", "travel"]):
        matches.append(KNOWLEDGE_BASE["KB-02"])

    # WFH equipment
    if any(k in t for k in ["work from home", "wfh", "home 4 days", "home 2 days", "home 3 days", "home office", "chair"]):
        matches.append(KNOWLEDGE_BASE["KB-10"])
        return matches

    # Laptop / Hardware
    if any(k in t for k in ["laptop", "turn on", "dead", "flickering", "monitor", "hardware", "crushed", "desk phone", "dark"]):
        matches.append(KNOWLEDGE_BASE["KB-03"])
        matches.append(KNOWLEDGE_BASE["ASSET-POL"])

    # Software installation
    if any(k in t for k in ["software", "install", "catalog", "browser extension", "tool", "docker", "vscode", "application"]):
        matches.append(KNOWLEDGE_BASE["KB-04"])

    # Printer
    if any(k in t for k in ["printer", "paper jam", "print spooler", "spooler"]):
        matches.append(KNOWLEDGE_BASE["KB-05"])

    # Mailbox / Outlook storage
    if any(k in t for k in ["mailbox", "quota", "25gb", "50gb", "100gb", "full", "can't send emails", "outlook", "storage"]):
        matches.append(KNOWLEDGE_BASE["KB-06"])

    # Expense software / Admin / Privileged Access
    if any(k in t for k in ["expense", "expense tool", "finance reporting", "admin access", "domain admin", "sudo", "root", "server"]):
        matches.append(KNOWLEDGE_BASE["KB-08"])

    return matches

def search_precedent(query: str) -> List[Dict[str, Any]]:
    """Search closed and active tickets for matching precedent."""
    q = query.lower()
    results = []
    for ticket in TICKET_QUEUE:
        if any(term in ticket["issue_summary"].lower() or term in ticket["resolution_pattern"].lower() for term in q.split()):
            results.append(ticket)
    return results
