from random import random
from time import sleep


## STATE 0
def state0():
    print("State 0")
    sleep(0.5)
    if random() > 0.5:
        return state1
    else:
        return state2


## STATE 1
def state1():
    print("State 1")
    sleep(0.5)
    if random() > 0.5:
        return state1
    else:
        return state2


## STATE 2
def state2():
    print("State 2")
    sleep(0.5)
    if random() > 0.5:
        return state0
    else:
        return None


## MAIN
if __name__ == "__main__":
    state = state0
    while state:
        state = state()
    print("Done")
