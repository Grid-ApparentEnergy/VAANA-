"""
Direct OpenAI implementation without ChromaDB
Uses hardcoded context for SQL generation
"""
import os
import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from config.settings import settings
from config.ddl import MDM_DDL
from config.documentation import MDM_DOCUMENTATION

# Hardcoded SQL examples with CORRECT column names
SQL_EXAMPLES = """
Example 1:
Question: Show me the first 5 records of the device table
SQL: SELECT * FROM device LIMIT 5;

Example 2:
Question: How many records are in the product table
SQL: SELECT COUNT(*) FROM product;

Example 3:
Question: How many devices are there
SQL: SELECT COUNT(*) FROM device;

Example 4:
Question: List all devices in Raipur
SQL: SELECT d.* FROM device d JOIN service_point_device_rel spdr ON d.id = spdr.device_id JOIN service_point sp ON spdr.service_point_id = sp.id JOIN address a ON sp.address_id = a.id WHERE a.city = 'Raipur';

Example 5:
Question: What are the active business services for device with id dev__EEOT4056946?
SQL: SELECT bs.* FROM business_service bs JOIN stream_service ss ON bs.id = ss.business_service_id JOIN stream s ON ss.stream_id = s.id JOIN service_point sp ON s.service_point_id = sp.id JOIN service_point_device_rel spdr ON sp.id = spdr.service_point_id JOIN device d ON spdr.device_id = d.id WHERE d.id = 'dev__EEOT4056946' AND bs.status = 'Active';

Example 6:
Question: Which cities have the most service points? List top 5.
SQL: SELECT a.city, COUNT(sp.id) AS service_point_count FROM service_point sp JOIN address a ON sp.address_id = a.id GROUP BY a.city ORDER BY service_point_count DESC LIMIT 5;

Example 7:
Question: Show me devices by type
SQL: SELECT device_type, COUNT(*) as count FROM device GROUP BY device_type;

Example 8:
Question: Get the latest interval data for a device with id dev__EEOT4056946
SQL: SELECT ir.* FROM interval_raw ir JOIN device d ON ir.device_id = d.id WHERE d.id = 'dev__EEOT4056946' ORDER BY ir.interval_end_time DESC LIMIT 10;

Example 9:
Question: Show me power outage events
SQL: SELECT er.* FROM event_raw er ORDER BY er.event_time DESC LIMIT 20;

Example 10:
Question: List all customers
SQL: SELECT * FROM customer LIMIT 10;

Example 11:
Question: Daily summary for DT meter with id dev__EEOT4056946 for today including peak load, avg load, and events
SQL: 
WITH interval_summary AS (
  SELECT 
    ir.device_id,
    MAX(ir.kw_import) as peak_load_kw,
    AVG(ir.kw_import) as avg_load_kw,
    MIN(ir.interval_end_time) as period_start,
    MAX(ir.interval_end_time) as period_end
  FROM interval_raw ir
  JOIN device d ON ir.device_id = d.id
  WHERE d.id = 'dev__EEOT4056946'
    AND ir.interval_end_time >= CURRENT_DATE
    AND ir.interval_end_time < CURRENT_DATE + INTERVAL '1 day'
  GROUP BY ir.device_id
),
event_summary AS (
  SELECT 
    er.device_id,
    er.event_code,
    COUNT(*) as event_count,
    STRING_AGG(DISTINCT er.event_code, ', ') as event_codes
  FROM event_raw er
  JOIN device d ON er.device_id = d.id
  WHERE d.id = 'dev__EEOT4056946'
    AND er.event_time >= CURRENT_DATE
    AND er.event_time < CURRENT_DATE + INTERVAL '1 day'
  GROUP BY er.device_id, er.event_code
)
SELECT 
  i.device_id,
  i.peak_load_kw,
  i.avg_load_kw,
  i.period_start,
  i.period_end,
  COALESCE(e.event_count, 0) as total_events,
  COALESCE(e.event_codes, 'No events') as event_codes
FROM interval_summary i
LEFT JOIN event_summary e ON i.device_id = e.device_id;

Example 12:
Question: Weekly summary for device with id dev__EEOT4056946 with peak load time and event details
SQL:
WITH interval_summary AS (
  SELECT 
    ir.device_id,
    MAX(ir.kw_import) as peak_load_kw,
    AVG(ir.kw_import) as avg_load_kw,
    (SELECT interval_end_time FROM interval_raw WHERE device_id = 'dev__EEOT4056946' AND kw_import = MAX(ir.kw_import) LIMIT 1) as peak_time,
    SUM(ir.kwh_import) as total_kwh_import
  FROM interval_raw ir
  JOIN device d ON ir.device_id = d.id
  WHERE d.id = 'dev__EEOT4056946'
    AND ir.interval_end_time >= date_trunc('week', CURRENT_DATE)
    AND ir.interval_end_time < date_trunc('week', CURRENT_DATE) + INTERVAL '7 days'
  GROUP BY ir.device_id
),
event_summary AS (
  SELECT 
    er.device_id,
    COUNT(*) as total_events,
    SUM(CASE WHEN er.event_code IN ('0101', '0102') THEN 1 ELSE 0 END) as power_failure_events,
    STRING_AGG(er.event_code || ' at ' || TO_CHAR(er.event_time, 'YYYY-MM-DD HH24:MI'), '; ') as event_details
  FROM event_raw er
  JOIN device d ON er.device_id = d.id
  WHERE d.id = 'dev__EEOT4056946'
    AND er.event_time >= date_trunc('week', CURRENT_DATE)
    AND er.event_time < date_trunc('week', CURRENT_DATE) + INTERVAL '7 days'
  GROUP BY er.device_id
)
SELECT 
  i.*,
  COALESCE(e.total_events, 0) as total_events,
  COALESCE(e.power_failure_events, 0) as power_failure_events,
  COALESCE(e.event_details, 'No events') as event_details
FROM interval_summary i
LEFT JOIN event_summary e ON i.device_id = e.device_id;
"""

