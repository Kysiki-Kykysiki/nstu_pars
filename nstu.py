import requests
from bs4 import BeautifulSoup


def get_schedule(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    schedule_data = []

    class_rows = soup.find_all('div', class_='schedule__table-row')
    for class_row in class_rows:
        class_data = class_row.find_all('div', class_='schedule__table-cell')
        if len(class_data) < 2:
            continue

        time_element = class_data[0].find('div', class_='schedule__table-time')
        if time_element:
            time = time_element.get_text(strip=True)
        else:
            time = ''

        item = class_data[1].find('div', attrs={'data-type': 'item'})

        if item:
            subject = item.get_text(strip=True)
            classroom_element = item.find('span', class_='schedule__table-class')
            if classroom_element:
                classroom = classroom_element.get_text(strip=True)
            else:
                classroom = ''
        else:
            subject, classroom = '', ''

        class_schedule = {
            'time': time,
            'subject': subject,
            'classroom': classroom
        }

        schedule_data.append(class_schedule)

    return schedule_data


def main():
    print("Введите группу")
    group = input()
    url = f'https://www.nstu.ru/studies/schedule/schedule_classes/schedule?group={group}'
    schedule = get_schedule(url)

    for class_schedule in schedule:
        if (class_schedule['time'] and class_schedule['subject'] and class_schedule['classroom']):
            print(f"Время: {class_schedule['time']}")
            print(f"Предмет: {class_schedule['subject']}")
            print(f"Аудитория: {class_schedule['classroom']}")
            print('-' * 50)


if __name__ == '__main__':
    main()
