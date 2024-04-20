--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6 (Homebrew)
-- Dumped by pg_dump version 15.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: companion_enemies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companion_enemies (
    plant_id_a bigint,
    plant_id_b bigint
);


ALTER TABLE public.companion_enemies OWNER TO postgres;

--
-- Name: companion_friends; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companion_friends (
    plant_id_a bigint,
    plant_id_b bigint
);


ALTER TABLE public.companion_friends OWNER TO postgres;

--
-- Name: freetext_plants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.freetext_plants (
    plant_id bigint NOT NULL,
    user_id bigint,
    plant_name text,
    duration_to_maturity_months bigint,
    plant_spacing_metres numeric,
    metres_squared_required numeric,
    perennial_or_annual text,
    january text,
    february text,
    march text,
    april text,
    may text,
    june text,
    july text,
    august text,
    september text,
    october text,
    november text,
    december text
);


ALTER TABLE public.freetext_plants OWNER TO postgres;

--
-- Name: freetext_plants_plant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.freetext_plants_plant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.freetext_plants_plant_id_seq OWNER TO postgres;

--
-- Name: freetext_plants_plant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.freetext_plants_plant_id_seq OWNED BY public.freetext_plants.plant_id;


--
-- Name: gardens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gardens (
    garden_id bigint NOT NULL,
    user_id bigint,
    garden_size_metres_squared numeric,
    garden_name text
);


ALTER TABLE public.gardens OWNER TO postgres;

--
-- Name: gardens_garden_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gardens_garden_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gardens_garden_id_seq OWNER TO postgres;

--
-- Name: gardens_garden_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gardens_garden_id_seq OWNED BY public.gardens.garden_id;


--
-- Name: planted_in_gardens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planted_in_gardens (
    plant_id bigint,
    number_of_plants bigint DEFAULT '0'::bigint,
    month_planted text,
    months_to_remain_planted bigint,
    freetext text DEFAULT 'no'::text,
    garden_id bigint
);


ALTER TABLE public.planted_in_gardens OWNER TO postgres;

--
-- Name: plants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plants (
    plant_id bigint NOT NULL,
    plant_name text,
    duration_to_maturity_months bigint,
    plant_spacing_metres numeric,
    metres_squared_required numeric,
    perennial_or_annual text,
    january text,
    february text,
    march text,
    april text,
    may text,
    june text,
    july text,
    august text,
    september text,
    october text,
    november text,
    december text
);


ALTER TABLE public.plants OWNER TO postgres;

--
-- Name: plants_plant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.plants_plant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.plants_plant_id_seq OWNER TO postgres;

--
-- Name: plants_plant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.plants_plant_id_seq OWNED BY public.plants.plant_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id bigint NOT NULL,
    username text,
    hash_password text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: freetext_plants plant_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freetext_plants ALTER COLUMN plant_id SET DEFAULT nextval('public.freetext_plants_plant_id_seq'::regclass);


--
-- Name: gardens garden_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gardens ALTER COLUMN garden_id SET DEFAULT nextval('public.gardens_garden_id_seq'::regclass);


