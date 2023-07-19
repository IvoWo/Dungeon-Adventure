from sys import exit
from GameAssets import *
from UI import *


pygame.init()
ScreenSize = (600, 600 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()

# load background image
background_surf = pygame.transform.rotozoom(pygame.image.load('pictures/blackBackground.png').convert_alpha(), 0, 2)
background_Main = pygame.transform.rotozoom(pygame.image.load('pictures/Main_Menu.png').convert_alpha(), 0, 6)


Room1 = Room('pictures/blackBackground.png')
playerGroup = pygame.sprite.GroupSingle()
player1 = Player(Room1)
playerGroup.add(player1)

Sword = Weapon("pictures/Sword1.png", 
                "Sword", "Dangery",
                1, 200, 23, 23,
                [Image("pictures/Sword1.png")], 
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")])

FlameSword = Weapon("pictures/FlameSword1.png", 
                    "pictures/FlameSword", "carefull: hot", 
                    2, 200, 150, 150, 
                    [Image("pictures/FlameSword1.png")],
                    [Image("pictures/FlameSword1.png"), Image("pictures/FlameSword2.png"), Image("pictures/FlameSword3.png")])
FlameSword.rect.center = (10, 50)

Room1.Itemlist.add(Sword, FlameSword)


# game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_surf, (0,0))
    playerGroup.draw(screen)
    playerGroup.update(screen)
    Room1.Itemlist.draw(screen)
    Room1.Itemlist.update()

    pygame.display.update()
    clock.tick(60)