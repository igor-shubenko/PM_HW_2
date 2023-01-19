from threading import Thread
from time import sleep
import threading

# Тут у нас запускается сначала функция func в треде, выполняется, завершается и
# дальше выполняется func2 тоже в треде. Причем интересно, func2 вызывает func которая не в треде
# и каждый раз ждет, когда та выполнит цикл.

def func(n = 1):
	while n < 5:
		print(f"Hello World, a am func, call - {n}")
		print()
		sleep(1)
		n += 1

trd = Thread(target=func)

trd.start() #starting thread
# trd.join()   # что-то типо точки останова, если закоментить, запустится сразу и второй тред

Flag = 1

def func2(args):
	while Flag:
		print("I'm func 2 calling func")
		func()
		print()
	print("Dead")

trd2 = Thread(target=func2, args=(5, ))
trd2.start()
print(a) # интересный баг, если раскоментить то треды не завершаются
print("Thread count:", threading.active_count())
print("Thread enumerate:", threading.enumerate())
print("Is alive:?", trd2.is_alive())
sleep(5)
Flag = False



trd2.join()
trd.join()
