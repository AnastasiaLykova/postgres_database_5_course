import json
import requests
import os


def get_vacancies_hh(employers_id: list, keyword: str, page=1, per_page=100):
    """
    На вход получает список id работодателей и ключевое слово для поиска.
    Обращается к сайту HH, после получения ответа записывает полученные вакансии
    в файл vacancies.json, в основной директории
    :param employers_id: список id работодателей
    :param keyword: ключевое слово
    :param page: количество страниц
    :param per_page:  количество вакансий на странице
    :return:
    """
    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "Anastasia Lykova"}
    vacancies_dict = {}

    for id in employers_id:
        for number in range(0, page+1):
            params = {'employer_id': id, "text": keyword, "area": 113, "page": number, "per_page": per_page}
            response = requests.get(url, params=params, headers=headers)
            response = response.content.decode()
            json_hh = json.loads(response)
            for vacancy in json_hh['items']:
                vacancies_dict[vacancy['id']] = vacancy

    with open(os.path.join("..", "vacancies.json"), 'w', encoding="utf-8") as file:
        json.dump(vacancies_dict, file, ensure_ascii=False, indent=4)
