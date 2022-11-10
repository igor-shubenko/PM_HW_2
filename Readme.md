### Поліморфізм

Поліморфізм у Python - це можливість взаємодіяти з різними об'єктами єдиним образом. Приклади поліморфізму:
1. Поліморфизм оператора "+", можливий через реалізацію метода \__add\__ у різних класах.

```
1 + 2   #3
[1, 2] + [3, 4]     #[1, 2, 3, 4]
'abc' + 'def'   #'abcdef'
```

2. Поліморфізм функції len(), можливий через реалізацію метода \__len\__ у різних класах.

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

Терпер подивимось до колекції \__dict\__ екземпляру класу:

```
print(device.__dict__)

#{'name': 'Base device', '_protected_namе': 'Base device', '_Device__private_name': 'Base device'}              
```

Бачимо, що атрибут __private_name записаний як _Device__private_name. Якщо звернутися до нього таким чино, то помилки
не буде. До методу можна звертатись таким же чином.

```
print(device._Device__private_name)         #Base device
device._Device__private_func()              #I am private
```

Підсумковуючи, можна сказати що до приватного атрибуту чи методу можна звернутися за правилом
***_ClassName__atributename***. Але це дуже не рекомендується, оскільки не просто так атрибут позначений як приватний.