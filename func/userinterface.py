from src.classes_api import HeadHunter, Super_job
from src.class_save_to_file import JsonSaveFile
import json
import os


def job_vacancy():
    """
    Функция для взаимодействия с пользователем и создания json файла.
    После внесения пользователем данных, данные сортируются согласно запросу пользователя и вносятся в json файл.
    Далее выбирается площадка для поиска вакансий если пользователь хочет еще просмотреть вакансии вводит 'y',
    подгружаются новые вакансии и перезаписывается файл json и так до бесконечности
    """
    name = input('Введите желаемую должность: ')
    per_page = input('Введите кол-во вакансий на странице: ')
    page = int(input('Введите страницу: '))
    hh_instance = HeadHunter(name, page, per_page)
    sj_instance = Super_job(name, page, per_page)
    json_file = JsonSaveFile('vacancies')
    combined_dict = {'HeadHunter': hh_instance.load_vacancy(), 'SuperJob': sj_instance.load_vacancy()}

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

    platform = input('Введите сайт для поиска: (1 - HeadHunter, 2 - SuperJob, 3 - оба сайта)\n')

    if platform =='3':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.load_vacancy()
            sj_data = sj_instance.load_vacancy()

            combined_dict['HeadHunter'] = hh_data
            combined_dict['SuperJob'] = sj_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform, data in combined_dict.items():
                print(f"\n Платформа: {platform}")
                for item in data:
                    print(f"id - {item['id']}\nurl - {item['url']}\nДолжность - {item['name']}\n"
                          f"З.п от - {item['salary_from']}\nЗ.п до - {item['salary_to']}\n"
                          f"Описание - {item['responsibility']}\nДата - {item['data']}\n")

            user_choice = input('перейти на следующую страницу? y/n ')
            if user_choice == 'y':
                page += 1
            else:
                break

    elif platform =='1':
        while True:
            hh_instance.page = page
            hh_data = hh_instance.load_vacancy()

            combined_dict['HeadHunter'] = hh_data

            for platform in combined_dict['HeadHunter']:
                print(f"\nid - {platform['id']}\nurl - {platform['url']}\nДолжность - {platform['name']}\n"
                      f"З.п от - {platform['salary_from']}\nЗ.п до - {platform['salary_to']}\n"
                      f"Описание - {platform['responsibility']}\nДата - {platform['data']}\n")

            if not os.path.exists('vacancies.json'):
                with open('vacancies.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)

            user_choice = input('перейти на следующую страницу? y/n ')
            if user_choice == 'y':
                page += 1
                with open('vacancies.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # new_dict = hh_data
                    data['HeadHunter'].append(hh_data)
                with open('vacancies.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)
            else:
                break

    elif platform =='2':
        while True:
            sj_instance.page = page
            sj_data = sj_instance.load_vacancy()

            combined_dict['SuperJob'] = sj_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(sj_data, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['SuperJob']:
                print(f"\nid - {platform['id']}\nurl - {platform['url']}\nДолжность - {platform['name']}\n"
                      f"З.п от - {platform['salary_from']}\nЗ.п до - {platform['salary_to']}\n"
                      f"Описание - {platform['responsibility']}\nДата - {platform['data']}\n")

            user_choice = input('перейти на следующую страницу? y/n ')
            if user_choice == 'y':
                page += 1
                json_file.add_vacancy_sj(sj_data)
            else:
                break

    user_sort = input('\nВывести топ 5 вакансий по зарплате? y/n ')
    if user_sort == 'y':
        print(json_file.load_sorted_vacancies())
