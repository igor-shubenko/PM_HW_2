## Опис програми

Web application, створений за допомогою FastApi, реалізує Api-interface для роботи з файлом через HTTP протокол.
Програма дозволяє зчитувати записи з файлу за ідентификатором або усі одразу, створювати нові записи, оновлювати існуючі, видаляти
записи за ідентифікатором або усі одразу.
Програма потребує встановлених бібліотек _fastapi_ та _uvicorn_. Усі залежності вказані у _requirements.txt_.

Програма очикує, що робота буде виконуватися з файлом **'data.jsonl'**, яки знаходиться у тій самій директорії. Якщо це не так,
треба у файлі main.py у одинадцятому(або дванадцятому) рядку змінити шлях до файлу у параметрах створення екземпляру класу. 

Одним із варіантів запуску програми є введення команди в терміналі з директорії з файлами:
> python main.py

Запуститься локальний сервер, доступний за адресою ***http://127.0.0.1:8765***

### Програма має два варіанти роботи

**Варіан перший**

Унікальним ідентифікатором запису комбінацію значень полів 'name'+'time_created',
наприклад _Thomas1665070563_.
Оскільки немає критерію обробки дублікатів, програма працює з даними у файлі "as is", 
тобто ніяк не фільтруючи існуючі дублікати, порожні поля, тощо. Але створення нових записів, якщо ідентифікатор
вже існує, не дозволено. Якщо приходить запить на оновлення, то оновлюються всі записи за вказаним ідентифікатором, при цьому зміна полів 'name' та 'time_created' не можлива.
Якщо приходить запит на видалення запису - видаляються усі записи за ідентифікатором.

Для реалізації вказаного функціоналу реалізовані наступні ендпоінти:

 - ***/get/{ind}*** - HTTP метод має бути GET. Замісь {ind} має бути унікальний ідентифікатор (наприклад _Thomas1665070563_). Якщо вказати ***all*** - будуть повернуті усі записи.
 - ***/add*** - HTTP метод має бути POST. Очикуються дані у тілі запиту у форматі JSON. Поля 'name' та 'time_created' обов'язкові.
 - ***/change/{ind}*** - HTTP метод має бути PUT. Замісь {ind} має бути унікальний ідентифікатор (наприклад _Thomas1665070563_). Очикуються дані у тілі запиту у форматі JSON. Поля 'name' та 'time_created' не обов'язкові.
 - ***/delete/{ind}*** - HTTP метод має бути DELETE. Замісь {ind} має бути унікальний ідентифікатор (наприклад _Thomas1665070563_). Якщо вказати ***all*** - будуть видалені усі записи.

**Варіант другий**

Унікальним ідентифікатором запису обирається порядковий номер рядку у файлі, починаючи з нуля. Робота з файлом проводится "as is",
тобто рядки з однаковим змістом можуть бути, але ідентификатор матимуть різний. Якщо видалити запис, рядок стає порожнім,
ідентифікатори інших записів не зміняться. Оновити дані для видаленого запису не дозволяється. Оновлювати можна усі поля крім "time_created".
Створити запис можна з будь яким набором полів, поля "name" та "time_created" обов'якзові.

Для того, щоб програма працювала за цим режимом роботи треба змінити класс, екземпляр якого створюєтся
для роботи з файлом. Для цього достатньо у файлі ***main.py*** закоментувати рядки 5 та 11, та розкоментувати 6 та 12.
При цьому методи роботи з файлом не змінюються(приклад поліморфізму). Ендпоінти ті самі, що й в першому варианті, замість **{ind}**
очикується число або **all** для відображення чи видалення усіх записів.


### Поліморфізм

Поліморфізм у Python - це можливість взаємодіяти з різними об'єктами єдиним образом. Приклади поліморфізму:
1. Поліморфизм оператора "+", можливий через реалізацію метода \_\_add\_\_ у різних класах.

```
1 + 2   #3
[1, 2] + [3, 4]     #[1, 2, 3, 4]
'abc' + 'def'   #'abcdef'
```

2. Поліморфізм функції len(), можливий через реалізацію метода \_\_len\_\_ у різних класах.

```
len('abc')    #3
len([1, 2, 3, 4])   #4
```

3. Власний приклад

```
class ElectricDevice:
    def __init__(self, name):
        self.name = name

    def turn_on(self):
        print(f"{self.name} status: ON")

    def turn_of(self):
        print(f"{self.name} status: OF")
        
    def get_info(self):
        print(self.name)


class Conditioner(ElectricDevice):
    def __init__(self, name):
        super().__init__(name)
        self.target_temperature = '+21 C'
        self.mode = 'standart'

    def get_info(self):
        print(f"{self.name}: target_temperature - {self.target_temperature}, "
            f"mode - {self.mode}")


class MusicCenter(ElectricDevice):
    def __init__(self, name):
        super().__init__(name)
        self.volume = '30%'
        self.playlist = 'My hits'

    def get_info(self):
        print(f"{self.name}: Playing {self.playlist} on {self.volume} volume")


room_conditioner = Conditioner('Samsung')   
home_music_center = MusicCenter('Sony')     

room_conditioner.turn_on()                  #Samsung status: ON
home_music_center.turn_on()                 #Sony status: ON

smart_house_devices = [room_conditioner, home_music_center]

for dev in smart_house_devices:
    def.get_info()                          #Samsung: target_temperature - +21 C, mode - standart
                                            #Sony: Playing My hits on 30% volume

room_conditioner.turn_of()                  #Samsung status: OF
home_music_center.turn_of()                 #Sony status: OF

```

Поліморфізм у даному прикладі - це методи ***turn_on()***, ***turn_off()***, ***get_info()***. ***turn_on()*** та ***turn_off()*** наслідуються від базового класу, 
тож є доступними і у дочерніх класах. ***get_info()*** перевизначений у дочерніх класах, але оскільки має однакову сигнатуру - 
може бути викликаний для інстансу кожного з них.
Тож справедливим буде сказати, що **поліморфізм реалізуєтся через методи, які мають однакову сигнатуру**.


### Доступ до приватних атрибутів класу

Чи можливий доступ до приватних атрибутів? **Так, можливий**.
Поясню на прикладі.

```
class Device:
    def __init__(self, name):
        self.name = name
        self._protected_namе = name
        self.__private_name = name

    def public_func(self):
        print("I am public")

    def _protected_func(self):
        print("I am protected")

    def __private_func(self):
        print("I am private")      
```

До простих та protected атрибутів та методів можемо звертатися за їх ім'ям.

```
device = Device('Base device')

print(device.name)                  #Base device
print(device._protected_namе)       #Base device
device.public_func()                #I am public
device._protected_func()            #I am protected

```

А от якщо звернутися таким чино до private атрибутів та методів - виникне помилка.

```
print(device.__private_name)        #AttributeError: 'Device' object has no attribute '__private_name'
device.__private_func()             #AttributeError: 'Device' object has no attribute '__private_func'
```

Терпер подивимось до колекції \_\_dict\_\_ екземпляру класу:

```
print(device.__dict__)

#{'name': 'Base device', '_protected_namе': 'Base device', '_Device__private_name': 'Base device'}              
```

Бачимо, що атрибут __private_name записаний як _Device__private_name. Якщо звернутися до нього таким чином, то помилки
не буде. До методу можна звертатись таким же чином.

```
print(device._Device__private_name)         #Base device
device._Device__private_func()              #I am private
```

Підсумковуючи, можна сказати що до приватного атрибуту чи методу можна звернутися за правилом
***_ClassName__atributename***. Але це дуже не рекомендується, оскільки не просто так атрибут позначений як приватний.