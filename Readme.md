###Поліморфізм

Поліморфізм - це можливість взаємодіяти з різними об'єктами єдиним образом. Приклади поліморфізму:
1. Поліморфизм оператора "+", можливий через реалізацію метода __add__ у різних класах.

```
1 + 2   #3
[1, 2] + [3, 4]     #[1, 2, 3, 4]
'abc' + 'def'   #'abcdef'
```

2. Поліморфізм функції len(), можливий через реалізацію метода __len__ у різних класах.

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


room_conditioner = Conditioner('Samsung')   #Samsung status: ON
home_music_center = MusicCenter('Sony')     #Sony status: ON

room_conditioner.turn_on()                  #Samsung: target_temperature - +21 C, mode - standart
home_music_center.turn_on()                 #Sony: Playing My hits on 30% volume

room_conditioner.get_info()                 #Samsung: target_temperature - +21 C, mode - standart
home_music_center.get_info()                #Sony: Playing My hits on 30% volume

room_conditioner.turn_of()                  #Samsung status: OF
home_music_center.turn_of()                 #Sony status: OF



```

Поліморфізм у даному прикладі - це методи *turn_on()*, *turn_off()*, *get_info()*. *turn_on()* та *turn_off()* наслідуються від базового класу, 
тож у є доступним і у дочерніх класах. *get_info()* визначений окремо у кожному класі, але оскільки має однакову сигнатуру - 
може бути викликаний для інстансу кожного з них.
Тож справедливим буде сказати, що **поліморфізм реалізуєтся через методи, які мають однакову сигнатуру**.