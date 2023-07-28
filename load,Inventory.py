from typing import Any
from GameAssets import*


pygame.init()
ScreenSize = (800, 680 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()

class Inventory:
    def __init__(self) -> None:
        
        self.contents = []
        self.slots = {'slot0' : (305,395), 'slot1': (355,395)}

    def draw(self,screen):
        image = pygame.transform.rotozoom(pygame.image.load('pictures/inventar.png').convert_alpha(), 0, 1)
        rect = image.get_rect()
        rect.topleft = (300,200)
        screen.blit(image, (rect.x, rect.y))

        x = 0
        for Sprite in self.contents:
            pic = pygame.transform.scale(Sprite.image,(45,50))
            slot = ('slot' + str(x))
            w = self.slots[slot]
            disp = Button(w[0], w[1], pic, 1)
            disp.draw(screen)
            x +=1


            
            

        

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

it2 = FlameSword = Weapon("pictures/FlameSword1.png", 
                    "pictures/FlameSword", "carefull: hot", 
                    2, 200, 150, 150, 
                    [Image("pictures/FlameSword1.png")],
                    [Image("pictures/FlameSword1.png"), Image("pictures/FlameSword2.png"), Image("pictures/FlameSword3.png")])

inv.contents.append(i)
inv.contents.append(it2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    inv.draw(screen)
     
    pos = pygame.mouse.get_pos()

    print(pos)
    pygame.display.update()
    clock.tick(60)










