MDM_DOCUMENTATION = """
MDM (Meter Data Management) system for utility meters in India.

KEY RELATIONSHIPS:
- CUSTOMER → ACCOUNT → SERVICE_AGREEMENT → SERVICE_POINT → DEVICE
- DEVICE → STREAM → interval_raw / daily_raw / instant_raw / event_raw
- service_point.address_id = address.id
- service_point_device_rel: many-to-many, device installed at service point
- contact_customer_rel: many-to-many, contact linked to customer

MEASUREMENT TABLES:
- interval_raw: 15-min readings (kwh_import, kwh_export, kwh_net, kvah, voltages V, currents A, frequency hz)
- daily_raw: daily aggregates (kwh_import, kwh_export, mdkva, mdkw = max demand)
- instant_raw: instantaneous (ir, iy, ib currents; v_rn, v_yn, v_bn voltages)
- event_raw: meter events identified by event_code (stored as zero-padded string e.g. '0101')

DEMAND CALCULATION:
- Peak kW from interval_raw = MAX(kwh_import) * 12 (since intervals are 5-min = 1/12 hour)
- Peak kVA from interval_raw = MAX(kvah) * 12
- Power Factor = kwh_import / kvah (per interval)

EVENT CODES: event_code is stored as a zero-padded 4-char string ('0003', '0101', etc.)
Always filter event_raw using: WHERE event_code = '0101' (not 101)

PERIOD PATTERNS (use these exact SQL expressions for time filtering):
- TODAY: interval_end_time >= CURRENT_DATE::timestamp AND interval_end_time < (CURRENT_DATE+1)::timestamp
- THIS_WEEK: interval_end_time >= date_trunc('week', CURRENT_DATE) AND interval_end_time < date_trunc('week', CURRENT_DATE) + INTERVAL '7 days'
- THIS_MONTH: interval_end_time >= date_trunc('month', CURRENT_DATE) AND interval_end_time < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'

ALL TABLES have: org_id (multi-tenancy), status='Active' (live records), insert_ts, last_upd_ts, rev
"""
