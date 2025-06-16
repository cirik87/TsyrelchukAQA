# Задача 1 (Создание словаря)
# Создай словарь student с ключами:
# "name" (значение — твоё имя), "age" (твой возраст) и "courses"
# (список из двух любых курсов,
# например ["Math", "Art"]).
# Выведи словарь на экран.
from pymsgbox import password

student = {"name":"Виталик",
           "age" : "37",
           "courses": ["Math", "Art"]}
print(student)

# Задача 2 (Доступ к элементам словаря по ключу)
# Дан словарь:
# car = {"brand": "Toyota", "model": "Camry", "year": 2020}
# Выведи на экран значение, связанное с ключом "model", используя квадратные скобки [].

car = {"brand": "Toyota", "model": "Camry", "year": 2020}
print(car['model'])

# Задача 3 (Добавление и обновление элементов словаря)
# Дан словарь:
# phone = {"brand": "Samsung", "model": "Galaxy S21"}
# Добавь в него новый ключ "year" со значением 2021.
# Обнови значение ключа "model" на "Galaxy S22".
# Выведи изменённый словарь на экран.

phone = {"brand": "Samsung", "model": "Galaxy S21"}
phone["year"] = 2021
phone["model"] = "Galaxy S22"
print(phone)

# Задача 4 (Удаление элементов словаря)
# Дан словарь:
# laptop = {"brand": "Lenovo", "model": "ThinkPad", "year": 2022, "price": 1500}
# Удали ключ "price" с помощью оператора del.
# Удали ключ "year" с помощью метода .pop(), сохрани его значение в переменную deleted_year.
# Выведи итоговый словарь и значение deleted_year.

laptop = {"brand": "Lenovo", "model": "ThinkPad", "year": 2022, "price": 1500}
del laptop["price"]
deleted_year = laptop.pop("year")
print(laptop)
print(deleted_year)

# Задача 5 (Получение элементов, ключей и значений словаря)
# Дан словарь:
# book = {
#     "title": "Гарри Поттер",
#     "author": "Дж.К. Роулинг",
#     "year": 1997,
#     "genre": "фэнтези"
# }
# Выведи список всех ключей словаря
# Выведи список всех значений словаря
# Выведи список всех пар (ключ, значение) в виде кортежей

book = {
    "title": "Гарри Поттер",
    "author": "Дж.К. Роулинг",
    "year": 1997,
    "genre": "фэнтези"
}
print(list(book.keys()))
print(list(book.values()))
print(list(book.items()))

# Задача 6 (Проверка на наличие ключей и значений)
# Дан словарь:
# movie = {
#     "title": "Назад в будущее",
#     "year": 1985,
#     "director": "Роберт Земекис",
#     "genre": "фантастика"
# }
# Проверь, есть ли ключ "director" в словаре (выведи True или False)
# Проверь, есть ли значение "фантастика" среди значений словаря (выведи True или False)
# Дополнительно: Проверь отсутствие ключа "budget" (выведи True, если его нет)

movie = {
    "title": "Назад в будущее",
    "year": 1985,
    "director": "Роберт Земекис",
    "genre": "фантастика"
}
print("director" in movie)
print("фантастика" in movie.values())
print("budget" not in movie)

# Задача 7 (Комбинированная работа со словарём)
# Дан словарь игрового персонажа:
# character = {
#     "name": "Эльф",
#     "level": 12,
#     "skills": ["Лук", "Скрытность"],
#     "gold": 450
# }
# Добавь новый навык "Магия" в список skills
# Увеличь количество gold на 150
# Проверь, есть ли ключ "inventory" (выведи True или False)
# Выведи итоговый словарь

character = {
    "name": "Эльф",
    "level": 12,
    "skills": ["Лук", "Скрытность"],
    "gold": 450
}
character["skills"].append("Магия")
character["gold"] = character["gold"] + 150
print("inventory" in character)
print(character)

# Задача 8 (Генерация словаря + методы)
# Создай словарь user с ключами:
# "login" (значение — любое имя)
# "password" (любой пароль)
# "age" (любой возраст от 18 до 30)
# Затем:
# Удали ключ "password" с помощью .pop()
# Добавь новый ключ "hobbies" со значением-списком из 3 хобби
# Выведи:
# Все ключи словаря
# Все значения словаря
# Все пары ключ-значение

