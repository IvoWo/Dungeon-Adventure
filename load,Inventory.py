import json
import pickle
from GameAssets import*

pygame.init()
screen = pygame.display.set_mode((600,600))

class pr:
    def __init__(self) -> None:
        pass

class test:
    def __init__(self, name, testzahl, testbild, pr) -> None:
        self.name = name
        self.testzahl = testzahl
        self.testbild = testbild
        self.pr = pr

teste = Weapon("pictures/Sword1.png", 
                "Sword", "Dangery",
                1, 200, 23, 23,
                [Image("pictures/Sword1.png")], 
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")])


with open('save/test.txt','wb') as score_file:
    pickle.dump(teste.__dict__, score_file)




