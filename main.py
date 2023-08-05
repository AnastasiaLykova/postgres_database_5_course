from src.hh_api import get_vacancies_hh
from src.fill_db import main as fill_db

if __name__ == "__main__":
    employers_id = [3776, 906557, 1740, 78638, 80, 39305, 139, 4649269, 2575750, 6120481]
    get_vacancies_hh(employers_id, 'python')
    fill_db("database.ini", "queries.sql", "vacancies.json")
