from collections import defaultdict

import requests

from helper import predict_salary


def get_vacancies(secret_key, lang):
    url = 'https://api.superjob.ru/2.0/vacancies/'

    page = 0
    vacancies = []
    next_page_exists = True

    headers = {'X-Api-App-Id': secret_key}
    town = 4
    per_page = 100
    position_id = 48
    params = {
        't': town,
        'count': per_page,
        'page': page,
        'catalogues': position_id,
        'keyword': lang
    }

    while next_page_exists:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        api_response = response.json()
        vacancies += api_response.get('objects')
        total_vacancies = int(api_response.get('total'))
        next_page_exists = api_response.get('more')
        params['page'] += 1
    
    return vacancies, total_vacancies


def predict_rub_salary_for_superJob(vacancy):
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    if vacancy['currency'] != 'rub':
        return None 
    return predict_salary(salary_from, salary_to)


def get_statistic(secret_key):
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
        vacancies, total_vacancies = get_vacancies(secret_key, lang)
        total = 0
        vacancies_processed = 0
        for vacancy in vacancies:
            salary = predict_rub_salary_for_superJob(vacancy) 
            if salary:
                total += salary
                vacancies_processed += 1
        statistic[lang] = { 
            "vacancies_found": total_vacancies,
            "vacancies_processed": vacancies_processed,
        }
        if vacancies_processed:
            statistic[lang]["average_salary"] = int(total // vacancies_processed)
        else:
            statistic[lang]["average_salary"] = None
    return statistic
