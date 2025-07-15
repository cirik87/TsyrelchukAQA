# Задача 1 (Базовое наследование)
# Создай базовый класс Animal с методом make_sound(), который печатает "Some generic sound". Затем создай подкласс Dog, который наследует Animal и переопределяет make_sound(), чтобы печатать "Woof!".
#
# Проверь работу, создав экземпляр Dog и вызвав его метод.



class Animal:

    def __init__(self, name):
        self.name = name  # Атрибут экземпляра


    def make_sound(self):
        print( f"{self.name}Some generic sound")

class Dog(Animal):
    def make_sound(self):
        print(f"{self.name}  Woof!")  # Дополнительная логика

dog = Dog(name="Artem")
dog.make_sound()

# Задача 2 (переопределение методов + super()):
# Создай базовый класс Vehicle с методом start_engine(), который печатает "Engine started".
# Затем создай подкласс ElectricCar, который:
# Переопределяет start_engine(), чтобы печатать "Electric motor activated".
# Но также вызывает родительский метод через super(), чтобы напечатать "Engine started" (как у всех транспортных средств).

class Vehicle:
    def start_engine(self):
        print(f"Engine started")

class ElectricCar(Vehicle):
    def start_engine(self):
        super().start_engine()  # Вызов родительского метода
        print(f"Electric motor activated")

car = ElectricCar()
car.start_engine()

# Задача 3 (Наследование и добавление новых свойств)
# Создай базовый класс Person:
# Имеет атрибуты: name (строка) и age (число), которые задаются в __init__
# Имеет метод introduce(), который выводит: "Hi, I'm {name} and I'm {age} years old".
# Затем создай подкласс Student, который:
# Наследует все от Person.
# Добавляет новый атрибут student_id (строка), который принимается в __init__ после name и age.
# Переопределяет метод introduce(), чтобы он также выводил ID студента:
# "Hi, I'm {name}, {age} years old. My student ID is {student_id}".

class Person():
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def introduce(self):
        print(f"Hi, I'm {self.name}, {self.age} years old. My student ID is {self.student_id}")

student = Student(name="Alex", age=20, student_id="S12345")
student.introduce()

# Задача 4: "Фигуры"
# Создай базовый класс Shape с методами:
# area() — возвращает 0 (площадь)
# info() — печатает "This is a geometric shape"
# Затем создай два дочерних класса:
# Rectangle (наследует Shape):
# __init__ принимает width и height
# Переопределяет area() (формула: width * height)
# Переопределяет info(): "This is a rectangle with area {area()}"
# Circle (наследует Shape):
# __init__ принимает radius
# Переопределяет area() (формула: 3.14 * radius ** 2)
# Добавляет новый метод circumference() (длина окружности: 2 * 3.14 * radius)

class Shape():

    def area(self):
        return 0

    def info(self):
        print(f"This is a geometric shape")

class Rectangle(Shape):
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def info(self):
        print(f"This is a rectangle with area {self.area()}")

class Circle(Shape):
    def __init__(self,radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

    def circumference(self):
        return  2 * 3.14 * self.radius

r = Rectangle(width=4, height=5)
print(r.area())  # Должно вернуть 20
r.info()         # Должно напечатать "This is a rectangle with area 20"

c = Circle(radius=3)
print(c.area())          # Должно вернуть ~28.26
print(c.circumference())

# Задача 5: "Транспортная иерархия"
# Создай иерархию классов:
# Базовый класс Vehicle:
# Атрибуты: model (строка), year (число)
# Метод start_engine() → выводит "Engine started"
# Метод display_info() → выводит "Model: {model}, Year: {year}"
# Подкласс Car (наследует Vehicle):
# Добавляет атрибут: fuel_type ("gasoline"/"diesel"/"electric")
# Переопределяет display_info() → добавляет информацию о топливе
# (формат: "Model: {model}, Year: {year}, Fuel: {fuel_type}")
# Подкласс ElectricCar (наследует Car):
# Переопределяет start_engine() → выводит "Electric motor activated"
# Переопределяет display_info() → заменяет "Fuel" на "Power source: electric"

class Vehicle:
    def __init__(self,model,year):
        self.model = model
        self.year = year

    def start_engine(self):
        print(f"Engine started")

    def display_info(self):
        print(f"Model: {self.model}, Year: {self.year}")

class Car(Vehicle):
    def __init__(self,model,year,fuel_type):
        super().__init__(model,year)
        self.fuel_type = fuel_type

    def display_info(self):
        print(f"Model: {self.model}, Year: {self.year}, Fuel: {self.fuel_type}")

class ElectricCar(Car):
    def __init__(self,model,year):
        super().__init__(model, year, "electric")


    def start_engine(self):
        print(f"Electric motor activated")

    def display_info(self):
        print(f"Model: {self.model}, Year: {self.year}, Power source: electric")

v = Vehicle("Ford T", 1920)
c = Car("Toyota Camry", 2020, "gasoline")
e = ElectricCar("Tesla Model S", 2023)

v.display_info()  # "Model: Ford T, Year: 1920"
c.display_info()  # "Model: Toyota Camry, Year: 2020, Fuel: gasoline"
e.display_info()  # "Model: Tesla Model S, Year: 2023, Power source: electric"

v.start_engine()  # "Engine started"
e.start_engine()  # "Electric motor activated"
