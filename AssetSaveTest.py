from sys import exit
from GameAssets import *
from UI import *
import json

pygame.init()

SCREENWIDTH, SCREENHIGHT = 600,600
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
pygame.display.set_caption('Dungeon-Adventure')

Room1 = Room('pictures/blackBackground.png')

Sword = Weapon("pictures/Sword1.png",
                "Sword", "Dangery",
                1, 1000, 16, 16,
                ["pictures/Sword1.png"],
                ["pictures/Sword1.png", "pictures/Sword2.png", "pictures/Sword3.png"],
                ["pictures/Sword1.png"],
                ["pictures/Sword1.png", "pictures/Sword2.png", "pictures/Sword3.png"],
                ["pictures/Sword1.png"],
                ["pictures/Sword1.png", "pictures/Sword2.png", "pictures/Sword3.png"])
Room1.Itemlist.add(Sword)

rock1 = Rock(450, 450)
Room1.Obstacles.add(rock1)

with open('clicker_score.txt','w') as score_file:
                json.dump(Room1.__dict__, score_file)