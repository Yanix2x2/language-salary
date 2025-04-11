from collections import defaultdict

import requests

from helper import predict_salary


def get_vacancies(lang):
    page = 0
    total_vacancies = {'items': []}

    url = 'https://api.hh.ru/vacancies'
    positions = 96
    town = 1
    days = 30
    per_page = 100
    params = {
        'professional_role': positions,
        'area': town,
        'period': days,
        'per_page': per_page,
        'page': page,
        'text': lang,
    } 
    pages_number = 1
    while page < pages_number:
        page_response = requests.get(url, params)
        page_response.raise_for_status()
        vacancies = page_response.json()
        total_vacancies['items'] += vacancies['items']
        total_vacancies['found'] = vacancies['found']
        pages_number = vacancies['pages']
        page += 1
    return total_vacancies


def predict_rub_salary(vacancy):
    salary = vacancy.get('salary')
    if not salary or salary['currency'] != 'RUR':
        return None
    salary_from = salary.get('from')
    salary_to = salary.get('to')
    return predict_salary(salary_from, salary_to)


def get_statistic():
    popular_langs = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go'
    ]
    statistic = defaultdict(int)
    for lang in popular_langs:
        vacancies = get_vacancies(lang)
        vacancies_processed = 0
        total = 0
        for vacancy in vacancies.get('items'):
            salary = predict_rub_salary(vacancy) 
            if salary:
                total += salary
                vacancies_processed += 1
        statistic[lang] = {
            'vacancies_found': vacancies.get('found'),
            'vacancies_processed': vacancies_processed
        }
        if vacancies_processed:
            statistic[lang]['average_salary'] = int(total // vacancies_processed)
        else:
            statistic[lang]["average_salary"] = None
    return statistic