--
-- Name: plants plant_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plants ALTER COLUMN plant_id SET DEFAULT nextval('public.plants_plant_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: companion_enemies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companion_enemies (plant_id_a, plant_id_b) FROM stdin;
1	22
1	32
3	4
3	16
3	22
3	32
4	52
7	22
7	49
9	49
12	22
12	49
11	19
11	13
18	38
22	37
22	49
27	34
32	37
37	16
37	45
38	13
38	39
38	41
38	52
52	41
46	2
8	49
52	21
\.


--
-- Data for Name: companion_friends; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companion_friends (plant_id_a, plant_id_b) FROM stdin;
1	2
1	16
1	34
1	52
2	52
3	7
3	8
3	9
3	11
3	12
3	28
3	34
4	3
4	7
4	8
4	9
4	12
4	28
4	32
4	37
4	38
4	47
7	3
3	7
7	11
7	17
7	28
7	37
9	11
9	17
12	11
12	17
12	28
10	11
10	32
10	52
15	11
15	32
15	52
15	11
11	17
13	16
13	19
13	32
13	47
16	18
16	28
16	37
13	9
18	2
18	3
18	7
18	8
18	9
18	11
18	12
18	19
18	28
18	35
18	37
18	40
19	7
19	9
19	12
20	3
20	47
22	35
22	41
27	11
27	13
27	32
27	35
27	49
28	3
28	4
28	9
28	11
28	18
28	32
28	35
28	37
28	40
28	49
53	40
44	40
32	4
32	7
32	9
32	11
32	27
32	28
32	34
32	35
32	46
32	49
32	52
34	1
34	52
37	3
37	4
37	8
37	9
37	11
37	12
37	13
37	18
37	28
37	35
37	38
37	40
38	3
38	7
38	8
38	9
38	12
38	20
38	35
38	37
38	53
39	3
39	9
39	20
39	37
39	40
39	37
40	3
40	11
40	18
40	28
40	35
40	37
40	47
46	13
46	20
46	49
49	3
49	16
49	27
49	28
49	32
49	47
52	1
52	2
52	13
52	7
52	8
52	9
52	11
52	12
52	13
52	16
52	19
52	32
52	34
52	35
9	22
\.


--
-- Data for Name: freetext_plants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.freetext_plants (plant_id, user_id, plant_name, duration_to_maturity_months, plant_spacing_metres, metres_squared_required, perennial_or_annual, january, february, march, april, may, june, july, august, september, october, november, december) FROM stdin;
1	1	marigold	3	0.3	0.09	annual	yes	yes	no	no	no	no	no	no	yes	yes	yes	yes
2	1	strawflower	3	0.3	0.09	annual	no	no	yes	yes	yes	no	no	no	yes	yes	yes	no
\.


--
-- Data for Name: gardens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gardens (garden_id, user_id, garden_size_metres_squared, garden_name) FROM stdin;
1	1	6	backyard
3	1	4	containers
\.


--
-- Data for Name: planted_in_gardens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planted_in_gardens (plant_id, number_of_plants, month_planted, months_to_remain_planted, freetext, garden_id) FROM stdin;
2	4	march	6	no	1
39	2	september	2	no	1
1	4	january	10	yes	3
2	4	april	4	yes	1
\.


--
-- Data for Name: plants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plants (plant_id, plant_name, duration_to_maturity_months, plant_spacing_metres, metres_squared_required, perennial_or_annual, january, february, march, april, may, june, july, august, september, october, november, december) FROM stdin;
1	asparagus	24	0.3	0.09	perennial	no	no	no	no	no	no	no	yes	yes	yes	yes	yes
2	basil	2	0.2	0.04	annual	no	no	no	no	no	no	no	no	yes	no	no	no
3	beans	2	0.07	0.0049	annual	yes	yes	no	no	no	no	no	no	yes	yes	yes	yes
4	beetroot	2	0.2	0.04	annual	yes	yes	yes	yes	no	no	yes	yes	yes	yes	yes	yes
5	blueberry bush	24	1.5	1.65	perennial	no	no	no	no	no	no	no	no	no	no	no	no
6	broad beans	2	0.15	0.0165	annual	no	no	yes	yes	yes	yes	no	no	no	no	no	no
7	broccoli	2	0.3	0.09	annual	no	yes	yes	no	no	no	no	no	no	no	no	no
8	brussels sprouts	3	0.3	0.09	annual	yes	no	no	no	no	no	no	no	no	no	no	yes
9	cabbage	2	0.3	0.09	annual	no	yes	yes	no	no	no	no	no	no	no	no	no
10	capsicum	2	0.5	0.25	perennial	no	no	no	no	no	no	no	yes	yes	no	no	no
11	carrot	2	0.1	0.01	annual	yes	yes	yes	yes	yes	no	no	no	yes	yes	yes	yes
12	cauliflower	2	0.3	0.09	annual	no	yes	no	no	no	no	no	no	no	no	no	no
13	celery	3	0.15	0.0165	annual	no	no	no	no	no	no	no	no	yes	yes	no	no
14	chickpea	3	0.15	0.0165	annual	no	no	no	no	yes	no	no	no	no	no	no	no
15	chilli	2	0.3	0.09	perennial	no	no	no	no	no	no	no	yes	yes	no	no	no
16	chives	1	0.05	0.0025	perennial	yes	yes	yes	yes	yes	no	no	no	yes	yes	yes	yes
17	coriander	1	0.3	0.09	annual	no	no	no	yes	yes	yes	yes	yes	yes	no	no	no
18	cucumber	2	0.4	0.16	annual	no	no	no	no	no	no	no	no	yes	yes	yes	yes
19	dill	2	0.2	0.04	annual	yes	yes	yes	yes	yes	no	no	no	yes	yes	yes	yes
20	eggplant	2	0.3	0.09	perennial	no	no	no	no	no	no	no	yes	yes	no	no	no
21	fennel	2	0.25	0.0625	annual	no	yes	yes	yes	yes	no	no	no	no	no	no	no
22	garlic	8	0.1	0.01	annual	no	no	no	yes	yes	yes	no	no	no	no	no	no
23	globe artichoke	4	0.9	0.81	perennial	no	no	no	no	no	no	no	yes	yes	yes	yes	no
24	gourd	2	0.4	0.16	annual	no	no	no	no	no	no	no	no	yes	yes	yes	yes
25	jerusalem artichoke	6	0.45	0.2025	annual	no	no	no	no	no	no	no	no	yes	yes	yes	no
26	kale	2	0.15	0.0165	annual	no	no	yes	yes	yes	no	no	no	no	no	no	no
27	leeks	2	0.1	0.01	annual	no	yes	yes	no	no	no	no	yes	yes	no	no	no
28	lettuce	1	0.2	0.04	annual	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes
29	mizuna	1	0.2	0.04	annual	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes
30	mustard greens	1	0.3	0.09	annual	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes
31	okra	2	0.3	0.09	annual	no	no	no	no	no	no	no	no	no	yes	yes	no
32	onion	2	0.1	0.01	annual	no	yes	no	no	yes	yes	yes	yes	no	no	no	no
33	pak choy	1	0.15	0.0165	annual	no	no	yes	yes	yes	no	no	no	no	no	no	no
34	parsley	2	0.2	0.04	annual	yes	yes	yes	yes	yes	no	no	no	yes	yes	yes	yes
35	parsnip	3	0.1	0.01	annual	no	no	no	no	no	no	no	yes	yes	yes	no	no
36	peanut	4	0.3	0.09	annual	no	no	no	no	no	no	no	no	no	yes	yes	no
37	peas	2	0.07	0.0049	annual	no	no	no	yes	yes	yes	yes	no	no	no	no	no
38	potato	2	0.3	0.09	annual	yes	yes	yes	yes	yes	no	no	yes	yes	yes	yes	yes
39	pumpkin	2	0.4	0.16	annual	no	no	no	no	no	no	no	no	yes	yes	yes	yes
40	radish	1	0.05	0.0025	annual	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes	yes
41	raspberry cane	12	0.3	0.09	perennial	no	no	no	no	yes	yes	yes	yes	no	no	no	no
42	rhubarb	12	0.6	0.36	perennial	no	no	no	no	no	no	no	no	yes	yes	no	no
43	rocket	1	0.25	0.0625	annual	no	no	yes	yes	yes	no	no	yes	yes	yes	yes	no
44	rockmelon	2	0.4	0.16	annual	no	no	no	no	no	no	no	no	yes	yes	no	no
45	shallot	2	0.15	0.0165	annual	no	yes	yes	yes	yes	yes	yes	yes	yes	no	no	no
46	silverbeet	2	0.2	0.04	annual	yes	yes	yes	yes	yes	no	no	no	yes	yes	yes	yes
47	spinach	1	0.2	0.04	annual	no	no	yes	yes	yes	no	no	no	no	no	no	no
48	spring onion	1	0.02	0.00040	annual	no	no	no	no	no	no	no	yes	yes	yes	no	no
49	strawberry runner	4	0.3	0.09	perennial	no	no	no	no	no	yes	yes	yes	yes	yes	no	no
50	sweet potato	3	0.3	0.09	annual	no	no	no	no	no	no	no	no	no	yes	yes	no
51	sweetcorn	2	0.2	0.04	annual	yes	yes	no	no	no	no	no	no	yes	yes	yes	yes
52	tomato	2	0.15	0.0165	annual	no	no	no	no	no	no	no	yes	yes	no	no	no
53	watermelon	2	0.4	0.16	annual	no	no	no	no	no	no	no	no	yes	yes	no	no
54	zucchini	2	0.4	0.16	annual	no	no	no	no	no	no	no	no	yes	yes	no	no
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, hash_password) FROM stdin;
1	admin	scrypt:32768:8:1$xeEcTCSTzANisVC1$ad40808fb56fda63e7083a35f387be13ae0d107f49ee7a3e49a8598d3abbdbb819c87c1ad4062e2acae204ad9e536614de44e889b7879c412b0e75b7ac413242
\.


