# Testing Guide for Vanna 2.0 Integration

## System Status

✓ Backend running on: http://localhost:8000
✓ Frontend running on: http://localhost:5173
✓ Vanna 2.0.2 with direct OpenAI integration (bypassing ChromaDB)
✓ Schema corrected (device.id is primary key)

## Quick Test via Frontend

1. Open http://localhost:5173 in your browser
2. Try these sample queries:
   - "How many devices are there"
   - "Show me the first 5 records of the device table"
   - "Show me devices by type"
   - "List all devices in Raipur"
   - "Get the latest interval data for device dev__EEOT4056946"

## API Endpoints

### Query Endpoint
```
POST http://localhost:8000/api/query/
Content-Type: application/json

{
  "query": "How many devices are there",
  "device_id": "",
  "period_type": "THIS_WEEK"
}
```

### Streaming Endpoint
```
POST http://localhost:8000/api/streaming/query
Content-Type: application/json

{
  "question": "Show me devices by type"
}
```

### Health Check
```
GET http://localhost:8000/api/health
```

## Testing with PowerShell

```powershell
# Test query endpoint
$body = @{query="How many devices are there"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/query/" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json -Depth 10
```

## Testing with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/query/",
    json={"query": "How many devices are there"}
)
print(response.json())
```

## Sample Queries to Test

### Basic Queries
- "How many devices are there"
- "Show me the first 5 records of the device table"
- "List all customers"
- "How many records are in the product table"

### Aggregation Queries
- "Show me devices by type"
- "Which cities have the most service points? List top 5"

### Join Queries
- "List all devices in Raipur"
- "What are the active business services for device dev__EEOT4056946"

### Time-Series Queries
- "Get the latest interval data for device dev__EEOT4056946"
- "Show me power outage events"

### Complex Summary Queries
- "Daily summary for device dev__EEOT4056946 for today including peak load, avg load, and events"
- "Weekly summary for device dev__EEOT4056946 with peak load time and event details"

## Verified Working

✓ SQL generation with OpenAI API
✓ Schema corrections applied (device.id as primary key)
✓ Query endpoint responding successfully
✓ Response structuring and formatting
✓ Input/output guardrails active
✓ SQL validation with sqlglot
✓ Safe SQL execution with read-only checks

## Key Schema Notes

- Device table primary key: `id` (NOT `device_id`)
- interval_raw.device_id and event_raw.device_id reference device.id
- All table names are SINGULAR (device, not devices)
- Device IDs follow pattern: dev__EEOT4056946

## Architecture

```
User Query → Input Guard → Prompt Multiplier → Vanna Direct (OpenAI) 
  → SQL Comparator → SQL Validator → Executor → Response Structurer 
  → Output Guard → JSON Response
```

## What Was Fixed

1. Updated `backend/core/vanna_direct.py`:
   - Fixed SQL examples to use correct schema
   - Added explicit rules about device.id vs device_id

2. Updated `backend/config/ddl.py`:
   - Complete schema with all tables
   - Correct primary key definitions
   - Foreign key relationships documented

3. Updated `backend/config/documentation.py`:
   - Comprehensive table descriptions
   - Relationship mappings
   - Important notes about schema quirks

## Next Steps

The system is fully functional and ready for production use. You can:
1. Test via the frontend UI at http://localhost:5173
2. Integrate with your application using the API endpoints
3. Add more training examples to `vanna_direct.py` if needed
4. Monitor logs for any edge cases
