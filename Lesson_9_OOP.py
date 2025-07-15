# Задача 1 (Раздел: Методы класса)
# Создай класс Rectangle с методом area(), который возвращает площадь прямоугольника.
# Ширина (width) и высота (height) должны передаваться в __init__.

class Rectangle:
    # Конструктор класса (инициализирует атрибуты)
    def __init__(self, width, height):
        self.width = width # Ширина
        self.height = height # Высота

    # Метод для вывода информации о машине
    def area(self):
        return  self.width * self.height


rect = Rectangle(5, 10)
print(rect.area())

# Задача 2 (Раздел: Параметр self)
# Создай класс Person с методом introduce(), который выводит строку:
# "Меня зовут {self.name}".
# Требования:
# В конструкторе __init__ принимай параметр name и сохраняй его в атрибут объекта.
# Метод introduce() должен использовать self.name для вывода фразы.

class Person:

    def __init__(self,name):
        self.name = name

    def introduce(self):
        print(f"Меня зовут {self.name}")

person = Person("Анна")
person.introduce()

# Задача 3 (Раздел: Общие атрибуты)
# Создай класс Dog со следующими требованиями:
# Общий атрибут (классовая переменная) species = "Собака"
# Атрибут экземпляра name, который передаётся при создании объекта
# Метод bark(), который выводит: "{name} говорит: Гав-гав!"

class Dog:
    species = "Собака"

    def __init__(self, name):
        self.name = name

    def bark(self):
        print(f"{self.name} говорит: Гав-гав!")

dog = Dog("Бобик")
print(dog.species)  # Должно вывести: "Собака"
dog.bark()

# Задача 4 (Раздел: Создание класса)
# Создай класс Book с:
# Атрибутом экземпляра title (передаётся при создании)
# Атрибутом экземпляра author (передаётся при создании)
# Методом info(), который возвращает строку в формате:
# "Книга: {title}, Автор: {author}"

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author

    def info(self):
        return f"Книга: {self.title}, Автор: {self.author}"

book = Book("1984", "Джордж Оруэлл")

print(book.info())

# Задача 5 (Раздел: Конструктор класса __init__)
# Создай класс Student с:
# Конструктором, принимающим три параметра:
# name (строка)
# age (число)
# major (строка, специальность)
# Методом introduce(), который возвращает строку:
# "Я {name}, мне {age} лет, изучаю {major}"

# Особые условия:
# В конструкторе должны быть проверки:
# age должен быть положительным числом
# name и major должны быть непустыми строками
# Если условия не выполняются, вызывай исключение ValueError с понятным сообщение

class Student:
    def __init__(self,name,age,major):
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if not name:
            raise ValueError("Имя не может быть пустым")
        if not major:
            raise ValueError("Специальность не может быть пустой")
        self.name = name
        self.age = age
        self.major = major

    def introduce(self):
        return f"Я {self.name}, мне {self.age} лет, изучаю {self.major}"

try:
    student = Student("Алексей", 20, "Информатику")
    print(student.introduce())
except ValueError as e:
    print(f"Ошибка: {e}")

# Задача 6 (Раздел: Методы класса и self)
# Создай класс BankAccount с:
# Атрибутами экземпляра:
# account_number (номер счета, строка)
# balance (баланс, число, по умолчанию 0)
# Методами:
# deposit(amount) — увеличивает баланс на указанную сумму (amount).
# withdraw(amount) — уменьшает баланс на amount, но не позволяет уйти в минус (если недостаточно средств, выводит "Недостаточно средств").
# check_balance() — возвращает строку: "Баланс счета {account_number}: {balance} руб.".
# Требования:
# Используй self для работы с атрибутами.
# В withdraw() должна быть проверка на достаточность средств.

class BankAccount:
    def __init__(self,account_number):
        self.account_number = account_number
        self.balance = 0

    def deposit(self,amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Недостаточно средств")

    def check_balance(self):
        return f"Баланс счета {self.account_number}: {self.balance} руб."

account = BankAccount("1234567890")
account.deposit(1000)
account.withdraw(500)
print(account.check_balance())
account.withdraw(600)

# Задача 7 (Раздел: Общие атрибуты и методы класса)
# Создай класс CoffeeMachine с:
# Общим атрибутом класса:
# water_level = 1000 (общий запас воды в мл для всех кофемашин)
# Атрибутами экземпляра:
# name (название кофемашины, передаётся в __init__)
# coffee_beans (количество кофейных зёрен в граммах, по умолчанию 0)
# Методами:
# add_beans(grams) — добавляет зёрна (увеличивает coffee_beans)
# make_coffee() — использует 200 мл воды и 20 г зёрен для приготовления кофе:
# Если ресурсов хватает, возвращает строку "Ваш кофе готов!" и уменьшает запасы
# Если чего-то не хватает, возвращает "Недостаточно ингредиентов"

class CoffeeMachine:
    water_level = 1000  # Общий уровень воды для всех машин

    def __init__(self, name):
        self.name = name
        self.coffee_beans = 0

    def add_beans(self, grams):
        self.coffee_beans += grams

    def make_coffee(self):  # Убрал параметр grams
        if self.coffee_beans >= 20 and CoffeeMachine.water_level >= 200:
            self.coffee_beans -= 20  # Фиксированное количество
            CoffeeMachine.water_level -= 200
            return "Ваш кофе готов!"  # Исправлена опечатка
        return "Недостаточно ингредиентов"


machine1 = CoffeeMachine("Кафе №1")
machine1.add_beans(50)
print(machine1.make_coffee())  # Ваш кофе готов!
print(CoffeeMachine.water_level)  # 800 (использовали 200 мл)

machine2 = CoffeeMachine("Кафе №2")
print(machine2.make_coffee()