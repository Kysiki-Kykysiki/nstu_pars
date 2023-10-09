import requests
from bs4 import BeautifulSoup


def get_text(element, class_name):
    item = element.find(['div', 'span'], class_=class_name)
    return item.get_text(strip=True) if item else ''


def get_schedule(url):
    try:
        req = requests.get(url)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'html.parser')

        schedule_data = []
        current_day = None

        class_rows = soup.find_all('div', class_='schedule__table-row')

        for class_row in class_rows:
            day_rows = class_row.find('div', class_='schedule__table-day')
            day_text = day_rows.get_text(strip=True) if day_rows else ''

            if day_text:
                current_day = day_text

            class_data = class_row.find_all('div', class_='schedule__table-cell')
            if len(class_data) < 2:
                continue

            time = get_text(class_data[0], 'schedule__table-time')
            subject = get_text(class_data[1], 'schedule__table-item')
            type_work = get_text(class_data[1], 'schedule__table-typework')
            classroom = get_text(class_data[1], 'schedule__table-class')

            class_schedule = {
                'day': current_day,
                'time': time,
                'subject': subject.replace(classroom, '').replace(type_work, '').strip(),
                'type': type_work,
                'classroom': classroom
            }

            schedule_data.append(class_schedule)

        return schedule_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def main():
    group = input("Введите группу\n")
    week = input("Введите недельку\n")
    day = input("Введите денек\n")
    url = f'https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group={group}&week={week}'

    schedule = get_schedule(url)
    current_day = None

    for class_schedule in schedule:
        if day in str(class_schedule['day']):
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
