"""
memory.py
Maintains session chat history and complete audit log for all IT triage decisions.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

AUDIT_LOG_FILE = "it_service_agent/audit_trail.json"

def save_audit_record(record: Dict[str, Any]):
    """Persist an audit log entry for enterprise compliance and review."""
    os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
    records = get_audit_trail()
    record["timestamp"] = datetime.now().isoformat()
    records.append(record)
    try:
        with open(AUDIT_LOG_FILE, "w") as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        print(f"Error saving audit log: {e}")

def get_audit_trail() -> List[Dict[str, Any]]:
    """Retrieve full historical audit trail."""
    if not os.path.exists(AUDIT_LOG_FILE):
        return []
    try:
        with open(AUDIT_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def clear_audit_trail():
    """Reset audit logs."""
    if os.path.exists(AUDIT_LOG_FILE):
        try:
            os.remove(AUDIT_LOG_FILE)
        except Exception:
            pass
