from sys import exit
from GameAssets import *
from UI import *
from pygame import mixer

#generates a screen
SCREENWIDTH, SCREENHIGHT = 600,600
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
pygame.display.set_caption('Dungeon-Adventure')

FPS = 120

gameStateManager = gameStateManager('start')
states = {'start':Gamestate_start(screen, gameStateManager), 'run':Gamestate_run(screen, gameStateManager)}

game = Game(gameStateManager, states, FPS)

while True:
    game.run()