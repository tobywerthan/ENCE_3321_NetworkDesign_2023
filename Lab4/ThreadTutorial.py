import threading
from time import sleep

def myThread(id):
    
    n = 0

    while n < 5:
        print("Thread " + str(id) + ": " + str(n))
        
        sleep(1)
        n += 1
    print("\n")

if __name__ == '__main__':

    id_1 = 1
    id_2 = 2

    task1 = threading.Thread(target=myThread, args=(id_1,))
    task1.setDaemon(True)

    task2 = threading.Thread(target=myThread, args=(id_2,))
    task2.setDaemon(True)

    task1.start()
    task2.start()

    task1.join()
    task2.join()

    print("Threads done.")