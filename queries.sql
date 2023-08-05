--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';

SET default_with_oids = false;

---
--- drop tables
---

DROP TABLE IF EXISTS employers;
DROP TABLE IF EXISTS vacancies;


CREATE TABLE employers (
    employer_id integer PRIMARY KEY,
    employer_name text,
    employer_url text
);

CREATE TABLE vacancies (
    vacancy_id integer PRIMARY KEY,
    vacancy_name text,
    department text,
    area text,
    salary_from integer,
    salary_to integer,
    type text,
    address text,
    published_at date,
    vacancy_url text,
    employer_id integer,
    requirement text,
    responsibility text,
    contacts text,
    experience text,
    employment text
);
