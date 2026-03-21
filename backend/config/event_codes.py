ALLOWED_EVENTS = [
    {"id": "0003", "description": "Y-Phase VT link missing", "severity": "High", "category": "Tamper"},
    {"id": "0004", "description": "Y-Phase VT link missing Restored", "severity": "Info", "category": "Tamper"},
    {"id": "0101", "description": "Power Failure (3 Phase)", "severity": "High", "category": "Outage"},
    {"id": "0102", "description": "Power Failure Restored", "severity": "Info", "category": "Outage"}
]

EVENT_PAIRS = [
    ("0003", "0004"),
    ("0101", "0102")
]

EVENT_BY_CODE = {e["id"]: e for e in ALLOWED_EVENTS}

def _pad_code(code: str | int) -> str:
    return str(code).zfill(4)

def get_event_description(code: str | int) -> str:
    padded = _pad_code(code)
    return EVENT_BY_CODE.get(padded, {"description": "Unknown Event"})["description"]

def get_event_severity(code: str | int) -> str:
    padded = _pad_code(code)
    return EVENT_BY_CODE.get(padded, {"severity": "Unknown"})["severity"]

def get_event_category(code: str | int) -> str:
    padded = _pad_code(code)
    return EVENT_BY_CODE.get(padded, {"category": "Unknown"})["category"]
