# Define the full boundary of what this system is allowed to do.
# Any query outside this boundary is rejected BEFORE hitting Vanna.

ALLOWED_TABLES = {
    "account", "address", "business_service", "contact",
    "contact_customer_rel", "customer", "daily_raw", "device",
    "event_raw", "instant_raw", "interval_est", "interval_raw",
    "meas_meta", "product", "service_agreement", "service_point",
    "service_point_class", "service_point_device_rel",
    "service_point_group", "service_point_group_hierarchy_rel",
    "service_point_group_member_rel", "service_point_hierarchy_rel",
    "simulated_device_states", "stream", "stream_service",
    "stream_type", "users",
}

BLOCKED_SQL_KEYWORDS = [
    "DROP", "DELETE", "TRUNCATE", "INSERT", "UPDATE", "ALTER",
    "CREATE", "GRANT", "REVOKE", "EXECUTE", "EXEC", "pg_",
    "information_schema", "pg_catalog", "COPY", "--", "xp_",
    "UNION SELECT", "INTO OUTFILE", "LOAD_FILE",
]

BLOCKED_INPUT_PATTERNS = [
    r"ignore previous instructions",
    r"disregard (your|all) (instructions|rules)",
    r"you are now",
    r"act as",
    r"jailbreak",
    r"pretend (you are|to be)",
    r"what (model|llm|ai) are you",
    r"which (model|version|gpt|claude)",
    r"reveal your (system prompt|instructions|model)",
    r"what is your (underlying|base) model",
    r"powered by",
]

MDM_DOMAIN_KEYWORDS = [
    "meter", "device", "energy", "kwh", "kvah", "demand", "load",
    "interval", "event", "voltage", "current", "power factor",
    "customer", "service point", "stream", "feeder", "dt meter",
    "daily", "weekly", "monthly", "period", "outage", "tamper",
    "phase", "unbalance", "pf", "max demand", "peak",
]
