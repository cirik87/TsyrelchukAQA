# with open("exampl.txt","r",encoding="utf-8") as file:
#     content = file.read()
#     print(content)

# Задача 1 (Базовые операции с файлами)
# Создай файл numbers.txt и запиши в него числа от 1 до 5, каждое с новой строки.
# text
# 1
# 2
# 3
# 4
# 5
# Что нужно использовать:
# Открытие файла в режиме записи ('w').
# Цикл для перебора чисел.
#
# file = open("numbers.txt","w",encoding="utf-8")
# i=1
# while i<=5:
#     file.write( str(i) + "\n")
#     i+=1
# file.close()

file = open("numbers.txt","w",encoding="utf-8")
for i in range(1,6):
    file.write(str(i) + "\n")
file.close()

# Задача 2 (Контекстный менеджер with)
# Дан файл greeting.txt с одной строкой:
# Привет, мир!
# Напиши код, который:
# Открывает файл для чтения через with
# Выводит его содержимое в консоль
# (Ожидаемый вывод:)
# Привет, мир!
with open("greeting.txt","r",encoding="utf-8") as file:
    content = file.read()
    print(content)

# Задача 3 (Комбинированная: запись + чтение через with)
# Создай файл colors.txt, запиши в него 3 любимых цвета (каждый с новой строки), а затем выведи содержимое файла в консоль.
# Требования:
# Используй только контекстный менеджер with.
# Сначала открой файл в режиме записи ('w'), затем — в режиме чтения ('r').

colors = ["зеленый", "красный", "синий"]
with open("colors.txt","w",encoding="utf-8") as file:
    for color in colors:
        file.write(color + "\n")
with open("colors.txt","r",encoding="utf-8") as file:
    print(file.read())