from sys import exit
from GameAssets import *
from UI import *
from pygame import mixer

pygame.init()
SCREENWIDTH, SCREENHIGHT = 600,600
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
FPS = 60
gameStateManager = gameStateManager('start')

states ={'start':Gamestate_start(screen, gameStateManager), 'level':Gamestate_run(screen, gameStateManager)}

while True:
    game = Game(gameStateManager, states, FPS)
    game.run