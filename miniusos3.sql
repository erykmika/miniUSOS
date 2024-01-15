--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: kierunki_studiow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kierunki_studiow (
    id integer NOT NULL,
    nazwa character varying(50) NOT NULL,
    stopien integer NOT NULL
);


ALTER TABLE public.kierunki_studiow OWNER TO postgres;

--
-- Name: kierunki_studiow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kierunki_studiow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kierunki_studiow_id_seq OWNER TO postgres;

--
-- Name: kierunki_studiow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kierunki_studiow_id_seq OWNED BY public.kierunki_studiow.id;


--
-- Name: komunikaty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.komunikaty (
    id integer NOT NULL,
    tytul character varying(255) NOT NULL,
    data timestamp without time zone NOT NULL,
    tresc character varying(1500) NOT NULL
);


ALTER TABLE public.komunikaty OWNER TO postgres;

--
-- Name: komunikaty_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.komunikaty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.komunikaty_id_seq OWNER TO postgres;

--
-- Name: komunikaty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.komunikaty_id_seq OWNED BY public.komunikaty.id;


--
-- Name: komunikaty_kierunki_studiow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.komunikaty_kierunki_studiow (
    id_kierunku integer NOT NULL,
    id_komunikatu integer NOT NULL
);


ALTER TABLE public.komunikaty_kierunki_studiow OWNER TO postgres;

--
-- Name: kursy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kursy (
    id character varying(10) NOT NULL,
    nazwa character varying(50) NOT NULL,
    budynek_sala character varying(30) NOT NULL,
    dzien_tygodnia smallint NOT NULL,
    godzina_rozpoczecia time without time zone NOT NULL,
    godzina_zakonczenia time without time zone NOT NULL,
    id_prowadzacego integer NOT NULL,
    id_kierunku integer NOT NULL
);


ALTER TABLE public.kursy OWNER TO postgres;

--
-- Name: oceny; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oceny (
    id integer NOT NULL,
    ocena character varying(3) NOT NULL,
    data_wpisania timestamp without time zone NOT NULL,
    nr_albumu integer NOT NULL,
    id_kursu character varying(10) NOT NULL
);


ALTER TABLE public.oceny OWNER TO postgres;

--
-- Name: oceny_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.oceny_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.oceny_id_seq OWNER TO postgres;

--
-- Name: oceny_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.oceny_id_seq OWNED BY public.oceny.id;


--
-- Name: prowadzacy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prowadzacy (
    id integer NOT NULL,
    imie character varying(30) NOT NULL,
    nazwisko character varying(30) NOT NULL,
    haslo character varying(32) NOT NULL,
    email character varying(254)
);


ALTER TABLE public.prowadzacy OWNER TO postgres;

--
-- Name: prowadzacy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.prowadzacy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.prowadzacy_id_seq OWNER TO postgres;

--
-- Name: prowadzacy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.prowadzacy_id_seq OWNED BY public.prowadzacy.id;


--
-- Name: studenci; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.studenci (
    nr_albumu integer NOT NULL,
    imie character varying(30) NOT NULL,
    nazwisko character varying(30) NOT NULL,
    semestr smallint NOT NULL,
    adres character varying(50) NOT NULL,
    haslo character varying(32) NOT NULL,
    email character varying(254) NOT NULL,
    id_kierunku integer NOT NULL
);


ALTER TABLE public.studenci OWNER TO postgres;

--
-- Name: studenci_kursy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.studenci_kursy (
    nr_albumu integer NOT NULL,
    id_kursu character varying(10) NOT NULL
);


ALTER TABLE public.studenci_kursy OWNER TO postgres;

--
-- Name: kierunki_studiow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kierunki_studiow ALTER COLUMN id SET DEFAULT nextval('public.kierunki_studiow_id_seq'::regclass);


--
-- Name: komunikaty id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.komunikaty ALTER COLUMN id SET DEFAULT nextval('public.komunikaty_id_seq'::regclass);


--
-- Name: oceny id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oceny ALTER COLUMN id SET DEFAULT nextval('public.oceny_id_seq'::regclass);


--
-- Name: prowadzacy id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prowadzacy ALTER COLUMN id SET DEFAULT nextval('public.prowadzacy_id_seq'::regclass);