CONTEXT = f"""
DATABASE SCHEMA:
{MDM_DDL}

DOCUMENTATION:
{MDM_DOCUMENTATION}

SQL EXAMPLES:
{SQL_EXAMPLES}

CRITICAL RULES:
- The device table primary key column is 'id' (NOT 'device_id')
- ALWAYS use SINGULAR table names: device (NOT devices), customer (NOT customers), business_service (NOT business_services), service_point (NOT service_points), address (NOT addresses)
- When joining device table: device.id = other_table.device_id
- service_point links to address via address_id
- device links to service_point via service_point_device_rel (spdr.device_id = device.id)
- To find business services for a device, join: device -> service_point_device_rel -> service_point -> stream -> stream_service -> business_service
- interval_raw.device_id and event_raw.device_id reference device.id
"""


def generate_sql(question: str) -> Optional[str]:
    """
    Generate SQL from question using OpenAI directly
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=settings.openai_api_key)
        
        # Construct prompt
        prompt = f"""{CONTEXT}

User question: {question}

Generate ONLY the SQL query, no explanations. Use proper PostgreSQL syntax.

SQL Query:"""
        
        logger.info(f"[vanna_direct] Generating SQL for: {question[:50]}...")
        
        # Call OpenAI
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a PostgreSQL expert. Generate only valid SQL queries based on the provided schema and examples."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        sql = response.choices[0].message.content.strip()
        
        # Clean up SQL (remove markdown code blocks if present)
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        sql = sql.strip()
        
        logger.info(f"[vanna_direct] Generated SQL: {sql[:100]}...")
        return sql
        
    except Exception as e:
        logger.error(f"[vanna_direct] SQL generation failed: {e}", exc_info=True)
        return None


def train_if_needed(force: bool = False):
    """No-op for compatibility"""
    logger.info("[vanna_direct] No training needed (using direct OpenAI)")
    pass
