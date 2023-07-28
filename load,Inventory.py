from typing import Any
from GameAssets import*

pygame.init()

Screen = pygame.display.set_mode((600,600))

class Inventory:
    def __init__(self) -> None:
        
        self.contents = []
        

    def draw(self,screen):

        for Item in self.contents:
            print(Item.Name)

inv = Inventory()

i = Weapon("pictures/Sword1.png", 
                "Sword", "Dangery",
                1, 200, 23, 23,
                [Image("pictures/Sword1.png")], 
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")])


inv.contents.append(i)

inv.draw(Screen)










