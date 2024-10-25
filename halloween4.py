from tkinter import *  # Імпортуємо всі компоненти бібліотеки tkinter для створення графічного інтерфейсу
from random import randint, choice  # Імпортуємо функції для генерації випадкових чисел і випадкового вибору елементів

# Клас для об'єктів
class Creature:
    def __init__(self, x, y=0):
        images = ["spider.png", "bat.png", "eae.png", "snale.png"]  # Список зображень для об'єктів
        self.img_file = choice(images)  # Вибираємо випадкове зображення з цього списку
        self.img = PhotoImage(file=self.img_file).subsample(10, 10)  # Завантажуємо зображення і зменшуємо його розмір
        self.speed = randint(1, 5)  # Встановлюємо випадкову швидкість від 1 до 5
        self.x = x  # Початкова позиція по осі x
        self.y = y  # Початкова позиція по осі y
        self.image = canv.create_image(self.x, self.y, image=self.img)  # Додаємо зображення об'єкта на полотно
        canv.tag_bind(self.image, '<Button-1>', self.remove)  # Додаємо можливість видалення об'єкта при натисканні миші

    def move(self):
        if not is_paused.get():  # Перевіряємо, чи гра не на паузі
            self.y += self.speed  # Збільшуємо координату y на значення швидкості
            canv.move(self.image, 0, self.speed)  # Переміщуємо об'єкт вниз по полотну
            if self.y > 500:  # Перевіряємо, чи об'єкт не вийшов за межі екрану
                self.y = 0  # Повертаємо об'єкт на верхню межу екрана
                canv.coords(self.image, self.x, self.y)  # Оновлюємо координати об'єкта

    def remove(self, event):
        canv.delete(self.image)  # Видаляємо зображення об'єкта з полотна
        list_creatures.remove(self)  # Видаляємо об'єкт зі списку об'єктів


list_creatures = []  # Порожній список для зберігання об'єктів


# Функція для створення об'єктів
def create_creatures():
    # Очищаємо список і видаляємо всі об'єкти з полотна перед створенням нових
    for creature in list_creatures:
        canv.delete(creature.image)  # Видаляємо зображення кожного об'єкта з полотна
    list_creatures.clear()  # Очищаємо список об'єктів

    # Створюємо об'єкти залежно від обраної кількості
    for _ in range(max_creatures.get()):
        x_position = randint(0, 500)  # Випадкове значення для x
        creature = Creature(x_position, 0)  # Створюємо новий об'єкт з випадковою позицією x
        list_creatures.append(creature)  # Додаємо новий об'єкт до списку


# Функція для переміщення всіх об'єктів
def draw():
    for el in list_creatures:  # Проходимо по кожному об'єкту в списку
        el.move()  # Викликаємо метод руху для кожного об'єкта
    canv.after(100, draw)  # Оновлюємо положення об'єктів кожні 100 мс


# Функція для переміщення прицілу
def move_pricel(event):
    canv.coords(pricel, event.x, event.y)  # Оновлюємо координати прицілу відповідно до руху миші


# Функції для керування грою
def pause_game():
    is_paused.set(True)  # Встановлюємо гру на паузу


def resume_game():
    is_paused.set(False)  # Продовжуємо гру


# Головне вікно та полотно
root = Tk()  # Створюємо головне вікно програми
root.title("Гра з падаючими об'єктами")  # Назва вікна
canv = Canvas(root, width=500, height=500, bg="white")  # Створюємо полотно розміром 500x500 з білим фоном
canv.pack()  # Додаємо полотно до вікна

# Зображення фону та прицілу
bg_img = PhotoImage(file="background.png")  # Завантажуємо зображення фону
canv.create_image(0, 0, anchor=NW, image=bg_img)  # Додаємо зображення фону на полотно

pricel_img = PhotoImage(file="pricel.png")  # Завантажуємо зображення прицілу
pricel = canv.create_image(250, 250, image=pricel_img)  # Створюємо зображення прицілу на полотні
canv.bind("<Motion>", move_pricel)  # Прив'язуємо функцію руху прицілу до події руху миші

# Налаштування паузи та кількості об'єктів
is_paused = BooleanVar(value=False)  # Змінна для контролю стану паузи
max_creatures = IntVar(value=5)  # Змінна для контролю кількості об'єктів


# Панель керування внизу
control_frame = Frame(root)  # Створюємо панель для елементів управління
control_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)  # Додаємо панель внизу вікна

# Внутрішній фрейм для центрування елементів управління
inner_control_frame = Frame(control_frame)  # Створюємо внутрішню панель для елементів управління
inner_control_frame.pack(side=TOP, anchor=CENTER)  # Центруємо елементи управління

pause_button = Button(inner_control_frame, text="STOP", command=pause_game)  # Кнопка для зупинки гри
pause_button.pack(side=LEFT, padx=5)  # Додаємо кнопку до панелі

resume_button = Button(inner_control_frame, text="GAME", command=resume_game)  # Кнопка для продовження гри
resume_button.pack(side=LEFT, padx=5)  # Додаємо кнопку до панелі

Label(inner_control_frame, text="Кількість об'єктів:").pack(side=LEFT, padx=5)  # Текстове поле для кількості об'єктів
creature_count_scale = Scale(inner_control_frame, from_=1, to=20, orient=HORIZONTAL, variable=max_creatures,
                             command=lambda _: create_creatures())  # Повзунок для налаштування кількості об'єктів
creature_count_scale.pack(side=LEFT, padx=5)  # Додаємо повзунок до панелі

# Запуск гри
draw()  # Запускаємо функцію переміщення об'єктів
create_creatures()  # Створюємо об'єкти згідно з вибраною кількістю

root.mainloop()  # Запускаємо основний цикл програми