--
-- Data for Name: kierunki_studiow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kierunki_studiow (id, nazwa, stopien) FROM stdin;
1	Informatyka	1
2	Chemia	1
3	Informatyka	1
4	Matematyka	1
5	Fizyka	1
6	Historia	1
7	Anglistyka	1
8	Psychologia	1
9	Socjologia	1
10	Ekonomia	1
11	Geografia	1
\.


--
-- Data for Name: komunikaty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.komunikaty (id, tytul, data, tresc) FROM stdin;
3	Nowy komunikat	2023-12-25 16:00:00	Treść nowego komunikatu
4	Ważne ogłoszenie	2023-12-25 16:30:00	Treść ważnego ogłoszenia
5	Informacja dla studentów	2023-12-25 17:00:00	Treść informacji dla studentów
6	Zmiana w planie zajęć	2023-12-25 17:30:00	Treść zmiany w planie zajęć
7	Zaproszenie na wykład	2023-12-25 18:00:00	Treść zaproszenia na wykład
8	Ostatnie ostrzeżenie	2023-12-25 18:30:00	Treść ostatniego ostrzeżenia
9	Przypomnienie o egzaminie	2023-12-25 19:00:00	Treść przypomnienia o egzaminie
10	Zmiana w harmonogramie	2023-12-25 19:30:00	Treść zmiany w harmonogramie
11	Nowy kurs dostępny	2023-12-25 20:00:00	Treść informacji o nowym kursie
12	Podsumowanie semestru	2023-12-25 20:30:00	Treść podsumowania semestru
\.


--
-- Data for Name: komunikaty_kierunki_studiow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.komunikaty_kierunki_studiow (id_kierunku, id_komunikatu) FROM stdin;
2	3
3	4
4	5
5	6
6	7
7	8
8	9
9	10
10	11
11	12
1	3
1	4
1	5
1	6
\.


--
-- Data for Name: kursy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kursy (id, nazwa, budynek_sala, dzien_tygodnia, godzina_rozpoczecia, godzina_zakonczenia, id_prowadzacego, id_kierunku) FROM stdin;
KURS1	Biologia Molekularna	A-101	1	08:00:00	10:00:00	1	1
KURS2	Podstawy Chemii	B-201	2	10:30:00	12:30:00	2	2
KURS3	Algorytmy i Struktury Danych	C-301	3	13:00:00	15:00:00	3	3
KURS4	Analiza Matematyczna	D-401	4	15:30:00	17:30:00	4	4
KURS5	Mechanika Kwantowa	E-501	5	18:00:00	20:00:00	5	5
KURS6	Literatura Angielska	F-601	1	08:30:00	10:30:00	6	6
KURS7	Psychologia Społeczna	G-701	2	11:00:00	13:00:00	7	7
KURS8	Socjologia Współczesna	H-801	3	13:30:00	15:30:00	8	8
KURS9	Mikroekonomia	I-901	4	16:00:00	18:00:00	9	9
KURS10	Geografia Świata	J-1001	5	18:30:00	20:30:00	10	10
KURS11	Administracja danymi osobowymi	A-101	1	10:30:00	12:00:00	1	1
KURS12	Administrowanie bazami danych	A-102	2	10:30:00	12:00:00	1	1
KURS13	Akademia cisco	A-103	3	16:00:00	18:00:00	1	1
KURS14	Algorytmy i struktura danych	A-204	4	16:00:00	18:00:00	1	1
KURS15	Analiza danych	A-305	5	10:30:00	12:00:00	1	1
\.


--
-- Data for Name: oceny; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oceny (id, ocena, data_wpisania, nr_albumu, id_kursu) FROM stdin;
5	3.5	2023-12-25 17:30:00	123127	KURS4
6	5.0	2023-12-25 18:00:00	123128	KURS5
7	4.5	2023-12-25 18:30:00	123129	KURS6
8	4.0	2023-12-25 19:00:00	123130	KURS7
9	3.0	2023-12-25 19:30:00	123131	KURS8
10	4.0	2023-12-25 20:00:00	123132	KURS9
11	5.0	2023-12-25 20:30:00	123133	KURS10
3	5.5	2023-12-25 16:38:25.188187	123125	KURS2
14	4.5	2024-01-14 15:07:04.086622	123124	KURS1
30	4.5	2023-12-27 20:00:00	123124	KURS12
40	4.0	2023-12-28 20:00:00	123124	KURS13
20	5.0	2023-12-26 20:00:00	123124	KURS11
\.


