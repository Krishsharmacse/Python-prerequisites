class takken:
    health="knaksu"
    stamina=500
    power=800
    def __init__(self):
        print("i am creating an object")
kisu=takken()
kisu.health=500000
print(kisu.health , kisu.stamina , kisu.power)
nisu=takken()
nisu.health=1000
print(nisu.health)