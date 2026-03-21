"""
Given one user query, generate 5 semantically equivalent NL variations.
This improves SQL generation coverage — different phrasings activate
different parts of Vanna's vector store.
"""
import json
import openai
from config.settings import settings
from config.event_codes import ALLOWED_EVENTS

def extract_entities(user_query: str) -> dict:
    """
    Use GPT to extract structured entities from the user's query.
    Returns: {device_id, period_type, event_codes, metric_types, location}
    """
    client = openai.OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
Extract structured entities from this MDM (Meter Data Management) query.
Return ONLY valid JSON with these keys:
{{
  "device_ids": [],        // list of device IDs like dev__EEOT4056946
  "period_type": "",       // TODAY | YESTERDAY | THIS_WEEK | LAST_WEEK | THIS_MONTH | LAST_MONTH | CUSTOM
  "event_categories": [],  // Grid Reliability | Revenue Protection | Network Health | Security | Operational Control
  "metric_types": [],      // energy | load | demand | voltage | current | power_factor | events
  "locations": []          // city names, feeder names, etc.
}}

Query: "{user_query}"
"""
    resp = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300,
    )
    try:
        content = resp.choices[0].message.content
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return json.loads(content)
    except Exception:
        return {}

def generate_prompt_variations(user_query: str, entities: dict) -> list[str]:
    """
    Generate 5 NL variations of the user's query.
    Variations are designed to hit different SQL patterns in Vanna's store.
    """
    client = openai.OpenAI(api_key=settings.openai_api_key)

    # Build event context hint for prompts
    event_hint = ""
    if entities.get("event_categories"):
        cats = entities["event_categories"]
        relevant_events = [e for e in ALLOWED_EVENTS if e["category"] in cats]
        if relevant_events:
            event_hint = f"\\nRelevant event codes: {[e['id'] for e in relevant_events[:5]]}"

    system = """You are an expert at rephrasing meter data management (MDM) queries.
Generate exactly 5 distinct phrasings of the user's query. Each must:
1. Preserve the EXACT same intent and all entity values (device IDs, time periods, etc.)
2. Use different vocabulary, structure, or perspective
3. Be suitable for generating a PostgreSQL query against an MDM database
4. Include all context: device IDs, time periods, metric names

Return a JSON array of 5 strings. No other text."""

    user_msg = f"""Original query: "{user_query}"
Extracted entities: {json.dumps(entities)}
{event_hint}

Generate 5 variations. Return JSON array only."""

    resp = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
        max_tokens=800,
    )
    try:
        content = resp.choices[0].message.content
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        variations = json.loads(content)
        # Always include original as first
        return [user_query] + [v for v in variations if v != user_query][:4]
    except Exception:
        return [user_query] * 5  # fallback: repeat original