--
-- Data for Name: prowadzacy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prowadzacy (id, imie, nazwisko, haslo, email) FROM stdin;
1	Henryk	Wesoły	202cb962ac59075b964b07152d234b70	henryk.wesoly@gmail.com
2	Jan	Kowalski	202cb962ac59075b964b07152d234b70	jan.kowalski@example.com
3	Anna	Nowak	202cb962ac59075b964b07152d234b70	anna.nowak@example.com
4	Piotr	Wójcik	202cb962ac59075b964b07152d234b70	piotr.wojcik@example.com
5	Katarzyna	Dąbrowska	202cb962ac59075b964b07152d234b70	katarzyna.dabrowska@example.com
6	Marek	Lis	202cb962ac59075b964b07152d234b70	marek.lis@example.com
7	Joanna	Kaczmarek	202cb962ac59075b964b07152d234b70	joanna.kaczmarek@example.com
8	Tomasz	Kruk	202cb962ac59075b964b07152d234b70	tomasz.kruk@example.com
9	Alicja	Pawłowska	202cb962ac59075b964b07152d234b70	alicja.pawlowska@example.com
10	Robert	Zając	202cb962ac59075b964b07152d234b70	robert.zajac@example.com
11	Ewa	Michalak	202cb962ac59075b964b07152d234b70	ewa.michalak@example.com
\.


--
-- Data for Name: studenci; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.studenci (nr_albumu, imie, nazwisko, semestr, adres, haslo, email, id_kierunku) FROM stdin;
123124	Karolina	Wójcik	2	ul. Kwiatowa 5, Warszawa	202cb962ac59075b964b07152d234b70	karolina.wojcik@example.com	1
123125	Marcin	Lis	3	ul. Leśna 12, Kraków	202cb962ac59075b964b07152d234b70	marcin.lis@example.com	2
123126	Katarzyna	Kowalska	4	ul. Słoneczna 8, Gdańsk	202cb962ac59075b964b07152d234b70	katarzyna.kowalska@example.com	3
123127	Paweł	Nowak	5	ul. Polna 3, Poznań	202cb962ac59075b964b07152d234b70	pawel.nowak@example.com	4
123128	Aneta	Zając	6	ul. Jesienna 10, Wrocław	202cb962ac59075b964b07152d234b70	aneta.zajac@example.com	5
123129	Grzegorz	Michalak	2	ul. Radosna 15, Lublin	202cb962ac59075b964b07152d234b70	grzegorz.michalak@example.com	6
123130	Ola	Piotrowska	3	ul. Skoczna 22, Katowice	202cb962ac59075b964b07152d234b70	ola.piotrowska@example.com	7
123131	Michał	Kaczmarek	4	ul. Cicha 7, Łódź	202cb962ac59075b964b07152d234b70	michal.kaczmarek@example.com	8
123132	Aleksandra	Szymańska	5	ul. Spokojna 14, Szczecin	202cb962ac59075b964b07152d234b70	aleksandra.szymanska@example.com	9
123133	Artur	Wójcik	6	ul. Nadmorska 18, Gdynia	202cb962ac59075b964b07152d234b70	artur.wojcik@example.com	10
\.


--
-- Data for Name: studenci_kursy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.studenci_kursy (nr_albumu, id_kursu) FROM stdin;
123124	KURS1
123125	KURS2
123126	KURS3
123127	KURS4
123128	KURS5
123129	KURS6
123130	KURS7
123131	KURS8
123132	KURS9
123133	KURS10
123124	KURS15
123124	KURS14
123124	KURS13
123124	KURS12
123124	KURS11
\.


--
-- Name: kierunki_studiow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kierunki_studiow_id_seq', 1, false);


--
-- Name: komunikaty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.komunikaty_id_seq', 1, false);


--
-- Name: oceny_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.oceny_id_seq', 46, true);


--
-- Name: prowadzacy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.prowadzacy_id_seq', 1, false);


