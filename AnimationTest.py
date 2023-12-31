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
                1, 200, 50, 50,
                [Image("pictures/Sword1.png", [Point(19, 87, "Handle")])], 
                [Image("pictures/Sword1.png", [Point(19, 87, "Handle")]), Image("pictures/Sword2.png", [Point(20, 85, "Handle")]), Image("pictures/Sword3.png", [Point(20, 89, "Handle")])],
                 [Image("pictures/Sword1.png", [Point(19, 87, "Handle")])], 
                [Image("pictures/Sword1.png", [Point(19, 87, "Handle")]), Image("pictures/Sword2.png", [Point(20, 85, "Handle")]), Image("pictures/Sword3.png", [Point(20, 89, "Handle")])],
                 [Image("pictures/Sword1.png", [Point(19, 87, "Handle")])], 
                [Image("pictures/Sword1.png", [Point(19, 87, "Handle")]), Image("pictures/Sword2.png", [Point(20, 85, "Handle")]), Image("pictures/Sword3.png", [Point(20, 89, "Handle")])])

TestProjectile = Projectile("pictures/FlameSword1.png", 6, 1, (1, 1), 100)
FlameSword = Weapon("pictures/FlameSword1.png", 
                    "pictures/FlameSword", "carefull: hot", 
                    2,  200,  50, 50, 
                    [Image("pictures/FlameSword1.png", [Point(45, 75, "Handle")])],
                    [Image("pictures/FlameSword1.png", [Point(45, 75, "Handle")]), 
                     Image("pictures/FlameSword2.png", [Point(32, 63, "Handle")]), 
                     Image("pictures/FlameSword3.png", [Point(27, 54, "Handle")])],
                     Projectile=TestProjectile)

charmanderDeathAnimation = [Image("pictures/charmanderDeath1.png"), Image("pictures/charmanderDeath2.png"), 
                            Image("pictures/charmanderDeath3.png"), Image("pictures/charmanderDeath4.png"), 
                            Image("pictures/charmanderDeath5.png"), Image("pictures/charmanderDeath6.png")]
Glumanda = Enemy("pictures/charmander.jpg",Room1, 20, 20, 4,2,  DeathAnimationImages= charmanderDeathAnimation)



TestProjectile.rect.center = (300, 300)
FlameSword.rect.center = (100, 100)

Room1.Enemies.add(Glumanda)
Room1.Itemlist.add( Sword, FlameSword)
Room1.Player.add(player1)


# game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(' \n this mouseclick: \n')
            MousePosition = pygame.mouse.get_pos()
            for group in [playerGroup, Room1.Itemlist, Player.ActiveItemSlot]:
                    for s in [s for s in group if s.rect.collidepoint(MousePosition)]:
                        print(MousePosition[0] -s.rect.topleft[0], MousePosition[1] -s.rect.topleft[1]) 

    screen.blit(background_surf, (0,0))
    Room1.update(screen)

    pygame.display.update()
    clock.tick(60)