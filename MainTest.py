from sys import exit
from GameAssets import *
from UI import *
from pygame import mixer

pygame.init()

#generates a screen
SCREENWIDTH, SCREENHIGHT = 600,600
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
pygame.display.set_caption('Dungeon-Adventure')

FPS = 60

#Is used to start the Music when the game is opened
#mixer.music.load('Sounds/Main_Menu_Sound.wav')
#mixer.music.play(-1)
#Music_Playing = 'M'

gameStateManager = gameStateManager('start')
states = {'start':Gamestate_start(screen, gameStateManager), 'run':Gamestate_run(screen, gameStateManager)}

while True:
    game = Game(gameStateManager, states, FPS)
    game.run()