--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

-- Started on 2016-10-04 20:17:32

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12355)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

DROP TYPE IF EXISTS revision_type;
DROP TYPE IF EXISTS files_kross_type;
DROP TYPE IF EXISTS user_type;
DROP TYPE IF EXISTS permission_type;


CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2231 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 583 (class 1247 OID 25160)
-- Name: files_kross_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE files_kross_type AS ENUM (
    'A',
    'M'
);


ALTER TYPE files_kross_type OWNER TO postgres;

--
-- TOC entry 559 (class 1247 OID 25076)
-- Name: permission_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE permission_type AS ENUM (
    'pbl',
    'grp',
    'sol'
);


ALTER TYPE permission_type OWNER TO postgres;

--
-- TOC entry 589 (class 1247 OID 25186)
-- Name: revision_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE revision_type AS ENUM (
    'A',
    'N'
);


ALTER TYPE revision_type OWNER TO postgres;

--
-- TOC entry 567 (class 1247 OID 25100)
-- Name: user_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE user_type AS ENUM (
    'admin',
    'volunteer'
);


ALTER TYPE user_type OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 185 (class 1259 OID 25127)
-- Name: annotations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE annotations (
    article_id integer NOT NULL,
    annotation_text text NOT NULL,
    annotation_sha_hash character varying(66) NOT NULL
);


ALTER TABLE annotations OWNER TO postgres;

--
-- TOC entry 182 (class 1259 OID 25085)
-- Name: articles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE articles (
    article_id integer NOT NULL,
    article_title text NOT NULL,
    article_annotation text,
    article_html text NOT NULL,
    category_article_id integer NOT NULL,
    template integer,
    permissions permission_type DEFAULT 'pbl'::permission_type NOT NULL
);


ALTER TABLE articles OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 25083)
-- Name: articles_article_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE articles_article_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE articles_article_id_seq OWNER TO postgres;

--
-- TOC entry 2232 (class 0 OID 0)
-- Dependencies: 181
-- Name: articles_article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE articles_article_id_seq OWNED BY articles.article_id;


--
-- TOC entry 187 (class 1259 OID 25143)
-- Name: files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE files (
    file_id integer NOT NULL,
    user_id integer NOT NULL,
    file_create_date timestamp without time zone DEFAULT now() NOT NULL,
    file_inside_name character varying(66) NOT NULL,
    file_extension character varying(20) NOT NULL,
    file_name character varying(254) NOT NULL
);


ALTER TABLE files OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 25141)
-- Name: files_file_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE files_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE files_file_id_seq OWNER TO postgres;

--
-- TOC entry 2233 (class 0 OID 0)
-- Dependencies: 186
-- Name: files_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE files_file_id_seq OWNED BY files.file_id;


--
-- TOC entry 188 (class 1259 OID 25165)
-- Name: files_kroses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE files_kroses (
    file_id integer NOT NULL,
    article_id integer NOT NULL,
    file_kros_create_date timestamp without time zone DEFAULT now() NOT NULL,
    file_kros_flag files_kross_type NOT NULL
);


ALTER TABLE files_kroses OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 25193)
-- Name: revisions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE revisions (
    revision_id integer NOT NULL,
    article_id integer NOT NULL,
    user_id integer NOT NULL,
    revision_date timestamp without time zone DEFAULT now() NOT NULL,
    revision_actual_flag revision_type NOT NULL,
    title_sha_hash character varying(66) NOT NULL,
    annotation_sha_hash character varying(66) NOT NULL,
    text_sha_hash character varying(66) NOT NULL
);


ALTER TABLE revisions OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 25191)
-- Name: revisions_revision_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE revisions_revision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE revisions_revision_id_seq OWNER TO postgres;

--
-- TOC entry 2234 (class 0 OID 0)
-- Dependencies: 189
-- Name: revisions_revision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE revisions_revision_id_seq OWNED BY revisions.revision_id;


--
-- TOC entry 191 (class 1259 OID 25217)
-- Name: texts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE texts (
    article_id integer NOT NULL,
    text_sha_hash character varying(66) NOT NULL,
    text_html text NOT NULL
);


ALTER TABLE texts OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 25232)
-- Name: titles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE titles (
    article_id integer NOT NULL,
    title_text text NOT NULL,
    title_sha_hash character varying(66) NOT NULL
);


ALTER TABLE titles OWNER TO postgres;

