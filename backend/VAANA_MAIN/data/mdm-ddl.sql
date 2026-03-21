--
-- PostgreSQL database dump
--

\restrict RlTul8TpclPjzOrjAGqPpHTWoUloh10DZX4i9WW4SLEVR97464MnDdH3rctNfSy

-- Dumped from database version 15.16
-- Dumped by pg_dump version 18.1

-- Started on 2026-03-18 00:05:33

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4946 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16462)
-- Name: account; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.account (
    id character varying(50) NOT NULL,
    customer_id character varying(50) NOT NULL,
    account_number character varying(100) NOT NULL,
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.account OWNER TO mdmadmin;

--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE account; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.account IS 'ACCOUNT ||--|{ SERVICE_AGREEMENT; owned by customer';


--
-- TOC entry 215 (class 1259 OID 16429)
-- Name: address; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.address (
    id character varying(50) NOT NULL,
    address_line1 character varying(255),
    address_line2 character varying(255),
    landmark character varying(255),
    city character varying(100),
    district character varying(100),
    state character varying(100),
    pincode character varying(6),
    country character varying(100),
    latitude numeric(10,7),
    longitude numeric(10,7),
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.address OWNER TO mdmadmin;

--
-- TOC entry 4950 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE address; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.address IS 'Physical address (India: address_line1/2, landmark, district, 6-digit pincode); SERVICE_POINT }|--|| ADDRESS';


--
-- TOC entry 232 (class 1259 OID 16720)
-- Name: business_service; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.business_service (
    id character varying(50) NOT NULL,
    name character varying(255),
    type character varying(100),
    sub_type character varying(100),
    json_config jsonb,
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.business_service OWNER TO mdmadmin;

--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE business_service; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.business_service IS 'BUSINESS_SERVICE ||--|{ STREAM_SERVICE attached_to';


--
-- TOC entry 216 (class 1259 OID 16440)
-- Name: contact; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.contact (
    id character varying(50) NOT NULL,
    contact_type character varying(100) NOT NULL,
    contact_details character varying(100) NOT NULL,
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.contact OWNER TO mdmadmin;

--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE contact; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.contact IS 'Contact; CONTACT }|--|{ CUSTOMER, optionally linked to auth_user';


--
-- TOC entry 228 (class 1259 OID 16645)
-- Name: contact_customer_rel; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.contact_customer_rel (
    id character varying(50) NOT NULL,
    contact_id character varying(50) NOT NULL,
    customer_id character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.contact_customer_rel OWNER TO mdmadmin;

--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE contact_customer_rel; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.contact_customer_rel IS 'CONTACT }|--|{ CUSTOMER: many-to-many contract';


--
-- TOC entry 217 (class 1259 OID 16451)
-- Name: customer; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.customer (
    id character varying(50) NOT NULL,
    first_name character varying(255) NOT NULL,
    middle_name character varying(255),
    last_name character varying(255),
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1,
    alt_id character varying(50)
);


ALTER TABLE public.customer OWNER TO mdmadmin;

--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE customer; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.customer IS 'Customer entity (individual or organization); CUSTOMER ||--o{ ACCOUNT';


--
-- TOC entry 240 (class 1259 OID 44285)
-- Name: daily_raw; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.daily_raw (
    stream_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    read_time timestamp without time zone NOT NULL,
    kwh_export numeric(18,6),
    kwh_import numeric(18,6),
    mdkva numeric(18,6),
    mdkw numeric(18,6),
    org_id character varying(50),
    insert_ts timestamp without time zone DEFAULT now()
);


ALTER TABLE public.daily_raw OWNER TO mdmadmin;

--
-- TOC entry 220 (class 1259 OID 16491)
-- Name: device; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.device (
    id character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    alt_id character varying(50),
    device_type character varying(50),
    serial_number character varying(100),
    product_id character varying(50),
    status character varying(50) DEFAULT 'Active'::character varying,
    attr_json jsonb,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.device OWNER TO mdmadmin;

--
-- TOC entry 4961 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE device; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.device IS 'Device; instance_of PRODUCT, installed_at SERVICE_POINT, supplies STREAM_SERVICE';


--
-- TOC entry 238 (class 1259 OID 41243)
-- Name: event_raw; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.event_raw (
    stream_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    event_time timestamp without time zone NOT NULL,
    event_reporting_time timestamp without time zone,
    event_code character varying(100),
    ib numeric(18,6),
    ir numeric(18,6),
    iy numeric(18,6),
    v_avg numeric(18,6),
    v_bn numeric(18,6),
    v_rn numeric(18,6),
    v_yn numeric(18,6),
    org_id character varying(50),
    insert_ts timestamp without time zone DEFAULT now()
);


ALTER TABLE public.event_raw OWNER TO mdmadmin;

--
-- TOC entry 239 (class 1259 OID 43883)
-- Name: instant_raw; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.instant_raw (
    stream_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    read_time timestamp without time zone NOT NULL,
    ir numeric(18,6),
    iy numeric(18,6),
    ib numeric(18,6),
    v_avg numeric(18,6),
    v_rn numeric(18,6),
    v_yn numeric(18,6),
    v_bn numeric(18,6),
    org_id character varying(50),
    insert_ts timestamp without time zone DEFAULT now()
);


ALTER TABLE public.instant_raw OWNER TO mdmadmin;

--
-- TOC entry 235 (class 1259 OID 16784)
-- Name: interval_est; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.interval_est (
    stream_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    interval_end_time timestamp without time zone NOT NULL,
    org_id character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.interval_est OWNER TO mdmadmin;

--
-- TOC entry 234 (class 1259 OID 16766)
-- Name: interval_raw; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.interval_raw (
    stream_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    interval_start_time timestamp without time zone NOT NULL,
    interval_end_time timestamp without time zone NOT NULL,
    kwh_import numeric(18,6),
    kwh_export numeric(18,6),
    kwh_net numeric(18,6),
    kvah numeric(18,6),
    kvah_import numeric(18,6),
    kvah_export numeric(18,6),
    ir numeric(18,6),
    iy numeric(18,6),
    ib numeric(18,6),
    i_avg numeric(18,6),
    v_avg numeric(18,6),
    v_rn numeric(18,6),
    v_yn numeric(18,6),
    v_bn numeric(18,6),
    v_ry numeric(18,6),
    v_by numeric(18,6),
    hz numeric(18,6),
    org_id character varying(50),
    insert_ts timestamp without time zone DEFAULT now()
);


ALTER TABLE public.interval_raw OWNER TO mdmadmin;

--
-- TOC entry 331 (class 1259 OID 88954)
-- Name: meas_meta; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.meas_meta (
    id character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    display_name character varying(255),
    db_col_name character varying(100) NOT NULL,
    unit character varying(50),
    data_type character varying(50),
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.meas_meta OWNER TO mdmadmin;

--
-- TOC entry 4967 (class 0 OID 0)
-- Dependencies: 331
-- Name: TABLE meas_meta; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.meas_meta IS 'Measurement metadata catalog; maps measurement names to db columns, units, and data types';


--
-- TOC entry 219 (class 1259 OID 16478)
-- Name: product; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.product (
    id character varying(50) NOT NULL,
    name character varying(255),
    type character varying(100),
    sub_type character varying(100),
    status character varying(50) DEFAULT 'Active'::character varying,
    attr_json jsonb,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.product OWNER TO mdmadmin;

--
-- TOC entry 4969 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE product; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.product IS 'Product catalog; DEVICE }|--|| PRODUCT instance_of';


--
-- TOC entry 227 (class 1259 OID 16625)
-- Name: service_agreement; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_agreement (
    id character varying(50) NOT NULL,
    account_id character varying(50) NOT NULL,
    service_point_id character varying(50) NOT NULL,
    agreement_number character varying(100),
    start_date date NOT NULL,
    end_date date,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.service_agreement OWNER TO mdmadmin;

--
-- TOC entry 4971 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE service_agreement; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_agreement IS 'SERVICE_AGREEMENT }|--|| SERVICE_POINT; under account';


--
-- TOC entry 222 (class 1259 OID 16522)
-- Name: service_point; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point (
    id character varying(50) NOT NULL,
    address_id character varying(50) NOT NULL,
    service_point_class_id character varying(50),
    name character varying(255),
    alt_id character varying(50),
    status character varying(50) DEFAULT 'Active'::character varying,
    attr_json jsonb,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.service_point OWNER TO mdmadmin;

--
-- TOC entry 4973 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE service_point; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point IS 'SERVICE_POINT }|--|| ADDRESS, }|--|{ DEVICE, ||--|{ STREAM; classification via service_point_class';


--
-- TOC entry 221 (class 1259 OID 16511)
-- Name: service_point_class; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point_class (
    id character varying(50) NOT NULL,
    name character varying(255),
    type character varying(100),
    sub_type character varying(100),
    status character varying(50) DEFAULT 'Active'::character varying,
    attr_json jsonb,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.service_point_class OWNER TO mdmadmin;

--
-- TOC entry 4975 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE service_point_class; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point_class IS 'Service point classification; type/sub_type (exact semantics to be defined)';


--
-- TOC entry 229 (class 1259 OID 16665)
-- Name: service_point_device_rel; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point_device_rel (
    id character varying(50) NOT NULL,
    service_point_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.service_point_device_rel OWNER TO mdmadmin;

--
-- TOC entry 4977 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE service_point_device_rel; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point_device_rel IS 'SERVICE_POINT }|--|{ DEVICE: many-to-many installed';


--
-- TOC entry 224 (class 1259 OID 16568)
-- Name: service_point_group; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point_group (
    id character varying(50) NOT NULL,
    name character varying(255),
    type character varying(100),
    sub_type character varying(100),
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1,
    alt_id character varying(50)
);


ALTER TABLE public.service_point_group OWNER TO mdmadmin;

--
-- TOC entry 4979 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE service_point_group; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point_group IS 'Group of service points; membership via service_point_group_member_rel (many-to-many); type/sub_type classify the group';


--
-- TOC entry 226 (class 1259 OID 16602)
-- Name: service_point_group_hierarchy_rel; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point_group_hierarchy_rel (
    id character varying(50) NOT NULL,
    parent_group_id character varying(50) NOT NULL,
    child_group_id character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1,
    CONSTRAINT chk_sp_group_hierarchy_no_self CHECK (((parent_group_id)::text <> (child_group_id)::text))
);


ALTER TABLE public.service_point_group_hierarchy_rel OWNER TO mdmadmin;

--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE service_point_group_hierarchy_rel; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point_group_hierarchy_rel IS 'SERVICE_POINT_GROUP parent-child hierarchy; temporal validity via start_date/end_date';


--
-- TOC entry 225 (class 1259 OID 16581)
-- Name: service_point_group_member_rel; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point_group_member_rel (
    id character varying(50) NOT NULL,
    service_point_id character varying(50) NOT NULL,
    service_point_group_id character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.service_point_group_member_rel OWNER TO mdmadmin;

--
-- TOC entry 4983 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE service_point_group_member_rel; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point_group_member_rel IS 'Many-to-many: one service point in multiple groups, one group many service points; temporal validity via start_date/end_date';


--
-- TOC entry 223 (class 1259 OID 16545)
-- Name: service_point_hierarchy_rel; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.service_point_hierarchy_rel (
    id character varying(50) NOT NULL,
    parent_service_point_id character varying(50) NOT NULL,
    child_service_point_id character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1,
    CONSTRAINT chk_sp_hierarchy_no_self CHECK (((parent_service_point_id)::text <> (child_service_point_id)::text))
);


ALTER TABLE public.service_point_hierarchy_rel OWNER TO mdmadmin;

--
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE service_point_hierarchy_rel; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.service_point_hierarchy_rel IS 'SERVICE_POINT parent-child hierarchy; one parent per child, many children per parent; temporal validity via start_date/end_date';


--
-- TOC entry 236 (class 1259 OID 17224)
-- Name: simulated_device_states; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.simulated_device_states (
    serial_number character varying(50) NOT NULL,
    cumulative_wh_import double precision DEFAULT 0.0 NOT NULL,
    cumulative_varh double precision DEFAULT 0.0 NOT NULL,
    cumulative_vah_import double precision DEFAULT 0.0 NOT NULL,
    cumulative_wh_export double precision DEFAULT 0.0 NOT NULL,
    cumulative_vah_export double precision DEFAULT 0.0 NOT NULL,
    last_reading_time timestamp with time zone,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    daily_wh_import double precision DEFAULT 0.0 NOT NULL,
    daily_varh double precision DEFAULT 0.0 NOT NULL,
    daily_vah_import double precision DEFAULT 0.0 NOT NULL,
    daily_wh_export double precision DEFAULT 0.0 NOT NULL,
    daily_vah_export double precision DEFAULT 0.0 NOT NULL,
    daily_max_demand_kw double precision DEFAULT 0.0 NOT NULL,
    daily_max_demand_kva double precision DEFAULT 0.0 NOT NULL,
    daily_max_demand_kw_datetime timestamp with time zone,
    daily_max_demand_kva_datetime timestamp with time zone,
    daily_max_demand_kw_export double precision DEFAULT 0.0 NOT NULL,
    daily_max_demand_kva_export double precision DEFAULT 0.0 NOT NULL,
    daily_tod_max_demand_kw jsonb DEFAULT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::jsonb,
    daily_tod_max_demand_kva jsonb DEFAULT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::jsonb,
    daily_tod_max_demand_kw_datetime jsonb DEFAULT '[null, null, null, null, null, null, null, null]'::jsonb,
    daily_tod_max_demand_kva_datetime jsonb DEFAULT '[null, null, null, null, null, null, null, null]'::jsonb,
    daily_tod_cumulative_kwh jsonb DEFAULT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::jsonb,
    daily_tod_cumulative_kvah jsonb DEFAULT '[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'::jsonb,
    last_daily_reset_date date,
    pending_event_restorations jsonb DEFAULT '[]'::jsonb,
    CONSTRAINT check_cumulative_vah_export_non_negative CHECK ((cumulative_vah_export >= (0)::double precision)),
    CONSTRAINT check_cumulative_vah_import_non_negative CHECK ((cumulative_vah_import >= (0)::double precision)),
    CONSTRAINT check_cumulative_varh_non_negative CHECK ((cumulative_varh >= (0)::double precision)),
    CONSTRAINT check_cumulative_wh_export_non_negative CHECK ((cumulative_wh_export >= (0)::double precision)),
    CONSTRAINT check_cumulative_wh_import_non_negative CHECK ((cumulative_wh_import >= (0)::double precision)),
    CONSTRAINT check_daily_max_demand_kva_non_negative CHECK ((daily_max_demand_kva >= (0)::double precision)),
    CONSTRAINT check_daily_max_demand_kw_non_negative CHECK ((daily_max_demand_kw >= (0)::double precision)),
    CONSTRAINT check_daily_vah_export_non_negative CHECK ((daily_vah_export >= (0)::double precision)),
    CONSTRAINT check_daily_vah_import_non_negative CHECK ((daily_vah_import >= (0)::double precision)),
    CONSTRAINT check_daily_varh_non_negative CHECK ((daily_varh >= (0)::double precision)),
    CONSTRAINT check_daily_wh_export_non_negative CHECK ((daily_wh_export >= (0)::double precision)),
    CONSTRAINT check_daily_wh_import_non_negative CHECK ((daily_wh_import >= (0)::double precision)),
    CONSTRAINT check_vah_export_ge_wh_export CHECK ((cumulative_vah_export >= cumulative_wh_export)),
    CONSTRAINT check_vah_ge_wh CHECK ((cumulative_vah_import >= cumulative_wh_import))
);


ALTER TABLE public.simulated_device_states OWNER TO mdmadmin;

--
-- TOC entry 4987 (class 0 OID 0)
-- Dependencies: 236
-- Name: COLUMN simulated_device_states.pending_event_restorations; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON COLUMN public.simulated_device_states.pending_event_restorations IS 'List of pending occurrence/restoration pairs';


--
-- TOC entry 231 (class 1259 OID 16698)
-- Name: stream; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.stream (
    id character varying(50) NOT NULL,
    stream_type_id character varying(50) NOT NULL,
    service_point_id character varying(50) NOT NULL,
    name character varying(255),
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.stream OWNER TO mdmadmin;

--
-- TOC entry 4989 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE stream; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.stream IS 'STREAM_TYPE, SERVICE_POINT ||--|{ STREAM instance_of';


--
-- TOC entry 233 (class 1259 OID 16733)
-- Name: stream_service; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.stream_service (
    id character varying(50) NOT NULL,
    business_service_id character varying(50) NOT NULL,
    stream_id character varying(50) NOT NULL,
    device_id character varying(50) NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.stream_service OWNER TO mdmadmin;

--
-- TOC entry 4991 (class 0 OID 0)
-- Dependencies: 233
-- Name: TABLE stream_service; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.stream_service IS 'BUSINESS_SERVICE, STREAM, DEVICE ||--|{ STREAM_SERVICE attached_to/supplies';


--
-- TOC entry 230 (class 1259 OID 16685)
-- Name: stream_type; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.stream_type (
    id character varying(50) NOT NULL,
    name character varying(255),
    type character varying(100),
    sub_type character varying(100),
    json_config jsonb,
    status character varying(50) DEFAULT 'Active'::character varying,
    org_id character varying(50),
    insert_by character varying(50),
    last_upd_by character varying(50),
    insert_ts timestamp without time zone DEFAULT now(),
    last_upd_ts timestamp without time zone DEFAULT now(),
    rev integer DEFAULT 1
);


ALTER TABLE public.stream_type OWNER TO mdmadmin;

--
-- TOC entry 4993 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE stream_type; Type: COMMENT; Schema: public; Owner: mdmadmin
--

COMMENT ON TABLE public.stream_type IS 'STREAM_TYPE ||--|{ STREAM_VARIABLE, STREAM';


--
-- TOC entry 237 (class 1259 OID 32148)
-- Name: users; Type: TABLE; Schema: public; Owner: mdmadmin
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    created_on timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_on timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status character varying(50) DEFAULT 'active'::character varying NOT NULL
);


ALTER TABLE public.users OWNER TO mdmadmin;

--
-- TOC entry 4644 (class 2606 OID 16470)
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- TOC entry 4636 (class 2606 OID 16439)
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);


--
-- TOC entry 4723 (class 2606 OID 16730)
-- Name: business_service business_service_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.business_service
    ADD CONSTRAINT business_service_pkey PRIMARY KEY (id);


--
-- TOC entry 4701 (class 2606 OID 16652)
-- Name: contact_customer_rel contact_customer_rel_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.contact_customer_rel
    ADD CONSTRAINT contact_customer_rel_pkey PRIMARY KEY (id);


--
-- TOC entry 4638 (class 2606 OID 16448)
-- Name: contact contact_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id);


--
-- TOC entry 4642 (class 2606 OID 16461)
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- TOC entry 4653 (class 2606 OID 16501)
-- Name: device device_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.device
    ADD CONSTRAINT device_pkey PRIMARY KEY (id);


--
-- TOC entry 4773 (class 2606 OID 88964)
-- Name: meas_meta meas_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.meas_meta
    ADD CONSTRAINT meas_meta_pkey PRIMARY KEY (id);


--
-- TOC entry 4649 (class 2606 OID 16488)
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- TOC entry 4697 (class 2606 OID 16632)
-- Name: service_agreement service_agreement_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_agreement
    ADD CONSTRAINT service_agreement_pkey PRIMARY KEY (id);


--
-- TOC entry 4660 (class 2606 OID 16521)
-- Name: service_point_class service_point_class_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_class
    ADD CONSTRAINT service_point_class_pkey PRIMARY KEY (id);


--
-- TOC entry 4709 (class 2606 OID 16672)
-- Name: service_point_device_rel service_point_device_rel_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_device_rel
    ADD CONSTRAINT service_point_device_rel_pkey PRIMARY KEY (id);


--
-- TOC entry 4689 (class 2606 OID 16610)
-- Name: service_point_group_hierarchy_rel service_point_group_hierarchy_rel_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_hierarchy_rel
    ADD CONSTRAINT service_point_group_hierarchy_rel_pkey PRIMARY KEY (id);


--
-- TOC entry 4682 (class 2606 OID 16588)
-- Name: service_point_group_member_rel service_point_group_member_rel_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_member_rel
    ADD CONSTRAINT service_point_group_member_rel_pkey PRIMARY KEY (id);


--
-- TOC entry 4676 (class 2606 OID 16578)
-- Name: service_point_group service_point_group_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group
    ADD CONSTRAINT service_point_group_pkey PRIMARY KEY (id);


--
-- TOC entry 4670 (class 2606 OID 16553)
-- Name: service_point_hierarchy_rel service_point_hierarchy_rel_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_hierarchy_rel
    ADD CONSTRAINT service_point_hierarchy_rel_pkey PRIMARY KEY (id);


--
-- TOC entry 4664 (class 2606 OID 16532)
-- Name: service_point service_point_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point
    ADD CONSTRAINT service_point_pkey PRIMARY KEY (id);


--
-- TOC entry 4719 (class 2606 OID 16707)
-- Name: stream stream_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream
    ADD CONSTRAINT stream_pkey PRIMARY KEY (id);


--
-- TOC entry 4730 (class 2606 OID 16740)
-- Name: stream_service stream_service_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_service
    ADD CONSTRAINT stream_service_pkey PRIMARY KEY (id);


--
-- TOC entry 4713 (class 2606 OID 16695)
-- Name: stream_type stream_type_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_type
    ADD CONSTRAINT stream_type_pkey PRIMARY KEY (id);


--
-- TOC entry 4647 (class 2606 OID 16472)
-- Name: account uk_account_org_number; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT uk_account_org_number UNIQUE (org_id, account_number);


--
-- TOC entry 4725 (class 2606 OID 16732)
-- Name: business_service uk_business_service_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.business_service
    ADD CONSTRAINT uk_business_service_org_name UNIQUE (org_id, name);


--
-- TOC entry 4705 (class 2606 OID 16654)
-- Name: contact_customer_rel uk_contact_customer_rel_org_contact_customer; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.contact_customer_rel
    ADD CONSTRAINT uk_contact_customer_rel_org_contact_customer UNIQUE (org_id, contact_id, customer_id);


--
-- TOC entry 4640 (class 2606 OID 16450)
-- Name: contact uk_contact_org_type_details; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.contact
    ADD CONSTRAINT uk_contact_org_type_details UNIQUE (org_id, contact_type, contact_details);


--
-- TOC entry 4771 (class 2606 OID 44290)
-- Name: daily_raw uk_daily_raw; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.daily_raw
    ADD CONSTRAINT uk_daily_raw UNIQUE (stream_id, device_id, org_id, read_time);


--
-- TOC entry 4656 (class 2606 OID 16505)
-- Name: device uk_device_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.device
    ADD CONSTRAINT uk_device_org_name UNIQUE (org_id, name);


--
-- TOC entry 4658 (class 2606 OID 16503)
-- Name: device uk_device_serial_number; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.device
    ADD CONSTRAINT uk_device_serial_number UNIQUE (serial_number);


--
-- TOC entry 4759 (class 2606 OID 67575)
-- Name: event_raw uk_event_raw; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.event_raw
    ADD CONSTRAINT uk_event_raw UNIQUE (stream_id, device_id, org_id, event_time, event_code);


--
-- TOC entry 4765 (class 2606 OID 43888)
-- Name: instant_raw uk_instant_raw; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.instant_raw
    ADD CONSTRAINT uk_instant_raw UNIQUE (stream_id, device_id, org_id, read_time);


--
-- TOC entry 4746 (class 2606 OID 16791)
-- Name: interval_est uk_interval_est; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.interval_est
    ADD CONSTRAINT uk_interval_est UNIQUE (stream_id, device_id, org_id, interval_end_time, rev);


--
-- TOC entry 4740 (class 2606 OID 16771)
-- Name: interval_raw uk_interval_raw; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.interval_raw
    ADD CONSTRAINT uk_interval_raw UNIQUE (stream_id, device_id, org_id, interval_end_time);


--
-- TOC entry 4775 (class 2606 OID 88968)
-- Name: meas_meta uk_meas_meta_org_db_col_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.meas_meta
    ADD CONSTRAINT uk_meas_meta_org_db_col_name UNIQUE (org_id, db_col_name);


--
-- TOC entry 4777 (class 2606 OID 88966)
-- Name: meas_meta uk_meas_meta_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.meas_meta
    ADD CONSTRAINT uk_meas_meta_org_name UNIQUE (org_id, name);


--
-- TOC entry 4651 (class 2606 OID 16490)
-- Name: product uk_product_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT uk_product_org_name UNIQUE (org_id, name);


--
-- TOC entry 4699 (class 2606 OID 16634)
-- Name: service_agreement uk_service_agreement_org_number; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_agreement
    ADD CONSTRAINT uk_service_agreement_org_number UNIQUE (org_id, agreement_number);


--
-- TOC entry 4711 (class 2606 OID 16674)
-- Name: service_point_device_rel uk_service_point_device_rel_org_sp_device; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_device_rel
    ADD CONSTRAINT uk_service_point_device_rel_org_sp_device UNIQUE (org_id, service_point_id, device_id);


--
-- TOC entry 4678 (class 2606 OID 16580)
-- Name: service_point_group uk_service_point_group_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group
    ADD CONSTRAINT uk_service_point_group_org_name UNIQUE (org_id, name);


--
-- TOC entry 4666 (class 2606 OID 16534)
-- Name: service_point uk_service_point_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point
    ADD CONSTRAINT uk_service_point_org_name UNIQUE (org_id, name);


--
-- TOC entry 4693 (class 2606 OID 16612)
-- Name: service_point_group_hierarchy_rel uk_sp_group_hierarchy_rel_org_parent_child_end; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_hierarchy_rel
    ADD CONSTRAINT uk_sp_group_hierarchy_rel_org_parent_child_end UNIQUE (org_id, parent_group_id, child_group_id, end_date);


--
-- TOC entry 4685 (class 2606 OID 16590)
-- Name: service_point_group_member_rel uk_sp_group_member_rel_org_sp_group_end; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_member_rel
    ADD CONSTRAINT uk_sp_group_member_rel_org_sp_group_end UNIQUE (org_id, service_point_id, service_point_group_id, end_date);


--
-- TOC entry 4674 (class 2606 OID 16555)
-- Name: service_point_hierarchy_rel uk_sp_hierarchy_rel_org_parent_child_end; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_hierarchy_rel
    ADD CONSTRAINT uk_sp_hierarchy_rel_org_parent_child_end UNIQUE (org_id, parent_service_point_id, child_service_point_id, end_date);


--
-- TOC entry 4733 (class 2606 OID 16742)
-- Name: stream_service uk_stream_service_biz_stream_device; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_service
    ADD CONSTRAINT uk_stream_service_biz_stream_device UNIQUE (business_service_id, stream_id, device_id);


--
-- TOC entry 4721 (class 2606 OID 16709)
-- Name: stream uk_stream_service_point_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream
    ADD CONSTRAINT uk_stream_service_point_name UNIQUE (service_point_id, name);


--
-- TOC entry 4715 (class 2606 OID 16697)
-- Name: stream_type uk_stream_type_org_name; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_type
    ADD CONSTRAINT uk_stream_type_org_name UNIQUE (org_id, name);


--
-- TOC entry 4750 (class 2606 OID 32160)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4752 (class 2606 OID 32158)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4645 (class 1259 OID 18595)
-- Name: idx_account_customer_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_account_customer_id ON public.account USING btree (customer_id);


--
-- TOC entry 4702 (class 1259 OID 18607)
-- Name: idx_contact_customer_rel_contact_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_contact_customer_rel_contact_id ON public.contact_customer_rel USING btree (contact_id);


--
-- TOC entry 4703 (class 1259 OID 18608)
-- Name: idx_contact_customer_rel_customer_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_contact_customer_rel_customer_id ON public.contact_customer_rel USING btree (customer_id);


--
-- TOC entry 4766 (class 1259 OID 65943)
-- Name: idx_daily_raw_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_daily_raw_device_id ON public.daily_raw USING btree (device_id);


--
-- TOC entry 4767 (class 1259 OID 65945)
-- Name: idx_daily_raw_org_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_daily_raw_org_id ON public.daily_raw USING btree (org_id);


--
-- TOC entry 4768 (class 1259 OID 65944)
-- Name: idx_daily_raw_read_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_daily_raw_read_time ON public.daily_raw USING btree (read_time);


--
-- TOC entry 4769 (class 1259 OID 65942)
-- Name: idx_daily_raw_stream_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_daily_raw_stream_id ON public.daily_raw USING btree (stream_id);


--
-- TOC entry 4654 (class 1259 OID 18596)
-- Name: idx_device_product_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_device_product_id ON public.device USING btree (product_id);


--
-- TOC entry 4753 (class 1259 OID 65981)
-- Name: idx_event_raw_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_event_raw_device_id ON public.event_raw USING btree (device_id);


--
-- TOC entry 4754 (class 1259 OID 65983)
-- Name: idx_event_raw_event_reporting_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_event_raw_event_reporting_time ON public.event_raw USING btree (event_reporting_time);


--
-- TOC entry 4755 (class 1259 OID 65982)
-- Name: idx_event_raw_event_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_event_raw_event_time ON public.event_raw USING btree (event_time);


--
-- TOC entry 4756 (class 1259 OID 65984)
-- Name: idx_event_raw_org_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_event_raw_org_id ON public.event_raw USING btree (org_id);


--
-- TOC entry 4757 (class 1259 OID 65950)
-- Name: idx_event_raw_stream_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_event_raw_stream_id ON public.event_raw USING btree (stream_id);


--
-- TOC entry 4760 (class 1259 OID 65939)
-- Name: idx_instant_raw_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_instant_raw_device_id ON public.instant_raw USING btree (device_id);


--
-- TOC entry 4761 (class 1259 OID 65941)
-- Name: idx_instant_raw_org_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_instant_raw_org_id ON public.instant_raw USING btree (org_id);


--
-- TOC entry 4762 (class 1259 OID 65940)
-- Name: idx_instant_raw_read_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_instant_raw_read_time ON public.instant_raw USING btree (read_time);


--
-- TOC entry 4763 (class 1259 OID 65938)
-- Name: idx_instant_raw_stream_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_instant_raw_stream_id ON public.instant_raw USING btree (stream_id);


--
-- TOC entry 4741 (class 1259 OID 65947)
-- Name: idx_interval_est_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_est_device_id ON public.interval_est USING btree (device_id);


--
-- TOC entry 4742 (class 1259 OID 65948)
-- Name: idx_interval_est_interval_end_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_est_interval_end_time ON public.interval_est USING btree (interval_end_time);


--
-- TOC entry 4743 (class 1259 OID 65949)
-- Name: idx_interval_est_org_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_est_org_id ON public.interval_est USING btree (org_id);


--
-- TOC entry 4744 (class 1259 OID 65946)
-- Name: idx_interval_est_stream_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_est_stream_id ON public.interval_est USING btree (stream_id);


--
-- TOC entry 4734 (class 1259 OID 66196)
-- Name: idx_interval_raw_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_raw_device_id ON public.interval_raw USING btree (device_id);


--
-- TOC entry 4735 (class 1259 OID 66278)
-- Name: idx_interval_raw_interval_end_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_raw_interval_end_time ON public.interval_raw USING btree (interval_end_time);


--
-- TOC entry 4736 (class 1259 OID 66277)
-- Name: idx_interval_raw_interval_start_time; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_raw_interval_start_time ON public.interval_raw USING btree (interval_start_time);


--
-- TOC entry 4737 (class 1259 OID 66315)
-- Name: idx_interval_raw_org_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_raw_org_id ON public.interval_raw USING btree (org_id);


--
-- TOC entry 4738 (class 1259 OID 66135)
-- Name: idx_interval_raw_stream_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_interval_raw_stream_id ON public.interval_raw USING btree (stream_id);


--
-- TOC entry 4694 (class 1259 OID 18605)
-- Name: idx_service_agreement_account_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_agreement_account_id ON public.service_agreement USING btree (account_id);


--
-- TOC entry 4695 (class 1259 OID 18606)
-- Name: idx_service_agreement_service_point_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_agreement_service_point_id ON public.service_agreement USING btree (service_point_id);


--
-- TOC entry 4661 (class 1259 OID 18597)
-- Name: idx_service_point_address_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_address_id ON public.service_point USING btree (address_id);


--
-- TOC entry 4706 (class 1259 OID 18610)
-- Name: idx_service_point_device_rel_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_device_rel_device_id ON public.service_point_device_rel USING btree (device_id);


--
-- TOC entry 4707 (class 1259 OID 18609)
-- Name: idx_service_point_device_rel_service_point_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_device_rel_service_point_id ON public.service_point_device_rel USING btree (service_point_id);


--
-- TOC entry 4686 (class 1259 OID 18604)
-- Name: idx_service_point_group_hierarchy_rel_child_group_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_group_hierarchy_rel_child_group_id ON public.service_point_group_hierarchy_rel USING btree (child_group_id);


--
-- TOC entry 4687 (class 1259 OID 18603)
-- Name: idx_service_point_group_hierarchy_rel_parent_group_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_group_hierarchy_rel_parent_group_id ON public.service_point_group_hierarchy_rel USING btree (parent_group_id);


--
-- TOC entry 4679 (class 1259 OID 18602)
-- Name: idx_service_point_group_member_rel_service_point_group_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_group_member_rel_service_point_group_id ON public.service_point_group_member_rel USING btree (service_point_group_id);


--
-- TOC entry 4680 (class 1259 OID 18601)
-- Name: idx_service_point_group_member_rel_service_point_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_group_member_rel_service_point_id ON public.service_point_group_member_rel USING btree (service_point_id);


--
-- TOC entry 4667 (class 1259 OID 18600)
-- Name: idx_service_point_hierarchy_rel_child_service_point_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_hierarchy_rel_child_service_point_id ON public.service_point_hierarchy_rel USING btree (child_service_point_id);


--
-- TOC entry 4668 (class 1259 OID 18599)
-- Name: idx_service_point_hierarchy_rel_parent_service_point_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_hierarchy_rel_parent_service_point_id ON public.service_point_hierarchy_rel USING btree (parent_service_point_id);


--
-- TOC entry 4662 (class 1259 OID 18598)
-- Name: idx_service_point_service_point_class_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_service_point_service_point_class_id ON public.service_point USING btree (service_point_class_id);


--
-- TOC entry 4726 (class 1259 OID 18613)
-- Name: idx_stream_service_business_service_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_stream_service_business_service_id ON public.stream_service USING btree (business_service_id);


--
-- TOC entry 4727 (class 1259 OID 18615)
-- Name: idx_stream_service_device_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_stream_service_device_id ON public.stream_service USING btree (device_id);


--
-- TOC entry 4716 (class 1259 OID 18612)
-- Name: idx_stream_service_point_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_stream_service_point_id ON public.stream USING btree (service_point_id);


--
-- TOC entry 4728 (class 1259 OID 18614)
-- Name: idx_stream_service_stream_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_stream_service_stream_id ON public.stream_service USING btree (stream_id);


--
-- TOC entry 4717 (class 1259 OID 18611)
-- Name: idx_stream_stream_type_id; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_stream_stream_type_id ON public.stream USING btree (stream_type_id);


--
-- TOC entry 4747 (class 1259 OID 32161)
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- TOC entry 4748 (class 1259 OID 32162)
-- Name: idx_users_status; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX idx_users_status ON public.users USING btree (status);


--
-- TOC entry 4731 (class 1259 OID 16758)
-- Name: stream_service_stream_device_org_idx; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE INDEX stream_service_stream_device_org_idx ON public.stream_service USING btree (stream_id, device_id, org_id);


--
-- TOC entry 4690 (class 1259 OID 16623)
-- Name: uk_sp_group_hierarchy_rel_active_per_pair; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE UNIQUE INDEX uk_sp_group_hierarchy_rel_active_per_pair ON public.service_point_group_hierarchy_rel USING btree (org_id, parent_group_id, child_group_id) WHERE (end_date IS NULL);


--
-- TOC entry 4691 (class 1259 OID 16624)
-- Name: uk_sp_group_hierarchy_rel_one_parent_per_child; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE UNIQUE INDEX uk_sp_group_hierarchy_rel_one_parent_per_child ON public.service_point_group_hierarchy_rel USING btree (child_group_id) WHERE (end_date IS NULL);


--
-- TOC entry 4683 (class 1259 OID 16601)
-- Name: uk_sp_group_member_rel_active_per_pair; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE UNIQUE INDEX uk_sp_group_member_rel_active_per_pair ON public.service_point_group_member_rel USING btree (org_id, service_point_id, service_point_group_id) WHERE (end_date IS NULL);


--
-- TOC entry 4671 (class 1259 OID 16566)
-- Name: uk_sp_hierarchy_rel_active_per_pair; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE UNIQUE INDEX uk_sp_hierarchy_rel_active_per_pair ON public.service_point_hierarchy_rel USING btree (org_id, parent_service_point_id, child_service_point_id) WHERE (end_date IS NULL);


--
-- TOC entry 4672 (class 1259 OID 16567)
-- Name: uk_sp_hierarchy_rel_one_parent_per_child; Type: INDEX; Schema: public; Owner: mdmadmin
--

CREATE UNIQUE INDEX uk_sp_hierarchy_rel_one_parent_per_child ON public.service_point_hierarchy_rel USING btree (child_service_point_id) WHERE (end_date IS NULL);


--
-- TOC entry 4778 (class 2606 OID 16473)
-- Name: account account_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(id);


--
-- TOC entry 4790 (class 2606 OID 16655)
-- Name: contact_customer_rel contact_customer_rel_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.contact_customer_rel
    ADD CONSTRAINT contact_customer_rel_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contact(id);


--
-- TOC entry 4791 (class 2606 OID 16660)
-- Name: contact_customer_rel contact_customer_rel_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.contact_customer_rel
    ADD CONSTRAINT contact_customer_rel_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(id);


--
-- TOC entry 4779 (class 2606 OID 16506)
-- Name: device device_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.device
    ADD CONSTRAINT device_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- TOC entry 4788 (class 2606 OID 16635)
-- Name: service_agreement service_agreement_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_agreement
    ADD CONSTRAINT service_agreement_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id);


--
-- TOC entry 4789 (class 2606 OID 16640)
-- Name: service_agreement service_agreement_service_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_agreement
    ADD CONSTRAINT service_agreement_service_point_id_fkey FOREIGN KEY (service_point_id) REFERENCES public.service_point(id);


--
-- TOC entry 4780 (class 2606 OID 16535)
-- Name: service_point service_point_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point
    ADD CONSTRAINT service_point_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.address(id);


--
-- TOC entry 4792 (class 2606 OID 16680)
-- Name: service_point_device_rel service_point_device_rel_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_device_rel
    ADD CONSTRAINT service_point_device_rel_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.device(id);


--
-- TOC entry 4793 (class 2606 OID 16675)
-- Name: service_point_device_rel service_point_device_rel_service_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_device_rel
    ADD CONSTRAINT service_point_device_rel_service_point_id_fkey FOREIGN KEY (service_point_id) REFERENCES public.service_point(id);


--
-- TOC entry 4786 (class 2606 OID 16618)
-- Name: service_point_group_hierarchy_rel service_point_group_hierarchy_rel_child_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_hierarchy_rel
    ADD CONSTRAINT service_point_group_hierarchy_rel_child_group_id_fkey FOREIGN KEY (child_group_id) REFERENCES public.service_point_group(id);


--
-- TOC entry 4787 (class 2606 OID 16613)
-- Name: service_point_group_hierarchy_rel service_point_group_hierarchy_rel_parent_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_hierarchy_rel
    ADD CONSTRAINT service_point_group_hierarchy_rel_parent_group_id_fkey FOREIGN KEY (parent_group_id) REFERENCES public.service_point_group(id);


--
-- TOC entry 4784 (class 2606 OID 16596)
-- Name: service_point_group_member_rel service_point_group_member_rel_service_point_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_member_rel
    ADD CONSTRAINT service_point_group_member_rel_service_point_group_id_fkey FOREIGN KEY (service_point_group_id) REFERENCES public.service_point_group(id);


--
-- TOC entry 4785 (class 2606 OID 16591)
-- Name: service_point_group_member_rel service_point_group_member_rel_service_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_group_member_rel
    ADD CONSTRAINT service_point_group_member_rel_service_point_id_fkey FOREIGN KEY (service_point_id) REFERENCES public.service_point(id);


--
-- TOC entry 4782 (class 2606 OID 16561)
-- Name: service_point_hierarchy_rel service_point_hierarchy_rel_child_service_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_hierarchy_rel
    ADD CONSTRAINT service_point_hierarchy_rel_child_service_point_id_fkey FOREIGN KEY (child_service_point_id) REFERENCES public.service_point(id);


--
-- TOC entry 4783 (class 2606 OID 16556)
-- Name: service_point_hierarchy_rel service_point_hierarchy_rel_parent_service_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point_hierarchy_rel
    ADD CONSTRAINT service_point_hierarchy_rel_parent_service_point_id_fkey FOREIGN KEY (parent_service_point_id) REFERENCES public.service_point(id);


--
-- TOC entry 4781 (class 2606 OID 16540)
-- Name: service_point service_point_service_point_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.service_point
    ADD CONSTRAINT service_point_service_point_class_id_fkey FOREIGN KEY (service_point_class_id) REFERENCES public.service_point_class(id);


--
-- TOC entry 4796 (class 2606 OID 16743)
-- Name: stream_service stream_service_business_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_service
    ADD CONSTRAINT stream_service_business_service_id_fkey FOREIGN KEY (business_service_id) REFERENCES public.business_service(id);


--
-- TOC entry 4797 (class 2606 OID 16753)
-- Name: stream_service stream_service_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_service
    ADD CONSTRAINT stream_service_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.device(id);


--
-- TOC entry 4794 (class 2606 OID 16715)
-- Name: stream stream_service_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream
    ADD CONSTRAINT stream_service_point_id_fkey FOREIGN KEY (service_point_id) REFERENCES public.service_point(id);


--
-- TOC entry 4798 (class 2606 OID 16748)
-- Name: stream_service stream_service_stream_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream_service
    ADD CONSTRAINT stream_service_stream_id_fkey FOREIGN KEY (stream_id) REFERENCES public.stream(id);


--
-- TOC entry 4795 (class 2606 OID 16710)
-- Name: stream stream_stream_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mdmadmin
--

ALTER TABLE ONLY public.stream
    ADD CONSTRAINT stream_stream_type_id_fkey FOREIGN KEY (stream_type_id) REFERENCES public.stream_type(id);


--
-- TOC entry 4947 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO hes_user;
GRANT USAGE ON SCHEMA public TO rag_user;


--
-- TOC entry 4949 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE account; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.account TO hes_user;
GRANT SELECT ON TABLE public.account TO rag_user;


--
-- TOC entry 4951 (class 0 OID 0)
-- Dependencies: 215
-- Name: TABLE address; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.address TO hes_user;
GRANT SELECT ON TABLE public.address TO rag_user;


--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE business_service; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.business_service TO hes_user;
GRANT SELECT ON TABLE public.business_service TO rag_user;


--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE contact; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.contact TO hes_user;
GRANT SELECT ON TABLE public.contact TO rag_user;


--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE contact_customer_rel; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.contact_customer_rel TO hes_user;
GRANT SELECT ON TABLE public.contact_customer_rel TO rag_user;


--
-- TOC entry 4959 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE customer; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.customer TO hes_user;
GRANT SELECT ON TABLE public.customer TO rag_user;


--
-- TOC entry 4960 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE daily_raw; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.daily_raw TO hes_user;
GRANT SELECT ON TABLE public.daily_raw TO rag_user;


--
-- TOC entry 4962 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE device; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.device TO hes_user;
GRANT SELECT ON TABLE public.device TO rag_user;


--
-- TOC entry 4963 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE event_raw; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.event_raw TO hes_user;
GRANT SELECT ON TABLE public.event_raw TO rag_user;


--
-- TOC entry 4964 (class 0 OID 0)
-- Dependencies: 239
-- Name: TABLE instant_raw; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.instant_raw TO hes_user;
GRANT SELECT ON TABLE public.instant_raw TO rag_user;


--
-- TOC entry 4965 (class 0 OID 0)
-- Dependencies: 235
-- Name: TABLE interval_est; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.interval_est TO hes_user;
GRANT SELECT ON TABLE public.interval_est TO rag_user;


--
-- TOC entry 4966 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE interval_raw; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.interval_raw TO hes_user;
GRANT SELECT ON TABLE public.interval_raw TO rag_user;


--
-- TOC entry 4968 (class 0 OID 0)
-- Dependencies: 331
-- Name: TABLE meas_meta; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.meas_meta TO hes_user;
GRANT SELECT ON TABLE public.meas_meta TO rag_user;


--
-- TOC entry 4970 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE product; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.product TO hes_user;
GRANT SELECT ON TABLE public.product TO rag_user;


--
-- TOC entry 4972 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE service_agreement; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_agreement TO hes_user;
GRANT SELECT ON TABLE public.service_agreement TO rag_user;


--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE service_point; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point TO hes_user;
GRANT SELECT ON TABLE public.service_point TO rag_user;


--
-- TOC entry 4976 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE service_point_class; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point_class TO hes_user;
GRANT SELECT ON TABLE public.service_point_class TO rag_user;


--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE service_point_device_rel; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point_device_rel TO hes_user;
GRANT SELECT ON TABLE public.service_point_device_rel TO rag_user;


--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE service_point_group; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point_group TO hes_user;
GRANT SELECT ON TABLE public.service_point_group TO rag_user;


--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE service_point_group_hierarchy_rel; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point_group_hierarchy_rel TO hes_user;
GRANT SELECT ON TABLE public.service_point_group_hierarchy_rel TO rag_user;


--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE service_point_group_member_rel; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point_group_member_rel TO hes_user;
GRANT SELECT ON TABLE public.service_point_group_member_rel TO rag_user;


--
-- TOC entry 4986 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE service_point_hierarchy_rel; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.service_point_hierarchy_rel TO hes_user;
GRANT SELECT ON TABLE public.service_point_hierarchy_rel TO rag_user;


--
-- TOC entry 4988 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE simulated_device_states; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.simulated_device_states TO hes_user;
GRANT SELECT ON TABLE public.simulated_device_states TO rag_user;


--
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE stream; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.stream TO hes_user;
GRANT SELECT ON TABLE public.stream TO rag_user;


--
-- TOC entry 4992 (class 0 OID 0)
-- Dependencies: 233
-- Name: TABLE stream_service; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.stream_service TO hes_user;
GRANT SELECT ON TABLE public.stream_service TO rag_user;


--
-- TOC entry 4994 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE stream_type; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT ON TABLE public.stream_type TO hes_user;
GRANT SELECT ON TABLE public.stream_type TO rag_user;


--
-- TOC entry 4995 (class 0 OID 0)
-- Dependencies: 237
-- Name: TABLE users; Type: ACL; Schema: public; Owner: mdmadmin
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.users TO hes_user;
GRANT SELECT ON TABLE public.users TO rag_user;


--
-- TOC entry 2412 (class 826 OID 16840)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: mdmadmin
--

ALTER DEFAULT PRIVILEGES FOR ROLE mdmadmin IN SCHEMA public GRANT SELECT ON TABLES TO hes_user;
ALTER DEFAULT PRIVILEGES FOR ROLE mdmadmin IN SCHEMA public GRANT SELECT ON TABLES TO rag_user;


-- Completed on 2026-03-18 00:05:37

--
-- PostgreSQL database dump complete
--

\unrestrict RlTul8TpclPjzOrjAGqPpHTWoUloh10DZX4i9WW4SLEVR97464MnDdH3rctNfSy

