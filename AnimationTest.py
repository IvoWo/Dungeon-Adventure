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

Sword = Weapon("Sword", "Dangery", "pictures/Sword1.png", 10, 0.3)
Sword.addAnimationImages("pictures/Sword1.png", "pictures/Sword2.png", "pictures/Sword3.png")
Room1.Itemlist.add(Sword)

# game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_surf, (0,0))
    playerGroup.draw(screen)
    playerGroup.update()
    Room1.Itemlist.draw(screen)
    Room1.Itemlist.update()

    pygame.display.update()
    clock.tick(60)