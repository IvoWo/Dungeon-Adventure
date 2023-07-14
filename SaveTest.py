import pygame, sys
import json

pygame.init()
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None,32)

red_surf = pygame.Surface([200,200])
red_surf.fill((240,80,54))
red_rect = red_surf.get_rect(center =(150,180))

blue_surf = pygame.Surface([200,200])
blue_surf.fill((0,123,194))
blue_rect = blue_surf.get_rect(center =(450, 180))

red_score_surf = game_font.render('red', True, 'Black')
red_score_rect = red_score_surf.get_rect(center = (150,320))

blue_score_surf = game_font.render('blue', True, 'Black')
blue_score_rect = blue_score_surf.get_rect(center = (450,320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((245, 255, 252))
    screen.blit(red_surf,red_rect)
    screen.blit(blue_surf, blue_rect)
    screen.blit(red_score_surf, red_score_rect)
    screen.blit(blue_score_surf, blue_score_rect)
    
    pygame.display.update()
    clock.tick(60)