--
-- TOC entry 184 (class 1259 OID 25107)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    user_id integer NOT NULL,
    user_create timestamp without time zone DEFAULT now() NOT NULL,
    user_login character varying(50) NOT NULL,
    user_name character varying(254) DEFAULT NULL::character varying,
    user_external character varying(50) DEFAULT NULL::character varying,
    user_pass character varying(70) DEFAULT NULL::character varying,
    user_phon character varying(50) DEFAULT NULL::character varying,
    user_email character varying(254) DEFAULT NULL::character varying,
    user_role user_type DEFAULT 'volunteer'::user_type NOT NULL
);


ALTER TABLE users OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 25105)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO postgres;

--
-- TOC entry 2235 (class 0 OID 0)
-- Dependencies: 183
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- TOC entry 2032 (class 2604 OID 25088)
-- Name: article_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles ALTER COLUMN article_id SET DEFAULT nextval('articles_article_id_seq'::regclass);


--
-- TOC entry 2042 (class 2604 OID 25146)
-- Name: file_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY files ALTER COLUMN file_id SET DEFAULT nextval('files_file_id_seq'::regclass);


--
-- TOC entry 2045 (class 2604 OID 25196)
-- Name: revision_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY revisions ALTER COLUMN revision_id SET DEFAULT nextval('revisions_revision_id_seq'::regclass);


