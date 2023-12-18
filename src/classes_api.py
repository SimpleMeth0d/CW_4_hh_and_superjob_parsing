import requests
from datetime import datetime
import os
from abc import ABC, abstractmethod


class APIManager(ABC):

    @abstractmethod
    def get_vacancies(self):
        """Получает вакансии по апи, возвращает список согласно запросу пользователя"""
        pass


class Vacancy:
    def __init__(self, name, page, per_page):
        self.name = name
        self.page = page
        self.per_page = per_page

    def __repr__(self):
        return f'{self.name}'


class HeadHunter(Vacancy, APIManager):
    """
    Класс для подключения по АПИ к hh.ru. Реализованы два метода один возвращает данные о вакансиях в формате json.
    Второй метод возвращает массив вакансий с необходимыми полями.
    """
    def __init__(self, name, page, per_page):
        super().__init__(name, page, per_page)
        self.url = 'https://api.hh.ru'
        # self.__params = {
        #     'text': self.name,  # Поиска вакансии по имени
        #     'page': self.page,  # Страница в HH
        #     'per_page': self.per_page,  # Количество вакансий на 1 странице
        # }

    def get_vacancies(self):
        """
        Отправляет Get запрос к сайту hh.ru с поиском вакансии по наименованию.
        :return: Данные о вакансиях в формате Json.
        """

        data = requests.get(f'{self.url}/vacancies', params={'text': self.name, 'page': self.page, 'per_page': self.per_page}).json()
        return data

    def load_vacancy(self):
        """
        Проходит в цикле по каждой вакансии и записывает в словарь необходимые данные о вакансии.
        :return: Массив вакансий с нужными атрибутами
        """
        data = self.get_vacancies()
        vacancies = []
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'url': vacancy['alternate_url'],
                'name': vacancy['name'],
                'salary_from': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'salary_to': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vacancies.append(vacancy_info)

        return vacancies


class Super_job(Vacancy, APIManager):
    """
    Класс для подключения по АПИ к super.job. Реализованы два метода один возвращает данные о вакансиях в формате Json.
    Второй метод возвращает массив вакансий с необходимыми полями.
    """
    def __init__(self, name, page, per_page):
        super().__init__(name, page, per_page)
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        # self.__params = {
        #     'keywords': self.name,
        #     'page': self.page,
        #     'count': self.per_page
        # }

    def get_vacancies(self):
        """
        Отправляет Get запрос к сайту super.job с поиском вакансии по ключевому слову.
        :return: Данные о вакансиях в формате Json.
        """
        headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('SJob_API_KEY'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application / x-www-form-urlencoded',
        }
        data = requests.get(self.url, headers=headers, params={'keywords': self.name, 'page': self.page, 'count': self.per_page}).json()
        return data

    def load_vacancy(self):
        """
        Проходит в цикле по каждой вакансии и записывает в словарь необходимые данные о вакансии.
        :return: Массив вакансий с нужными атрибутами
        """
        data = self.get_vacancies()
        vacancy_list_SJ = []
        for i in data['objects']:
            published_at = datetime.fromtimestamp(i.get('date_published', ''))
            super_job = {
                'url': i['link'],
                'name': i.get('profession', ''),
                'salary_from': i.get('payment_from', '') if i.get('payment_from') else None,
                'salary_to': i.get('payment_to') if i.get('payment_to') else None,
                'responsibility': i.get('candidat').replace('\n', '').replace('•', '') if i.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),
            }
            vacancy_list_SJ.append(super_job)
        return vacancy_list_SJ
