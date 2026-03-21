# Summary Query Examples for DT Meters

## Overview
This document provides SQL query patterns for generating daily/weekly/monthly summaries for DT meters, including interval data (load) and event data.

## Query Pattern: Complete Summary

### Daily Summary
```sql
WITH interval_summary AS (
  SELECT 
    device_id,
    MAX(kw_import) as peak_load_kw,
    AVG(kw_import) as avg_load_kw,
    (SELECT interval_end_time 
     FROM interval_raw 
     WHERE device_id = 'YOUR_DEVICE_ID' 
       AND kw_import = (SELECT MAX(kw_import) FROM interval_raw WHERE device_id = 'YOUR_DEVICE_ID' AND interval_end_time >= CURRENT_DATE)
     LIMIT 1) as peak_load_time,
    SUM(kwh_import) as total_kwh_import,
    MIN(interval_end_time) as period_start,
    MAX(interval_end_time) as period_end
  FROM interval_raw
  WHERE device_id = 'YOUR_DEVICE_ID'
    AND interval_end_time >= CURRENT_DATE
    AND interval_end_time < CURRENT_DATE + INTERVAL '1 day'
  GROUP BY device_id
),
event_summary AS (
  SELECT 
    device_id,
    event_code,
    COUNT(*) as event_count,
    SUM(EXTRACT(EPOCH FROM (restoration_time - occurrence_time))/60) as total_duration_minutes
  FROM (
    SELECT 
      occ.device_id,
      occ.event_code,
      occ.event_time as occurrence_time,
      MIN(rst.event_time) as restoration_time
    FROM event_raw occ
    LEFT JOIN event_raw rst 
      ON rst.device_id = occ.device_id 
      AND rst.event_code = (occ.event_code::int + 1)::text
      AND rst.event_time > occ.event_time
    WHERE occ.device_id = 'YOUR_DEVICE_ID'
      AND occ.event_time >= CURRENT_DATE
      AND occ.event_time < CURRENT_DATE + INTERVAL '1 day'
      AND occ.event_code::int % 2 = 1
    GROUP BY occ.device_id, occ.event_code, occ.event_time
  ) events
  GROUP BY device_id, event_code
)
SELECT 
  i.device_id,
  i.peak_load_kw,
  i.avg_load_kw,
  i.peak_load_time,
  i.total_kwh_import,
  i.period_start,
  i.period_end,
  COALESCE(json_agg(json_build_object(
    'event_code', e.event_code,
    'count', e.event_count,
    'total_minutes', e.total_duration_minutes
  )) FILTER (WHERE e.event_code IS NOT NULL), '[]'::json) as events
FROM interval_summary i
LEFT JOIN event_summary e ON i.device_id = e.device_id
GROUP BY i.device_id, i.peak_load_kw, i.avg_load_kw, i.peak_load_time, i.total_kwh_import, i.period_start, i.period_end;
```

### Weekly Summary
Replace the date filters with:
```sql
WHERE interval_end_time >= date_trunc('week', CURRENT_DATE)
  AND interval_end_time < date_trunc('week', CURRENT_DATE) + INTERVAL '7 days'
```

### Monthly Summary
Replace the date filters with:
```sql
WHERE interval_end_time >= date_trunc('month', CURRENT_DATE)
  AND interval_end_time < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
```

## Natural Language Query Examples

The system can understand these queries:

1. **"Daily summary for DT meter [device_id] for today"**
   - Returns: Peak load, avg load, peak time, total energy, events

2. **"Weekly summary for device [device_id] with events"**
   - Returns: Week-to-date load statistics and event counts

3. **"Monthly summary for [device_id] including peak load time and event details"**
   - Returns: Month-to-date comprehensive summary

4. **"Show me yesterday's summary for DT meter [device_id]"**
   - Returns: Previous day's complete summary

## Response Format

The enhanced response structurer automatically formats the results with:

- **Summary**: Natural language description of the data
- **KPIs**: Key metrics displayed as cards (peak load, avg load, total energy)
- **Charts**: Auto-generated visualizations based on data patterns
- **Tables**: Complete data table with all columns
- **Metadata**: Row count, period, truncation status

## Example Response Structure

```json
{
  "status": "success",
  "summary": "Device dev__EEOT4056946 recorded a peak load of 45.2 kW at 14:30 today...",
  "kpis": [],
  "charts": [
    {
      "id": "metric",
      "type": "metric",
      "title": "Peak Load",
      "data": {"value": 45.2, "label": "Peak Load (kW)"}
    }
  ],
  "tables": [
    {
      "id": "raw_data",
      "title": "Query Results",
      "columns": ["device_id", "peak_load_kw", "avg_load_kw", "peak_load_time", "total_kwh_import", "events"],
      "rows": [...]
    }
  ],
  "metadata": {
    "device_id": "dev__EEOT4056946",
    "period_type": "DAILY",
    "row_count": 1,
    "truncated": false
  }
}
```

## Testing

Use the frontend chat interface at http://localhost:5173 or test via API:

```bash
curl -X POST "http://localhost:8000/api/stream/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Daily summary for DT meter dev__EEOT4056946 for today", "device_id": "", "period_type": "DAILY"}'
```