--
-- TOC entry 2034 (class 2604 OID 25110)
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- TOC entry 2216 (class 0 OID 25127)
-- Dependencies: 185
-- Data for Name: annotations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  annotations (article_id, annotation_text, annotation_sha_hash) VALUES 
(2,	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'3312f2f071e0c4c50c9165159db773750761d6a9bbf73bacd2270d6d868d1dd0'),
(4,	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'5bef2d09b4f5f2110373870af4c9c7e0ddc135fe029087508538fc950d5b97da'),
(1,	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'8402d4bffd9334332c82c79ac1c226eba896aec279027172a4e1c0c29231766f'),
(3,	'0KjQsNCx0LvQvtC90Ys=',	'8c0f4c6dfae1b203f4f6f4ce4476c2dbf2077d91a6ab12ad290bb66328e8081c'),
(6,	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==',	'c9761801d393a57c1bf154f9ad58d01c5c6abf9b06272bfc6a7cf70d3e4532b7'),
(5,	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'cd0a31e15ed0f494158e78d79a554ee926a2583e56868a9cf3b7d53cbc207bff');



--
-- TOC entry 2213 (class 0 OID 25085)
-- Dependencies: 182
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  articles (article_id, article_title, article_annotation, article_html, category_article_id, template, permissions) VALUES 
(1,	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'PHA+0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk8L3A+',	0,	'0',	'pbl'),
(2,	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'PHA+0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuDwvcD4=',	1,	'0',	'pbl'),
(3,	'0KjQsNCx0LvQvtC90Ys=',	'0KjQsNCx0LvQvtC90Ys=',	'PHA+0KjQsNCx0LvQvtC90Ys8L3A+',	1,	'0',	'pbl'),
(4,	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'PHA+0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y88L3A+',	1,	'0',	'pbl'),
(5,	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'PHA+0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA8L3A+',	4,	'6',	'pbl'),
(6,	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgdGC0YDQsNC90LjRhtGL',	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==',	'PCFET0NUWVBFIGh0bWw+DQo8aHRtbD4NCjxoZWFkPg0KPG1ldGEgY2hhcnNldD0iVVRGLTgiPg0KPHRpdGxlPlRvcm5hZG8gV2lraSBBZG1pbiBsYXllcjwvdGl0bGU+DQo8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Ii9zdGF0aWMvd2lraS5jc3MiIHR5cGU9InRleHQvY3NzIj4NCjxsaW5rIHJlbD0iYWx0ZXJuYXRlIiBocmVmPSIvZmVlZCIgdHlwZT0iYXBwbGljYXRpb24vYXRvbSt4bWwiIA0KdGl0bGU9Int7YXJ0aWNsZS5hcnRpY2xlX3RpdGxlfX0iPg0KDQo8L2hlYWQ+DQo8Ym9keT4NCjxkaXYgaWQ9ImJvZHkiPg0KPGRpdiBpZD0iaGVhZGVyIj4NCjxkaXYgc3R5bGU9ImZsb2F0OnJpZ2h0Ij4NCg0KPGEgaHJlZj0iL2F1dGgvbG9naW4iPlNpZ24gaW48L2E+IHRvIGNvbXBvc2UvZWRpdA0KDQo8L2Rpdj4NCjxoMT48YSBocmVmPSIvIj7QndCwINCT0LvQsNCy0L3Rg9GOPC9hPjwvaDE+DQo8L2Rpdj4NCjwhLS0gdXNlciBJUzogTm9uZSAtLT4NCjxkaXYgaWQ9ImNvbnRlbnQiPg0KDQo8IS0tIG1vZHVsZXMgMTM3ICBhcnRpY2xlLmh0bWwgLS0+DQo8ZGl2IGNsYXNzPSJhcnRpY2xlIj4NCjxoMT48YSBocmVmPSJ7e2FydGljbGUuYXJ0aWNsZV9pZH19Ij57e2FydGljbGUuYXJ0aWNsZV90aXRsZX19PC9hPjwvaDE+DQo8ZGl2IGNsYXNzPSJib2R5Ij57e2FydGljbGUuYXJ0aWNsZV9hbm5vdGF0aW9ufX08L2Rpdj4NCjxkaXYgY2xhc3M9ImJvZHkiPg0KeyUgcmF3IGFydGljbGUuYXJ0aWNsZV9odG1sICV9DQo8YnI+DQo8IS0tIG1vZHVsZXMvZmlsZXNfbGlzdC5odG1sIC0tPg0Ke3tmaWxlTGlzdH19DQo8IS0tIC8gbW9kdWxlcy9maWxlc19saXN0Lmh0bWwgLS0+DQo8L2Rpdj4NCjxkaXYgY2xhc3M9ImFkbWluIj4NCls8YSBocmVmPSJ7e2FydGljbGUuYXJ0aWNsZV9pZH19Ij5FZGl0IHRoaXMgd2lraTwvYT5dDQpbPGEgaHJlZj0ie3thcnRpY2xlLmFydGljbGVfaWR9fSI+VmlldyBhbGwgcmV2aXNpb25zPC9hPl0NCjwvZGl2Pg0KPC9kaXY+DQoNCjwvZGl2Pg0KPC9kaXY+DQoNCjwvYm9keT4NCjwvaHRtbD4=',	3,	0,	'pbl');



--
-- TOC entry 2236 (class 0 OID 0)
-- Dependencies: 181
-- Name: articles_article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('articles_article_id_seq', 7, true);



--
-- TOC entry 2237 (class 0 OID 0)
-- Dependencies: 186
-- Name: files_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('files_file_id_seq', 1, false);




--
-- TOC entry 2221 (class 0 OID 25193)
-- Dependencies: 190
-- Data for Name: revisions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  revisions (revision_id, article_id, user_id, revision_date, revision_actual_flag, title_sha_hash, annotation_sha_hash, text_sha_hash) VALUES 
(1,	1,	1,	'2016-08-11 09:33:43',	'A',	'136e050397813d0297c61a5ab8ecb24928896a4b282f0a4be52de7bf19e2907d',	'8402d4bffd9334332c82c79ac1c226eba896aec279027172a4e1c0c29231766f',	'c41af4fe916911c79460ec66c912a82868bdaadca6fbeb5329953f8e3b074b15'),
(2,	2,	1,	'2016-08-11 09:34:11',	'A',	'9a28c9f82da29ef3ecc8052d88363a3b3bc0ae6e4c250743b17a27a4398c8a1a',	'3312f2f071e0c4c50c9165159db773750761d6a9bbf73bacd2270d6d868d1dd0',	'ff0917f405ec86faeff00de5eed8e26b9fea3680a2cbf5ae99aafa49bd324fb8'),
(3,	3,	1,	'2016-08-11 09:34:31',	'A',	'99d49ee10b9e1309e286af411756e97d90d11dc9763be58299fa89ae8c3fb6f2',	'8c0f4c6dfae1b203f4f6f4ce4476c2dbf2077d91a6ab12ad290bb66328e8081c',	'ee5c6e6d845e957e61f43fcc4919ad78452cd2fa770d61897042aa2e1c69766c'),
(4,	4,	1,	'2016-08-11 09:34:53',	'A',	'0e27a9d729935babb7f9489e627ea7fb83599136684370b3ff327269ff2d1b5f',	'5bef2d09b4f5f2110373870af4c9c7e0ddc135fe029087508538fc950d5b97da',	'a2bdf727661b4064802c9c1a4858d7fb07b6db7ef196e77c7367ac054ff99035'),
(5,	5,	1,	'2016-08-11 09:36:25',	'A',	'49f68ae49b1599586d02a26ffd33f3d9bd26bbf8f2b624efef7abd21151c7ded',	'cd0a31e15ed0f494158e78d79a554ee926a2583e56868a9cf3b7d53cbc207bff',	'9ab19d7ebab9c72a557be2fb02631f8eac77729515b23b9c47f9daa43a71cc50'),
(6,	6,	1,	'2016-10-04 19:30:37.173685',	'A',	'52c322298e8a7f517e34353ae10b5918b64019b6a53bfb3aa9532c3ccd22021d',	'c9761801d393a57c1bf154f9ad58d01c5c6abf9b06272bfc6a7cf70d3e4532b7',	'6494631c8b83ebc6d72a5add30f5a6899bd2fa2ff4de32ad85eb6536c93e217e');



--
-- TOC entry 2238 (class 0 OID 0)
-- Dependencies: 189
-- Name: revisions_revision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('revisions_revision_id_seq', 7, true);


--
-- TOC entry 2222 (class 0 OID 25217)
-- Dependencies: 191
-- Data for Name: texts; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  texts (article_id, text_sha_hash, text_html) VALUES 
(5,	'9ab19d7ebab9c72a557be2fb02631f8eac77729515b23b9c47f9daa43a71cc50',	'eJyzKbC7MPnC7gsbLmy6sPfChov9ChcbLzYBGU0Xe8AcoMxOkICNfoEdAJZhHAQ='),
(4,	'a2bdf727661b4064802c9c1a4858d7fb07b6db7ef196e77c7367ac054ff99035',	'eJyzKbC7MOPC3ostF/ZdbLiw58KGi20XdlzYd2EvEG642K9wsfFiE5DRdLHnYr+NfoEdAA8eHvU='),
(1,	'c41af4fe916911c79460ec66c912a82868bdaadca6fbeb5329953f8e3b074b15',	'eJyzKbC7sPDC/gs7LjZe2Hdhl8KFWRc2XGy6sPXC5gv7LjZc2HFhp8LFRqAARHCnjX6BHQBpwyDx'),
(3,	'ee5c6e6d845e957e61f43fcc4919ad78452cd2fa770d61897042aa2e1c69766c',	'eJyzKbC7sOLChgsbL+y+sO/C3ovdNvoFdgCOSgx/'),
(2,	'ff0917f405ec86faeff00de5eed8e26b9fea3680a2cbf5ae99aafa49bd324fb8',	'eJwBJgDZ/zxwPtCh0LvRg9C20LXQsdC90YvQtSDRgdGC0LDRgtGM0Lg8L3A+3r0Xyw=='),
(6,	'6494631c8b83ebc6d72a5add30f5a6899bd2fa2ff4de32ad85eb6536c93e217e',	'eJyNU81q3DAQvi/sO0wEORVHLD20hLWhtCkUSlvItqWUElRrdi0iS4s0m2QxPvWeS899h5Br6Ds4b1TJa2+dbPpz0aDRfDPffKOZ7r14+3z26d0RFFTqbDyabi0KGW2JJCAvhPNIKXs/e5k8ZdFPijRmM+uMkBY+qlMFz2SpDGixRjflm/cQqJU5BYc6ZZ7WGn2BSAwKh/OUcU+CVM7PA/wg954BrZeYMsIL4vF+N4HQhKEe4RY/R5Q9SCyXWuUhnzVckC0fXZSawXjUMklZVQkXamk86OxJ+1DXsUgow/uOv1q5jlaqM1AyZfHOho4YiG7rattK2VxbQYdOLQrqMoqepVhRwbVdKMOyY7UwoMyUiwzIQm7LpfXIUSra0AgpW/0n2e8ELGt+NFfQfG9umqvmuvl5++32MqYIrCfZALWXJLDy6ODV8SG8sQYhSYbUc2sITU8wRpdWrsJUYPL4CUCvUPwEA2SuhfdB4M0ru09vV1klo6x/VHzIfJB/I/QuShhjqZ1rhHad7uDGo2ofnDiH+/C2mf06TtZld7vmcxXOE608DXququh+HZx13cXzvyMeYiXiNkRan/8p1FEYPlChPMRFiOp8+R/YB4WhW63DcpwpH+TxHXRLp7MPe/p/ztuV/wUBvlKN');



--
-- TOC entry 2223 (class 0 OID 25232)
-- Dependencies: 192
-- Data for Name: titles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  titles (article_id, title_text, title_sha_hash) VALUES 
(4,	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'0e27a9d729935babb7f9489e627ea7fb83599136684370b3ff327269ff2d1b5f'),
(1,	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'136e050397813d0297c61a5ab8ecb24928896a4b282f0a4be52de7bf19e2907d'),
(5,	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'49f68ae49b1599586d02a26ffd33f3d9bd26bbf8f2b624efef7abd21151c7ded'),
(3,	'0KjQsNCx0LvQvtC90Ys=',	'99d49ee10b9e1309e286af411756e97d90d11dc9763be58299fa89ae8c3fb6f2'),
(2,	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'9a28c9f82da29ef3ecc8052d88363a3b3bc0ae6e4c250743b17a27a4398c8a1a'),
(6,	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgdGC0YDQsNC90LjRhtGL',	'52c322298e8a7f517e34353ae10b5918b64019b6a53bfb3aa9532c3ccd22021d');



--
-- TOC entry 2215 (class 0 OID 25107)
-- Dependencies: 184
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  users (user_id, user_create, user_login, user_name, user_external, user_pass, user_phon, user_email, user_role) VALUES 
(1,	'2015-12-25 12:53:08',	'login',	'MyName And SurName ewrwerwerw',	'',	'$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.',	'1234-65432-4444',	'mail_0001@mail.com',	'admin');



--
-- TOC entry 2239 (class 0 OID 0)
-- Dependencies: 183
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_user_id_seq', 2, false);


--
-- TOC entry 2061 (class 2606 OID 25134)
-- Name: annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT annotations_pkey PRIMARY KEY (annotation_sha_hash);


--
-- TOC entry 2049 (class 2606 OID 25094)
-- Name: articles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY articles
    ADD CONSTRAINT articles_pkey PRIMARY KEY (article_id);


--
-- TOC entry 2073 (class 2606 OID 25170)
-- Name: files_kroses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY files_kroses
    ADD CONSTRAINT files_kroses_pkey PRIMARY KEY (file_id, article_id);


--
-- TOC entry 2066 (class 2606 OID 25149)
-- Name: files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_pkey PRIMARY KEY (file_id);


--
-- TOC entry 2077 (class 2606 OID 25199)
-- Name: revisions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY revisions
    ADD CONSTRAINT revisions_pkey PRIMARY KEY (revision_id);


--
-- TOC entry 2085 (class 2606 OID 25224)
-- Name: texts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY texts
    ADD CONSTRAINT texts_pkey PRIMARY KEY (text_sha_hash);


--
-- TOC entry 2089 (class 2606 OID 25239)
-- Name: titles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY titles
    ADD CONSTRAINT titles_pkey PRIMARY KEY (title_sha_hash);


--
-- TOC entry 2054 (class 2606 OID 25122)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 2059 (class 1259 OID 25140)
-- Name: annotation_article_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX annotation_article_id ON annotations USING btree (article_id);


--
-- TOC entry 2047 (class 1259 OID 25095)
-- Name: articles_article_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX articles_article_id_idx ON articles USING btree (article_id);


--
-- TOC entry 2050 (class 1259 OID 25096)
-- Name: category_article_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX category_article_id ON articles USING btree (category_article_id);


--
-- TOC entry 2062 (class 1259 OID 25155)
-- Name: file_create_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX file_create_date ON files USING btree (file_create_date);


--
-- TOC entry 2063 (class 1259 OID 25156)
-- Name: file_extension; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX file_extension ON files USING btree (file_extension);


--
-- TOC entry 2068 (class 1259 OID 25183)
-- Name: file_kros_create_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX file_kros_create_date ON files_kroses USING btree (file_kros_create_date);


--
-- TOC entry 2069 (class 1259 OID 25184)
-- Name: file_kros_flag; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX file_kros_flag ON files_kroses USING btree (file_kros_flag);


--
-- TOC entry 2064 (class 1259 OID 25157)
-- Name: file_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX file_name ON files USING btree (file_name);


--
-- TOC entry 2070 (class 1259 OID 25182)
-- Name: files_kroses_article_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX files_kroses_article_id ON files_kroses USING btree (article_id);


--
-- TOC entry 2071 (class 1259 OID 25181)
-- Name: files_kroses_file_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX files_kroses_file_id ON files_kroses USING btree (file_id);


--
-- TOC entry 2067 (class 1259 OID 25158)
-- Name: files_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX files_user_id ON files USING btree (user_id);


--
-- TOC entry 2051 (class 1259 OID 25098)
-- Name: permissions; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX permissions ON articles USING btree (permissions);


--
-- TOC entry 2075 (class 1259 OID 25213)
-- Name: revisions_annotation_sha_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_annotation_sha_hash ON revisions USING btree (annotation_sha_hash);


--
-- TOC entry 2074 (class 1259 OID 25210)
-- Name: revisions_article_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_article_id ON files_kroses USING btree (article_id);


--
-- TOC entry 2078 (class 1259 OID 25215)
-- Name: revisions_revision_actual_flag; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_revision_actual_flag ON revisions USING btree (revision_actual_flag);


--
-- TOC entry 2079 (class 1259 OID 25211)
-- Name: revisions_revision_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_revision_date ON revisions USING btree (revision_date);


--
-- TOC entry 2080 (class 1259 OID 25214)
-- Name: revisions_text_sha_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_text_sha_hash ON revisions USING btree (text_sha_hash);


--
-- TOC entry 2081 (class 1259 OID 25212)
-- Name: revisions_title_sha_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_title_sha_hash ON revisions USING btree (title_sha_hash);


--
-- TOC entry 2082 (class 1259 OID 25216)
-- Name: revisions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX revisions_user_id ON revisions USING btree (user_id);


--
-- TOC entry 2052 (class 1259 OID 25097)
-- Name: template; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX template ON articles USING btree (template);


--
-- TOC entry 2083 (class 1259 OID 25230)
-- Name: texts_article_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX texts_article_id ON texts USING btree (article_id);


--
-- TOC entry 2086 (class 1259 OID 25231)
-- Name: texts_text_sha_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX texts_text_sha_hash ON texts USING btree (text_sha_hash);


--
-- TOC entry 2087 (class 1259 OID 25245)
-- Name: titles_article_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX titles_article_id ON titles USING btree (article_id);


--
-- TOC entry 2055 (class 1259 OID 25126)
-- Name: users_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_email ON users USING btree (user_email);


--
-- TOC entry 2056 (class 1259 OID 25123)
-- Name: users_user_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_name ON users USING btree (user_name);


--
-- TOC entry 2057 (class 1259 OID 25124)
-- Name: users_user_pass; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_pass ON users USING btree (user_pass);


--
-- TOC entry 2058 (class 1259 OID 25125)
-- Name: users_user_phon; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_phon ON users USING btree (user_phon);


--
-- TOC entry 2090 (class 2606 OID 25135)
-- Name: annotations_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY annotations
    ADD CONSTRAINT annotations_article_id_fkey FOREIGN KEY (article_id) REFERENCES articles(article_id);


--
-- TOC entry 2093 (class 2606 OID 25176)
-- Name: files_kroses_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY files_kroses
    ADD CONSTRAINT files_kroses_article_id_fkey FOREIGN KEY (article_id) REFERENCES articles(article_id);


--
-- TOC entry 2092 (class 2606 OID 25171)
-- Name: files_kroses_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY files_kroses
    ADD CONSTRAINT files_kroses_file_id_fkey FOREIGN KEY (file_id) REFERENCES files(file_id);


--
-- TOC entry 2091 (class 2606 OID 25150)
-- Name: files_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY files
    ADD CONSTRAINT files_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- TOC entry 2094 (class 2606 OID 25200)
-- Name: revisions_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY revisions
    ADD CONSTRAINT revisions_article_id_fkey FOREIGN KEY (article_id) REFERENCES articles(article_id);


--
-- TOC entry 2095 (class 2606 OID 25205)
-- Name: revisions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY revisions
    ADD CONSTRAINT revisions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- TOC entry 2096 (class 2606 OID 25225)
-- Name: texts_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY texts
    ADD CONSTRAINT texts_article_id_fkey FOREIGN KEY (article_id) REFERENCES articles(article_id);


--
-- TOC entry 2097 (class 2606 OID 25240)
-- Name: titles_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY titles
    ADD CONSTRAINT titles_article_id_fkey FOREIGN KEY (article_id) REFERENCES articles(article_id);


--
-- TOC entry 2230 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2016-10-04 20:17:33

--
-- PostgreSQL database dump complete
--