--
-- Name: kierunki_studiow kierunki_studiow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kierunki_studiow
    ADD CONSTRAINT kierunki_studiow_pkey PRIMARY KEY (id);


--
-- Name: komunikaty_kierunki_studiow komunikaty_kierunki_studiow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.komunikaty_kierunki_studiow
    ADD CONSTRAINT komunikaty_kierunki_studiow_pkey PRIMARY KEY (id_kierunku, id_komunikatu);


--
-- Name: komunikaty komunikaty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.komunikaty
    ADD CONSTRAINT komunikaty_pkey PRIMARY KEY (id);


--
-- Name: kursy kursy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kursy
    ADD CONSTRAINT kursy_pkey PRIMARY KEY (id);


--
-- Name: oceny oceny_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oceny
    ADD CONSTRAINT oceny_pkey PRIMARY KEY (id);


--
-- Name: prowadzacy prowadzacy_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prowadzacy
    ADD CONSTRAINT prowadzacy_email_key UNIQUE (email);


--
-- Name: prowadzacy prowadzacy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prowadzacy
    ADD CONSTRAINT prowadzacy_pkey PRIMARY KEY (id);


--
-- Name: studenci studenci_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studenci
    ADD CONSTRAINT studenci_email_key UNIQUE (email);


--
-- Name: studenci_kursy studenci_kursy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studenci_kursy
    ADD CONSTRAINT studenci_kursy_pkey PRIMARY KEY (nr_albumu, id_kursu);


--
-- Name: studenci studenci_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studenci
    ADD CONSTRAINT studenci_pkey PRIMARY KEY (nr_albumu);


--
-- Name: komunikaty_kierunki_studiow komunikaty_kierunki_studiow_id_kierunku_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.komunikaty_kierunki_studiow
    ADD CONSTRAINT komunikaty_kierunki_studiow_id_kierunku_fkey FOREIGN KEY (id_kierunku) REFERENCES public.kierunki_studiow(id);


--
-- Name: komunikaty_kierunki_studiow komunikaty_kierunki_studiow_id_komunikatu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.komunikaty_kierunki_studiow
    ADD CONSTRAINT komunikaty_kierunki_studiow_id_komunikatu_fkey FOREIGN KEY (id_komunikatu) REFERENCES public.komunikaty(id);


--
-- Name: kursy kursy_id_kierunku_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kursy
    ADD CONSTRAINT kursy_id_kierunku_fkey FOREIGN KEY (id_kierunku) REFERENCES public.kierunki_studiow(id);


--
-- Name: kursy kursy_id_prowadzacego_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kursy
    ADD CONSTRAINT kursy_id_prowadzacego_fkey FOREIGN KEY (id_prowadzacego) REFERENCES public.prowadzacy(id);


--
-- Name: oceny oceny_id_kursu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oceny
    ADD CONSTRAINT oceny_id_kursu_fkey FOREIGN KEY (id_kursu) REFERENCES public.kursy(id);


--
-- Name: oceny oceny_nr_albumu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oceny
    ADD CONSTRAINT oceny_nr_albumu_fkey FOREIGN KEY (nr_albumu) REFERENCES public.studenci(nr_albumu);


--
-- Name: oceny ocenykursystudenci; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oceny
    ADD CONSTRAINT ocenykursystudenci FOREIGN KEY (nr_albumu, id_kursu) REFERENCES public.studenci_kursy(nr_albumu, id_kursu) ON DELETE CASCADE;


--
-- Name: studenci studenci_id_kierunku_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studenci
    ADD CONSTRAINT studenci_id_kierunku_fkey FOREIGN KEY (id_kierunku) REFERENCES public.kierunki_studiow(id);


--
-- Name: studenci_kursy studenci_kursy_id_kursu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studenci_kursy
    ADD CONSTRAINT studenci_kursy_id_kursu_fkey FOREIGN KEY (id_kursu) REFERENCES public.kursy(id);


--
-- Name: studenci_kursy studenci_kursy_nr_albumu_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studenci_kursy
    ADD CONSTRAINT studenci_kursy_nr_albumu_fkey FOREIGN KEY (nr_albumu) REFERENCES public.studenci(nr_albumu);


--
-- PostgreSQL database dump complete
--

