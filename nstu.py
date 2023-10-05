import requests
from bs4 import BeautifulSoup


def get_schedule(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    schedule_data = []
    current_day = None  # Переменная для отслеживания текущего дня

    class_rows = soup.find_all('div', class_='schedule__table-row')

    for class_row in class_rows:
        day_rows = class_row.find('div', class_='schedule__table-day')
        day_text = day_rows.get_text(strip=True) if day_rows else ''

        # Если день изменился, обновляем current_day
        if day_text:
            current_day = day_text

        class_data = class_row.find_all('div', class_='schedule__table-cell')
        if len(class_data) < 2:
            continue

        time_element = class_data[0].find('div', class_='schedule__table-time')
        if time_element:
            time = time_element.get_text(strip=True)
        else:
            time = ''

        item = class_data[1].find('div', class_='schedule__table-cell')

        if item:
            subject_element = item.find('div', class_='schedule__table-item')
            work_type = item.find('span', class_='schedule__table-typework')
            subject_text = subject_element.get_text(strip=True) if subject_element else ''
            work_type_text = work_type.get_text(strip=True) if work_type else ''
            classroom_element = item.find('span', class_='schedule__table-class')
            classroom_text = classroom_element.get_text(strip=True) if classroom_element else ''
            subject = subject_text.replace(classroom_text, '').replace(work_type_text, '').strip()
            classroom = classroom_text
            type_work = work_type_text
        else:
            subject, classroom, type_work = '', '', ''

        class_schedule = {
            'day': current_day,  # Используем текущий день
            'time': time,
            'subject': subject,
            'type': type_work,
            'classroom': classroom
        }

        schedule_data.append(class_schedule)

    return schedule_data


def main():
    print("Введите группу")
    group = input()
    url = f'https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group={group}'
    schedule = get_schedule(url)
    current_day = None  # Переменная для отслеживания текущего дня

    for class_schedule in schedule:
        # Проверяем, изменился ли день
        if class_schedule['day'] != current_day:
            print(f"День: {class_schedule['day']}")
            current_day = class_schedule['day']

        if (class_schedule['time'] and class_schedule['subject'] and class_schedule['classroom']):
            print(f"Время: {class_schedule['time']}")
            print(f"Предмет: {class_schedule['subject']}")
            print(f"Тип пары: {class_schedule['type']}")
            print(f"Аудитория: {class_schedule['classroom']}")
            print('-' * 50)


if __name__ == '__main__':
    main()
