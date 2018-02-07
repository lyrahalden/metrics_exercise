--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.10
-- Dumped by pg_dump version 9.5.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE brands (
    brand_id integer NOT NULL,
    brand_name character varying(80)
);


ALTER TABLE brands OWNER TO vagrant;

--
-- Name: brands_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE brands_brand_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brands_brand_id_seq OWNER TO vagrant;

--
-- Name: brands_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE brands_brand_id_seq OWNED BY brands.brand_id;


--
-- Name: households; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE households (
    household_id integer NOT NULL,
    user_id integer
);


ALTER TABLE households OWNER TO vagrant;

--
-- Name: households_household_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE households_household_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE households_household_id_seq OWNER TO vagrant;

--
-- Name: households_household_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE households_household_id_seq OWNED BY households.household_id;


--
-- Name: purchases; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE purchases (
    purchase_id integer NOT NULL,
    household_id integer NOT NULL,
    brand_id integer NOT NULL,
    retailer_id integer NOT NULL,
    date timestamp without time zone
);


ALTER TABLE purchases OWNER TO vagrant;

--
-- Name: purchases_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE purchases_purchase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE purchases_purchase_id_seq OWNER TO vagrant;

--
-- Name: purchases_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE purchases_purchase_id_seq OWNED BY purchases.purchase_id;


--
-- Name: retailers; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE retailers (
    retailer_id integer NOT NULL,
    retailer_name character varying(80)
);


ALTER TABLE retailers OWNER TO vagrant;

--
-- Name: retailers_retailer_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE retailers_retailer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE retailers_retailer_id_seq OWNER TO vagrant;

--
-- Name: retailers_retailer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE retailers_retailer_id_seq OWNED BY retailers.retailer_id;


--
-- Name: brand_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY brands ALTER COLUMN brand_id SET DEFAULT nextval('brands_brand_id_seq'::regclass);


--
-- Name: household_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY households ALTER COLUMN household_id SET DEFAULT nextval('households_household_id_seq'::regclass);


--
-- Name: purchase_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY purchases ALTER COLUMN purchase_id SET DEFAULT nextval('purchases_purchase_id_seq'::regclass);


--
-- Name: retailer_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY retailers ALTER COLUMN retailer_id SET DEFAULT nextval('retailers_retailer_id_seq'::regclass);


--
-- Data for Name: brands; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY brands (brand_id, brand_name) FROM stdin;
\.


--
-- Name: brands_brand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('brands_brand_id_seq', 1, false);


--
-- Data for Name: households; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY households (household_id, user_id) FROM stdin;
\.


--
-- Name: households_household_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('households_household_id_seq', 1, false);


--
-- Data for Name: purchases; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY purchases (purchase_id, household_id, brand_id, retailer_id, date) FROM stdin;
\.


--
-- Name: purchases_purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('purchases_purchase_id_seq', 1, false);


--
-- Data for Name: retailers; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY retailers (retailer_id, retailer_name) FROM stdin;
\.


--
-- Name: retailers_retailer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('retailers_retailer_id_seq', 1, false);


--
-- Name: brands_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (brand_id);


--
-- Name: households_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY households
    ADD CONSTRAINT households_pkey PRIMARY KEY (household_id);


--
-- Name: purchases_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (purchase_id);


--
-- Name: retailers_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY retailers
    ADD CONSTRAINT retailers_pkey PRIMARY KEY (retailer_id);


--
-- Name: purchases_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY purchases
    ADD CONSTRAINT purchases_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES brands(brand_id);


--
-- Name: purchases_household_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY purchases
    ADD CONSTRAINT purchases_household_id_fkey FOREIGN KEY (household_id) REFERENCES households(household_id);


--
-- Name: purchases_retailer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY purchases
    ADD CONSTRAINT purchases_retailer_id_fkey FOREIGN KEY (retailer_id) REFERENCES retailers(retailer_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

