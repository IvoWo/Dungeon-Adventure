import pygame
from sys import exit


pygame.init()
ScreenSize = (600, 600 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()
PauseGame = False


# instanciate groups
herbivoreGroup = pygame.sprite.Group()

# load background image
# background_surf = pygame.transform.rotozoom(pygame.image.load('Pictures\ground.jpg').convert_alpha(), 0, 2)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            PauseGame = not PauseGame

    if PauseGame:
        pass
    else:
        

        # screen.blit(background_surf, (0,0))
        # animate groups
        herbivoreGroup.draw(screen)
        herbivoreGroup.update()

    pygame.display.update()
    clock.tick(60)

