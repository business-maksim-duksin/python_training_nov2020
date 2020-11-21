from threading import Thread
from itertools import count

a = count(0, 1)


def function(arg):
    global a
    for _ in range(arg):
        next(a)


def main():
    threads = []
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)  # ???


main()
