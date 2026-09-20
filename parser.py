"""
parser.py
Tool call parser and structured response extractor.
Handles JSON tool calls from LLM or regex fallback.
"""

import re
import json
from typing import Optional, Dict, Any

def parse_tool_call(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Detects if the LLM output contains a tool invocation.
    Expected pattern:
    Action: { "tool": "lookup_kb_policy", "parameters": { "policy_id": "KB-01" } }
    or ```json { "tool": ... } ```
    """
    if not response_text:
        return None

    # Check for Action: { ... }
    action_match = re.search(r"Action:\s*(\{.*?\})", response_text, re.DOTALL)
    if action_match:
        try:
            return json.loads(action_match.group(1).strip())
        except Exception:
            pass

    # Check for markdown code blocks containing json with "tool"
    code_blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
    for block in code_blocks:
        try:
            parsed = json.loads(block.strip())
            if isinstance(parsed, dict) and "tool" in parsed:
                return parsed
        except Exception:
            continue

    # Direct JSON search
    json_candidate = re.search(r'\{\s*"tool":\s*"[^"]+".*?\}', response_text, re.DOTALL)
    if json_candidate:
        try:
            return json.loads(json_candidate.group(0).strip())
        except Exception:
            pass

    return None

def extract_json_payload(text: str) -> Optional[Dict[str, Any]]:
    """Extract general JSON payload from response text."""
    try:
        # direct parse
        return json.loads(text.strip())
    except Exception:
        pass

    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass
    return None
