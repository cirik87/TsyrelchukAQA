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