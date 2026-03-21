import re
from typing import Optional
from .rules import BLOCKED_INPUT_PATTERNS, MDM_DOMAIN_KEYWORDS

class InputGuardResult:
    def __init__(self, allowed: bool, reason: str = ""):
        self.allowed = allowed
        self.reason = reason

def check_input(user_query: str) -> InputGuardResult:
    """
    Validates user input before sending to Vanna.
    Returns InputGuardResult(allowed=False, reason=...) on violation.
    """
    query_lower = user_query.lower().strip()

    # 1. Empty / too short
    if len(query_lower) < 5:
        return InputGuardResult(False, "Query too short.")

    # 2. Too long (prompt injection attempts are often very long)
    if len(user_query) > 1000:
        return InputGuardResult(False, "Query too long. Max 1000 characters.")

    # 3. Prompt injection / jailbreak patterns
    for pattern in BLOCKED_INPUT_PATTERNS:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return InputGuardResult(
                False,
                "This query is not supported. Please ask questions about your MDM data."
            )

    # 4. Domain relevance check
    domain_hit = any(kw in query_lower for kw in MDM_DOMAIN_KEYWORDS)
    if not domain_hit:
        return InputGuardResult(
            False,
            "I can only answer questions about meter data, energy, devices, "
            "events, and related MDM topics. Please rephrase your question."
        )

    return InputGuardResult(True)