--
-- Name: freetext_plants_plant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.freetext_plants_plant_id_seq', 2, true);


--
-- Name: gardens_garden_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gardens_garden_id_seq', 3, true);


--
-- Name: plants_plant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plants_plant_id_seq', 54, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: users idx_16392_sqlite_autoindex_users_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT idx_16392_sqlite_autoindex_users_1 PRIMARY KEY (user_id);


--
-- Name: gardens idx_16399_sqlite_autoindex_gardens_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gardens
    ADD CONSTRAINT idx_16399_sqlite_autoindex_gardens_1 PRIMARY KEY (garden_id);


--
-- Name: plants idx_16412_sqlite_autoindex_plants_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT idx_16412_sqlite_autoindex_plants_1 PRIMARY KEY (plant_id);


--
-- Name: freetext_plants idx_16419_sqlite_autoindex_freetext_plants_1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freetext_plants
    ADD CONSTRAINT idx_16419_sqlite_autoindex_freetext_plants_1 PRIMARY KEY (plant_id);


--
-- Name: idx_16412_sqlite_autoindex_plants_2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_16412_sqlite_autoindex_plants_2 ON public.plants USING btree (plant_name);


--
-- Name: companion_enemies companion_enemies_plant_id_a_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companion_enemies
    ADD CONSTRAINT companion_enemies_plant_id_a_fkey FOREIGN KEY (plant_id_a) REFERENCES public.plants(plant_id);


--
-- Name: companion_enemies companion_enemies_plant_id_b_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companion_enemies
    ADD CONSTRAINT companion_enemies_plant_id_b_fkey FOREIGN KEY (plant_id_b) REFERENCES public.plants(plant_id);


--
-- Name: companion_friends companion_friends_plant_id_a_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companion_friends
    ADD CONSTRAINT companion_friends_plant_id_a_fkey FOREIGN KEY (plant_id_a) REFERENCES public.plants(plant_id);


--
-- Name: companion_friends companion_friends_plant_id_b_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companion_friends
    ADD CONSTRAINT companion_friends_plant_id_b_fkey FOREIGN KEY (plant_id_b) REFERENCES public.plants(plant_id);


--
-- Name: freetext_plants freetext_plants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.freetext_plants
    ADD CONSTRAINT freetext_plants_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: gardens gardens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gardens
    ADD CONSTRAINT gardens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: planted_in_gardens planted_in_gardens_garden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planted_in_gardens
    ADD CONSTRAINT planted_in_gardens_garden_id_fkey FOREIGN KEY (garden_id) REFERENCES public.gardens(garden_id);


--
-- PostgreSQL database dump complete
--