user = {"login":"Anna",
        "password":"QWERTY",
        "age":25
        }
user.pop("password")
user["hobbies"]= ["Рисование", "Музыка", "Прогулки"]
print(f"Ключи: {list(user.keys())}")
print(f"Значения: {list(user.values())}")
print(f"Пары: {list(user.items())}")

# Задача 9 (Глубокая работа со словарём)
# Дан словарь библиотеки:
# library = {
#     "name": "Центральная библиотека",
#     "books": {
#         "фантастика": ["Дюна", "1984"],
#         "детективы": ["Шерлок Холмс"]
#     }
# }
# Добавь в жанр "фантастика" книгу "Гарри Поттер"
# Создай новый жанр "роман" с книгой "Война и мир"
# Удали жанр "детективы" (вместе со списком книг)
# Выведи:
# Все книжные жанры (только названия)
# Все книги в жанре "фантастика"
# Общее количество книг в библиотеке

library = {
    "name": "Центральная библиотека",
    "books": {
        "фантастика": ["Дюна", "1984"],
        "детективы": ["Шерлок Холмс"]
    }
}
library["books"]["фантастика"].append("Гарри Поттер")
library["books"]["роман"] = ["Война и мир"]
del library["books"]["детективы"]
print(f"Жанры: {list(library['books'].keys())}")
print(f"Фантастика: {library['books']['фантастика']}")
print(f"Всего книг: {sum(len(books) for books in library['books'].values())}")

# Финальная задача: "Учёт сотрудников компании"
# Ты — разработчик системы учёта сотрудников. Нужно создать программу для обработки данных о командах и их участниках.
# Исходные данные:
# company = {
#     "teams": {
#         "Разработка": ["Алексей", "Мария", "Иван"],
#         "Маркетинг": ["Ольга", "Пётр"],
#         "Дизайн": ["Елена"]
#     },
#     "positions": {
#         "Алексей": "Team Lead",
#         "Мария": "Junior",
#         "Иван": "Middle",
#         "Ольга": "Head of Marketing",
#         "Пётр": "Analyst",
#         "Елена": "UX/UI Designer"
#     }
# }
# Задачи:
# Добавление нового сотрудника
# В команду "Дизайн" добавь нового сотрудника "Артём" (должность — "Junior Designer").
# Создай новую команду "Аналитика" с сотрудником "Дарья" (должность — "Data Scientist").
# Удаление сотрудника
# Удали "Пётр" из команды "Маркетинг" и его должность.
# Повышение сотрудника
# Измени должность "Мария" с "Junior" на "Middle".
# Анализ данных
# Выведи:
# Количество команд в компании.
# Имя сотрудника с должностью "Team Lead".
# Всех junior-сотрудников (должности содержат слово "Junior").

company = {
    "teams": {
        "Разработка": ["Алексей", "Мария", "Иван"],
        "Маркетинг": ["Ольга", "Пётр"],
        "Дизайн": ["Елена"]
    },
    "positions": {
        "Алексей": "Team Lead",
        "Мария": "Junior",
        "Иван": "Middle",
        "Ольга": "Head of Marketing",
        "Пётр": "Analyst",
        "Елена": "UX/UI Designer"
    }
}
company["teams"]["Дизайн"].append("Артём")
company["positions"]["Артём"] ="Junior Designer"
company["teams"]["Аналитика"] = ["Дарья"]
company["positions"]["Дарья"] ="Data Scientist"


company["teams"]["Маркетинг"].remove("Пётр")
company["positions"].pop("Пётр", None)
company["positions"]["Мария"] ="Middle"

summa = len(company["teams"])
print(f"Команд в компании: {summa}")

team_lead = [name for name, pos in company["positions"].items() if pos == "Team Lead"][0]

juniors = [name for name, pos in company["positions"].items() if "Junior" in pos]

print(f"Team Lead: {team_lead}")
print(f"Junior-сотрудники: {juniors}")