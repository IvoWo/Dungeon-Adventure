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
        self.slots = {'slot0': (5,195), 'slot1': (55,195), 'slot2': (110,195), 'slot3': (165,195), 'slot4': (220,195),
                      'slot5': (5,250), 'slot6': (55,250), 'slot7': (110,250), 'slot8': (165,250), 'slot9': (220,250),
                      'slots10': (5,300), 'slot11': (55,300), 'slots12': (110,300), 'slots13': (165,300), 'slots14': (220,300)}

    def draw(self,screen):
        image = pygame.transform.rotozoom(pygame.image.load('pictures/inventar.png').convert_alpha(), 0, 1)
        rect = image.get_rect()
        rect.topleft = (300,200)
        screen.blit(image, (rect.x, rect.y))
        buttons = []

        x = 0
        for Sprite in self.contents:
            pic = pygame.transform.scale(Sprite.image,(45,50))
            slot = ('slot' + str(x))
            w = self.slots[slot]
            button = Button(w[0] + rect.topleft[0], w[1] + rect.topleft[1], pic, 1)
            buttons.append(button)
            #screen.blit(pic, (w[0] + rect.topleft[0], w[1] + rect.topleft[1]))
            #buttons.append(pic)
            x +=1
        
        for Button in buttons:
            if Button.draw():
                print('*')

            
            

        

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

it2 = Weapon("pictures/FlameSword1.png", 
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

    #print(pos)
    pygame.display.update()
    clock.tick(60)










