import random

random.seed(3)

def bla():
    c = random.randint(1, 100)
    d = random.randint(1, 100)
    print(c,d)

for i in range(5):
    bla()