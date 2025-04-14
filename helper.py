from terminaltables import AsciiTable


def get_table(title, statistic):
    table_data = [
        [
            'Язык программирования', 
            'Вакансий найдено', 
            'Вакансий обработано',  
            'Средняя зарплата'  
        ]
    ]

    for lang, info in statistic.items():
        table_data.append([
            f'{lang}', 
            f'{info["vacancies_found"]}',
            f'{info["vacancies_processed"]}',
            f'{info["average_salary"]}'
        ])

    table = AsciiTable(table_data, title=title)
    return table.table


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    elif not salary_from:
        return salary_to * 1.2
    elif not salary_to:
        return salary_from * 0.8
    else:
        return (salary_from + salary_to) // 2
