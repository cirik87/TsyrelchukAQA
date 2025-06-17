# Задача 1 (Создание и вызов функций)
# Напиши функцию say_hello(), которая выводит (не возвращает) строку "Hello, Python!". Затем вызови эту функцию.


def say_hello():
    print("Hello, Python!")

say_hello()

# Задача 2 (Аргументы функций)
#
# Напиши функцию greet(name), которая принимает один аргумент name и возвращает (не печатает!) строку в формате:
# "Привет, [name]!"

def greet(name):
    if not isinstance(name, str):
        return "Имя должно быть строкой!"

    return (f"Привет, {name}!")

message = greet(1)
print(message)

# Задача 3 (Аргументы со значениями по умолчанию)
# Напиши функцию order(food, drink='чай'), которая:
# Принимает обязательный аргумент food (еда) и необязательный drink (напиток со значением по умолчанию 'чай').
# Возвращает строку в формате:
# "Ваш заказ: [food] и [drink]".

def order(food, drink='чай'):
    return (f"Ваш заказ: {food} и {drink}")

print(order("сэндвич"))

# Задача 4 (Возвращение данных из функций)
# Напиши функцию calculate(a, b, operation), которая:
# Принимает два числа (a, b) и строку operation ('+', '-', '*').
# Возвращает результат указанной операции:
# + → сумма,
# - → разность,
# * → произведение.

def calculate(a, b, operation):
    if operation == "*":
        return a * b
    elif operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    else:
        return "Введи нормальный знак"

print(calculate(5, 3, '1'))

# Задача 5 (Декораторы)
# Напиши декоратор repeat(n), который:
# Принимает число n и вызывает декорируемую функцию n раз.
# Возвращает результат последнего вызова.

def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Привет, {name}!")

greet("Анна")

def log_decorator(func):
    def wrapper():
        print("Выполняется функция...")
        result = func() # Вызов функции с аргументами
        return result
    return wrapper

@log_decorator
def say_hello():
    print("Привет!")

say_hello()

def double_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)*2 # Вызов функции с аргументами
        return res
    return wrapper

@double_decorator
def get_number():
    return 5

result = get_number()
print(result)

# Задача 9 (Раздел: Аргументы с дефолтными значениями)
# Напиши функцию с именем describe_person, которая принимает два аргумента:
# name — имя человека (строка),
# age — возраст, со значением по умолчанию 18.
# Функция должна выводить на экран строку вида:
# "Имя: [name], Возраст: [age]"
# Примеры вывода:
# describe_person("Анна", 25) → "Имя: Анна, Возраст: 25"
# describe_person("Борис") → "Имя: Борис, Возраст: 18"
# После определения функции — вызови её дважды: один раз с обоими аргументами, второй — только с именем.

def describe_person(name,age = 18):
    print (f"Имя: {name}, Возраст: {age}")
describe_person("Анна", 25)
describe_person("Борис")