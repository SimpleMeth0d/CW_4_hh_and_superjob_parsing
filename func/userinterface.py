from src.classes_api import HeadHunter, Super_job
import json


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
                    print(f"url - {item['url']}\nДолжность - {item['name']}\nЗ.п от - {item['salary_from']}\n"
                          f"З.п до - {item['salary_to']}\nОписание - {item['responsibility']}\n"
                          f"Дата - {item['data']}\n")

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

    elif platform =='1':
        while True:
            hh_instance.page = page
            hh_data = hh_instance.load_vacancy()

            combined_dict['HeadHunter'] = hh_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['HeadHunter']:
                print(f"\nurl - {platform['url']}\nДолжность - {platform['name']}\nЗ.п от - {platform['salary_from']}\n"
                      f"З.п до - {platform['salary_to']}\nОписание - {platform['responsibility']}\n"
                      f"Дата - {platform['data']}\n")
            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

    elif platform =='2':
        while True:
            sj_instance.page = page
            sj_data = sj_instance.load_vacancy()

            combined_dict['SuperJob'] = sj_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['SuperJob']:
                print(f"\nurl - {platform['url']}\nДолжность - {platform['name']}\nЗ.п от - {platform['salary_from']}\n"
                      f"З.п до - {platform['salary_to']}\nОписание - {platform['responsibility']}\n"
                      f"Дата - {platform['data']}\n")

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break
