from abc import ABC, abstractmethod
import random as rnd
import os


class Flight:
    base = {}
    name_file = 'schedule'
    file_txt = os.listdir()[1].split('.')[0]

    # Получение базы данных из файла
    try:
        with open('schedule.txt', 'r', encoding='utf-8') as file:
            for txt in file:
                lst = [txt.rstrip().split('_')]
                for item in lst:
                    time = item[0]
                    city = item[2]
                    base[item[1]] = [time, city]
    except FileNotFoundError:
        print('Файл для считывания информации аэропорта отсутствует!')

    def delay(self, index, time: int):  # Функция задержки рейса
        if index in self.base.keys():
            t = list(map(int, self.base[index][0].split(':')))
            hour = t[0] * 60
            min = t[1]
            result = hour + min + time
            result_hour = result // 60
            result_min = result % 60
            self.base[index][0] = str(result_hour) + ':' + str(result_min)

            if int(self.base[index][0][:2]) >= 24:
                print('Рейс переносится на следующий день')
                del self.base[index]
            else:
                print(f'Борт под номером {index}: задержан на {time} минут')


class Schedule(Flight):
    def show_scoreboard(self):  # Вывод на экран каждого рейса
        if len(self.base) != 0:
            for k, v in self.base.items():
                print(f'Борт под номером {k}, вылетает в {v[0]}, в страну {v[1]}')
        else:
            print('Аэропорт закрыт')

    def show_time(self, city):  # Метод для покупки билетов
        lst = set(x[1] for x in self.base.values())
        time_country = []
        if city in lst:
            for item in self.base.values():
                if city in item:
                    time_country.append(item[0])
                    print(f'Данный рейс доступен по времени {item[0]}')
        else:
            print('Извините рейсы в данную страну отсутствуют')

        return time_country


class Airplane(ABC):  # Создание абстрактного класса
    count_seats = 0
    type_airplane = 'Not Defined'

    @abstractmethod
    def count_return(self):
        pass

    @abstractmethod
    def airplane_return(self):
        pass


class Airbus319(Airplane):  # Создание наследуемого класса
    def count_return(self):
        self.count_seats = 110
        return self.count_seats

    def airplane_return(self):
        self.type_airplane = 'Пассажирский'
        return self.type_airplane

    def __str__(self):
        return f'Airbus319'


class Boeing737(Airplane):  # Создание наследуемого класса
    def count_return(self):
        self.count_seats = 100
        return self.count_seats

    def airplane_return(self):
        self.type_airplane = 'Грузовой'
        return self.type_airplane

    def __str__(self):
        return f'Boeing737'


s = Schedule()  # Создание экземпляра класса
b = Flight()  # Создание экземпляра класса
s.show_scoreboard()  # Вывод информации на экран

while True:  # Запуск программы
    print('1 – вывести расписание, 2 – ввести опоздание 2, 3 - купить билет, 0 - выход из системы')
    admin = input('Введите команду: ')

    if admin == '1':
        s.show_scoreboard()  # Вывод информации на экран
    elif admin == '2':
        admin_index = input('Введите номер задержанного рейса: ')
        admin_time = int(input('Введите величину опоздания в минутах: '))
        b.delay(admin_index, admin_time)  # Вызываем метод задержки рейса
        print('Информация записана')
    elif admin == '3':
        admin_ticket = input('Введите страну куда хотите полететь: ')
        time_lst = s.show_time(admin_ticket)  # Вызов метода покупки билетов
        if len(time_lst) != 0:
            user_time_country = input('На какое время вам удобно? - ')
            if user_time_country in time_lst:
                airplane, airplane_2 = Airbus319, Boeing737
                air = rnd.choice([airplane, airplane_2])
                print(f'Билет в страну {admin_ticket} зарегистрирован, время вылета {user_time_country}. '
                      f'Вы полетите на {air.__name__}')
            else:
                print('Извините на данное время билетов нет')
    elif admin == '0':
        print('Произошел выход из системы')
        break
    else:
        print('Неверная команда, повторите попытку!')
