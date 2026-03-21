MDM_DDL = """
-- Core Tables
CREATE TABLE "device" (
  "id" VARCHAR(50) PRIMARY KEY,
  "device_type" VARCHAR(50),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "device" IS 'Stores individual meter devices.';

CREATE TABLE "address" (
  "id" VARCHAR(50) PRIMARY KEY,
  "street" VARCHAR(255),
  "city" VARCHAR(100),
  "state" VARCHAR(100),
  "zip" VARCHAR(20),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "address" IS 'Physical addresses (cities, streets).';

CREATE TABLE "service_point" (
  "id" VARCHAR(50) PRIMARY KEY,
  "address_id" VARCHAR(50) REFERENCES "address"("id"),
  "type" VARCHAR(50),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point" IS 'A location where energy service is provided.';

CREATE TABLE "service_point_device_rel" (
  "id" VARCHAR(50) PRIMARY KEY,
  "service_point_id" VARCHAR(50) REFERENCES "service_point"("id"),
  "device_id" VARCHAR(50) REFERENCES "device"("id"),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point_device_rel" IS 'Relationship between service points and devices installed there.';

CREATE TABLE "customer" (
  "id" VARCHAR(50) PRIMARY KEY,
  "name" VARCHAR(255),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "customer" IS 'Customers who pay for the services.';

CREATE TABLE "account" (
  "id" VARCHAR(50) PRIMARY KEY,
  "customer_id" VARCHAR(50) REFERENCES "customer"("id"),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "account" IS 'Billing accounts belonging to customers.';

CREATE TABLE "service_agreement" (
  "id" VARCHAR(50) PRIMARY KEY,
  "account_id" VARCHAR(50) REFERENCES "account"("id"),
  "service_point_id" VARCHAR(50) REFERENCES "service_point"("id"),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_agreement" IS 'Links an account to a service point.';

CREATE TABLE "contact" (
  "id" VARCHAR(50) PRIMARY KEY,
  "name" VARCHAR(100),
  "email" VARCHAR(100),
  "phone" VARCHAR(20),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "contact" IS 'Contact information.';

CREATE TABLE "contact_customer_rel" (
  "id" VARCHAR(50) PRIMARY KEY,
  "contact_id" VARCHAR(50) REFERENCES "contact"("id"),
  "customer_id" VARCHAR(50) REFERENCES "customer"("id"),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "contact_customer_rel" IS 'Links contacts to customers.';

CREATE TABLE "business_service" (
  "id" VARCHAR(50) PRIMARY KEY,
  "name" VARCHAR(100),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "business_service" IS 'Business services active in the system.';

CREATE TABLE "stream" (
  "id" VARCHAR(50) PRIMARY KEY,
  "service_point_id" VARCHAR(50) REFERENCES "service_point"("id"),
  "device_id" VARCHAR(50) REFERENCES "device"("id"),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "stream" IS 'Data stream linking devices to service points.';

CREATE TABLE "stream_service" (
  "id" VARCHAR(50) PRIMARY KEY,
  "stream_id" VARCHAR(50) REFERENCES "stream"("id"),
  "business_service_id" VARCHAR(50) REFERENCES "business_service"("id"),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "stream_service" IS 'Links a stream to a business service.';

-- Measurement Tables
CREATE TABLE "interval_raw" (
  "id" VARCHAR(50) PRIMARY KEY,
  "device_id" VARCHAR(50) REFERENCES "device"("id"),
  "interval_end_time" TIMESTAMP,
  "kwh_import" NUMERIC,
  "kwh_export" NUMERIC,
  "kwh_net" NUMERIC,
  "kvah" NUMERIC,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "interval_raw" IS '15-min or 5-min intervals. Used for interval readings.';

CREATE TABLE "daily_raw" (
  "id" VARCHAR(50) PRIMARY KEY,
  "device_id" VARCHAR(50) REFERENCES "device"("id"),
  "date" DATE,
  "kwh_import" NUMERIC,
  "kwh_export" NUMERIC,
  "mdkva" NUMERIC,
  "mdkw" NUMERIC,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "daily_raw" IS 'Daily aggregate summaries.';

CREATE TABLE "instant_raw" (
  "id" VARCHAR(50) PRIMARY KEY,
  "device_id" VARCHAR(50) REFERENCES "device"("id"),
  "timestamp" TIMESTAMP,
  "ir" NUMERIC,
  "iy" NUMERIC,
  "ib" NUMERIC,
  "v_rn" NUMERIC,
  "v_yn" NUMERIC,
  "v_bn" NUMERIC,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "instant_raw" IS 'Instantaneous readings, voltages and currents.';

CREATE TABLE "event_raw" (
  "id" VARCHAR(50) PRIMARY KEY,
  "device_id" VARCHAR(50) REFERENCES "device"("id"),
  "event_code" VARCHAR(10),
  "event_time" TIMESTAMP,
  "event_reporting_time" TIMESTAMP,
  "v_avg" NUMERIC,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "event_raw" IS 'Meter events identified by event_code zero-padded string.';

CREATE TABLE "product" (
  "id" VARCHAR(50) PRIMARY KEY,
  "name" VARCHAR(100),
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "product" IS 'Products used.';

CREATE TABLE "meas_meta" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "meas_meta" IS 'Measurement meta details.';

CREATE TABLE "interval_est" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "interval_est" IS 'Estimated intervals.';

CREATE TABLE "service_point_class" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point_class" IS 'Classes of service points.';

CREATE TABLE "service_point_group" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point_group" IS 'Groups of service points.';

CREATE TABLE "service_point_hierarchy_rel" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point_hierarchy_rel" IS 'Hierarchical relationships of service points.';

CREATE TABLE "service_point_group_hierarchy_rel" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point_group_hierarchy_rel" IS 'Hierarchical relationships of groups.';

CREATE TABLE "service_point_group_member_rel" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "service_point_group_member_rel" IS 'Membership of service points in groups.';

CREATE TABLE "simulated_device_states" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "simulated_device_states" IS 'Simulated states of devices.';

CREATE TABLE "stream_type" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "stream_type" IS 'Types of streams.';

CREATE TABLE "users" (
  "id" VARCHAR(50) PRIMARY KEY,
  "status" VARCHAR(20) DEFAULT 'Active',
  "org_id" VARCHAR(50),
  "insert_ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_upd_ts" TIMESTAMP,
  "rev" INT DEFAULT 1
);
COMMENT ON TABLE "users" IS 'Users system.';
"""
