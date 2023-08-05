import psycopg2
from src.config import config
import os


class DBManager:
    def __init__(self, filename=os.path.join("..", "database.ini")):
        params = config(filename)
        conn = psycopg2.connect(dbname='vacancy_db', **params)
        conn.autocommit = True
        self.cur = conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute(
            """
            SELECT employers.employer_name, COUNT(vacancies.employer_id)
            FROM employers 
            JOIN vacancies USING(employer_id)
            GROUP BY employers.employer_name
            ORDER BY COUNT(vacancies.employer_id) DESC
            """
            )
        [print(i[0], i[1]) for i in self.cur.fetchall()]

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute(
            """
            SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.vacancy_url
            FROM vacancies v
            JOIN employers e USING(employer_id)
            """
        )
        [print(i) for i in self.cur.fetchall()]

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cur.execute(
            """
            SELECT AVG(salary_from), AVG(salary_to)
            FROM vacancies
            """
        )
        print(self.cur.fetchall())

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям"""
        self.cur.execute(
            """
            SELECT * 
            FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
            OR salary_to > (SELECT AVG(salary_to) FROM vacancies)
            """
        )
        [print(i) for i in self.cur.fetchall()]

    def get_vacancies_with_keyword(self, word='python'):
        """Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например “python”"""
        word = '%' + word + '%'
        self.cur.execute(
            """
            SELECT * 
            FROM vacancies
            WHERE vacancy_name like %(word)s
            """, {'word': word}
        )
        [print(i) for i in self.cur.fetchall()]
