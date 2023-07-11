import datetime


def get_birthdays_per_week(users):
    today = datetime.date.today()
    # Номер поточного дня тижня (0 - понеділок, 6 - неділя)
    current_weekday = today.weekday()

    # Створюємо список днів тижня
    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Зміщуємо список днів тижня так, щоб поточний день був першим
    weekdays = weekdays[current_weekday:] + weekdays[:current_weekday]

    # Проходимо по кожному дню тижня
    for i, weekday in enumerate(weekdays):
        # Обчислюємо дату для поточного дня тижня
        date = today + datetime.timedelta(days=i)

        # Виводимо користувачів, які мають день народження в поточний день тижня
        
        birthday_users = [user['name'] for user in users if user['birthday'].day ==
                          date.day and user['birthday'].month == date.month]
        if birthday_users:
            print(f"{weekday}: ", end="")
            print(", ".join(birthday_users))
       


# Приклад використання
users = [
    {'name': 'Bill', 'birthday': datetime.datetime(2023, 7, 9)},
    {'name': 'Jill', 'birthday': datetime.datetime(2023, 6, 19)},
    {'name': 'Kim', 'birthday': datetime.datetime(2023, 7, 7)},
    {'name': 'Jan', 'birthday': datetime.datetime(2023, 6, 23)},
]

get_birthdays_per_week(users)
