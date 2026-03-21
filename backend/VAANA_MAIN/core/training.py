import os
# Business Context
BUSINESS_CONTEXT = """
    CRITICAL DOMAIN KNOWLEDGE - TABLE MAPPING:
    - Devices/Meters: Use the `device` (SINGULAR) table. DO NOT USE `devices`.
    - Hardware Events: Use the `event_raw` table.
    - Interval/Load Data: Use the `interval_raw` table.
    - Customers: Use the `customer` (SINGULAR) table. DO NOT USE `customers`.
    - Products: Use the `product` (SINGULAR) table. DO NOT USE `products`.
    - Business Services: Use the `business_service` (SINGULAR) table. DO NOT USE `business_services`.
    - Service Points: Use the `service_point` (SINGULAR) table. DO NOT USE `service_points`.
    - Addresses/Cities: Use the `address` (SINGULAR) table.

    RULES:
    1. ALWAYS USE SINGULAR NAMES for the tables above.
    2. `service_point` links to `address` via `address_id`.
    3. `device` links to `service_point` via `service_point_device_rel`.
    4. To find business services for a device, join `device` -> `service_point_device_rel` -> `service_point` -> `stream` -> `stream_service` -> `business_service`.

    EVENT CODES mapping (event_raw.event_code):
    - 3: Y-Phase VT link missing (Occurrence) 
    - 4: Y-Phase VT link missing (Restoration)
    - 101: Power Failure (3 Phase) - Occurrence
    - 102: Power Failure (3 Phase) - Restoration
"""

# Gold Standard SQL
EXAMPLES = [
    {
        "question": "Show me the first 5 records of the device table",
        "sql": "SELECT * FROM device LIMIT 5;"
    },
    {
        "question": "show me the total tables",
        "sql": "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
    },
    {
        "question": "How many records are in the product table",
        "sql": "SELECT COUNT(*) FROM product;"
    },
    {
        "question": "List all devices in Raipur",
        "sql": "SELECT d.* FROM device d JOIN service_point_device_rel spdr ON d.id = spdr.device_id JOIN service_point sp ON spdr.service_point_id = sp.id JOIN address a ON sp.address_id = a.id WHERE a.city = 'Raipur';"
    },
    {
        "question": "What are the active business services for device dev__EEOT4056946?",
        "sql": "SELECT bs.* FROM business_service bs JOIN stream_service ss ON bs.id = ss.business_service_id JOIN stream s ON ss.stream_id = s.id JOIN service_point sp ON s.service_point_id = sp.id JOIN service_point_device_rel spdr ON sp.id = spdr.service_point_id WHERE spdr.device_id = 'dev__EEOT4056946' AND bs.status = 'Active';"
    },
    {
        "question": "Which cities have the most service points? List top 5.",
        "sql": "SELECT a.city, COUNT(sp.id) AS service_point_count FROM service_point sp JOIN address a ON sp.address_id = a.id GROUP BY a.city ORDER BY service_point_count DESC LIMIT 5;"
    }
]

def train_agent(agent):
    print("\n--- Starting Training Sequence ---")
    
    # 6a. Train DDL
    try:
        ddl_path = os.path.join("data", "mdm-ddl.sql")
        print(f"[Info] Using DDL file: {ddl_path}")
        if os.path.exists(ddl_path):
            with open(ddl_path, "r") as f:
                ddl_content = f.read()
            agent.agent_memory.add_ddl(ddl_content)
            print("[OK] DDL ingested successfully.")
        else:
            print(f"[Warn] Warning: {ddl_path} not found in the current directory.")
    except Exception as e:
        print(f"[Error] Error during DDL ingestion: {e}")

    # 6b. Train Business Logic
    try:
        agent.agent_memory.add_documentation(BUSINESS_CONTEXT)
        print("[OK] Business logic ingested successfully.")
    except Exception as e:
        print(f"[Error] Error during business logic ingestion: {e}")

    # 6c. Train Gold Standard SQL Queries
        # Train from internal examples list
        for ex in EXAMPLES:
            agent.agent_memory.add_sql(
                question=ex["question"],
                sql=ex["sql"]
            )
        print(f"[OK] {len(EXAMPLES)} internal SQL Examples ingested.")

        # Train from external examples.json if it exists
        examples_path = os.path.join("data", "examples.json")
        if os.path.exists(examples_path):
            import json
            with open(examples_path, "r") as f:
                ext_examples = json.load(f)
            
            for ex in ext_examples:
                agent.agent_memory.add_sql(
                    question=ex["question"],
                    sql=ex["sql"]
                )
            print(f"[OK] {len(ext_examples)} external SQL Examples ingested from {examples_path}.")
    except Exception as e:
        print(f"[Error] Error during SQL query ingestion: {e}")

    print("----------------------------------\n")
