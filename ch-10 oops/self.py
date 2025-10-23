class takken:
    health="nunu"
    stamina=500
    power=800
    def avarage(self):
        print(self.health*self.stamina*self.power)
    @staticmethod
    def sum():
        print("are you crazy")
kisu=takken()
kisu.health=500000
print(kisu.health , kisu.stamina , kisu.power)
nisu=takken()
nisu.health=1000
print(nisu.health)
nisu.avarage()
nisu.sum()