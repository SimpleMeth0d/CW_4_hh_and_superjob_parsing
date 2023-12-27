import os
import json
from abc import ABC, abstractmethod
from src.classes_api import HeadHunter, Super_job

class SaveToFile(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add_vacancy_hh(self, vacancy):
        pass

    @abstractmethod
    def add_vacancy_sj(self, vacancy):
        pass

    @abstractmethod
    def add_vacancy_both(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, id_vacancy: str):
        pass


class JsonSaveFile(SaveToFile):

    def __init__(self, title):
        self.name_file = title

    def add_vacancy_hh(self, vacancy: dict):
        """
        Метод добавления вакансий из HeadHunter в файл json
        :param vacancy: экземпляр класса Vacancy в dict
        :return:создает файл с вакансией и добавляет следующие вакансии в созданный файл
        """

        with open(f'{self.name_file}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['HeadHunter'].append(vacancy)
        with open(f'{self.name_file}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_vacancy_sj(self, vacancy: dict):
        """
        Метод добавления вакансий из SuperJob в файл json
        :param vacancy: экземпляр класса Vacancy в dict
        :return:создает файл с вакансией и добавляет следующие вакансии в созданный файл
        """

        with open(f'{self.name_file}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['SuperJob'].append(vacancy)
        with open(f'{self.name_file}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_vacancy_both(self, vacancy_hh, vacancy_sj):
        """
        Метод добавления вакансий в файл json
        :return:создает файл с вакансией и добавляет следующие вакансии в созданный файл
        """

        with open(f'{self.name_file}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data['HeadHunter'].append(vacancy_hh)
            data['SuperJob'].append(vacancy_sj)
        with open(f'{self.name_file}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def delete_vacancy(self, id_vacancy: str):
        """
        Метод для удаления из файла вакансии по id
        :param id_vacancy: id вакансии str
        :return: перезапись файла
        """
        with open(f'{self.name_file}.json', 'r') as file:
            data_file = json.load(file)
            for idx, txt in enumerate(data_file):
                if txt['id'] == id_vacancy:
                    print('Запись будет удалена')
                    data_file.pop(idx)
                    break

        with open(f'{self.name_file}.json', 'w') as file:
            json.dump(data_file, file, indent=2, ensure_ascii=False)

    def load_sorted_vacancies(self):
        '''
        Считывает файл json.
        Сортирует список словарей по зарплате.
        Возвращает список из 5ти последних операций
        '''
        with open(f'{self.name_file}.json', 'rt', encoding='utf-8') as file:
            vacancies = json.load(file)
            sorted_vacancies = sorted(vacancies.items(), key=lambda vacancies: ['salary_from'], reverse=True)
            list_of_five = []
            while len(list_of_five) < 5:
                for i in sorted_vacancies:
                    list_of_five.append(i)
            return list_of_five
