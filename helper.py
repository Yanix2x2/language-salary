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

    for lang in statistic:
        table_data.append([
            f'{lang}', 
            f'{statistic[lang]["vacancies_found"]}',
            f'{statistic[lang]["vacancies_processed"]}',
            f'{statistic[lang]["average_salary"]}'
            ])

    table = AsciiTable(table_data, title=title)
    return table.table


def predict_salary(salary_from, salary_to):
    if not salary_from and not salary_to:
        return None
    elif salary_from is None:
        return salary_to * 1.2
    elif salary_to is None:
        return salary_from * 0.8
    else:
        return (salary_from + salary_to) // 2
