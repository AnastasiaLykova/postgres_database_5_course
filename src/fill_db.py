import json
import psycopg2
from src.config import config
import os


def main(filename=os.path.join("..", "database.ini"),
         script_file=os.path.join("..", "queries.sql"),
         json_file=os.path.join("..", "vacancies.json")):
    db_name = 'vacancy_db'

    params = config(filename)
    conn = None

    create_database(params, db_name)
    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:

                create_tables_script(cur, script_file)

                vacancies = get_vacancy_data(json_file)
                insert_vacancy_data(cur, vacancies)

                add_foreign_keys(cur)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """
    Создает новую базу данных
    :param params: параметры подключения к базе
    :param db_name: название новой базы данных
    :return:
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()


def create_tables_script(cur, script_file) -> None:
    """
    Создает в базе данных таблицы по sql скрипту
    :param cur:
    :param script_file: sql скрипт
    :return:
    """
    with open(script_file, 'r', encoding='utf-8') as sql:
        cur.execute(sql.read())


def get_vacancy_data(json_file: str):
    """
    Извлекает данные из JSON-файла и возвращает список словарей с соответствующей информацией
    :param json_file: файл json
    :return:
    """
    with open(json_file, 'r', encoding='utf') as file:
        vacancies = json.load(file)
        return vacancies


def insert_vacancy_data(cur, vacancies) -> None:
    """
    Заполняет базу данных вакансиями
    :param cur:
    :param vacancies: словарь с вакансиями
    :return:
    """
    employers_id = []
    for vacancy in vacancies.values():

        if vacancy['salary'] is not None:
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
        else:
            salary_from = None
            salary_to = None

        department_name = None if vacancy['department'] is None else vacancy['department']['name']
        area_name = None if vacancy['area'] is None else vacancy['area']['name']
        type_name = None if vacancy['type'] is None else vacancy['type']['name']
        address_raw = None if vacancy['address'] is None else vacancy['address']['raw']
        published_at = vacancy['published_at'][:10]
        snippet_requirement = None if vacancy['snippet'] is None else vacancy['snippet']['requirement']
        snippet_responsibility = None if vacancy['snippet'] is None else vacancy['snippet']['responsibility']
        experience_name = None if vacancy['experience'] is None else vacancy['experience']['name']
        employment_name = None if vacancy['employment'] is None else vacancy['employment']['name']

        cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, department, area, salary_from, salary_to, 
                type, address, published_at, vacancy_url, employer_id, requirement, responsibility, contacts, 
                experience, employment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id'], vacancy['name'], department_name, area_name,
                 salary_from, salary_to, type_name, address_raw, published_at,
                 vacancy['alternate_url'], vacancy['employer']['id'], snippet_requirement,
                 snippet_responsibility, vacancy['contacts'],
                 experience_name, employment_name)
                )

        employers_data = vacancy['employer']

        if employers_data['id'] not in employers_id:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name, employer_url) 
                VALUES (%s, %s, %s)
                """,
                (employers_data['id'], employers_data['name'], employers_data['alternate_url'])
            )
            employers_id.append(employers_data['id'])


def add_foreign_keys(cur) -> None:
    """
    Добавляет внешний ключ
    :param cur:
    :return:
    """
    cur.execute(
                """
                ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers
                FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                """
                )


if __name__ == '__main__':
    main()
