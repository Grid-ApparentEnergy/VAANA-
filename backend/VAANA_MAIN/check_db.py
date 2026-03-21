import os, sys
# Add core to path
sys.path.append(os.path.join(os.getcwd(), 'core'))

import psycopg2
from core.config import POSTGRES_DB_CONFIG

try:
    conn = psycopg2.connect(**POSTGRES_DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    print("Available tables in the database:")
    for t in tables:
        print(f"- {t[0]}")
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
