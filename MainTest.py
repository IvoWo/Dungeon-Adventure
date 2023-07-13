from sys import exit
from GameAssets import *
from UI import *
from pygame import mixer

SCREENWIDTH, SCREENHIGHT = 600,600
FPS = 60

class Game:  
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREENWIDTH,SCREENHIGHT))
        self.clock = pygame.time.Clock()

        self.gameStateManager = gameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)

        self.states = {'start':self.start, 'level':self.level}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()
            self.clock.tick(FPS)
    
class Level:
    def __init__(self, display, gameStateManager): 
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('blue')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('start')

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display

        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('red')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('level')

class gameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state
        
    
if __name__ == '__main__':
    game = Game()
    game.run()