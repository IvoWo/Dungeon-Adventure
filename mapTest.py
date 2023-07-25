from GameAssets import *

pygame.init()

screen = pygame.display.set_mode((600,600))
screen.fill("Black")
FPS = 60
clock = pygame.time.Clock()

Room1 = Room('pictures/blackBackground.png')
image = pygame.transform.rotozoom(pygame.image.load('pictures/blackBackground.png').convert_alpha(), 0, 2)

player = pygame.sprite.GroupSingle()
player1 = Player(Room1)
player.add(player1)

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

while True:
    screen.blit(image, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                print('*')
    
    Room1.draw(screen)
    player.draw(screen)
    player.update(screen)
    #Room1.Itemlist.draw(screen)
    Room1.Itemlist.update()
    pygame.display.update()
    clock.tick(FPS)