from sys import exit
from GameAssets import *


pygame.init()
ScreenSize = (600, 600 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()
PauseGame = False
MainMenu = False

#define Fonts
font = pygame.font.SysFont("arialblack", 40)

#define colors
TEXT_COL = (255, 255, 255)
#drawText("press Space to continue", font, TEXT_COL, 50, 250)

Continue_img = pygame.image.load('pictures/Continue_Button.png').convert_alpha()
Quit_img = pygame.image.load('pictures/Quit_Button.png').convert_alpha()
Options_img = pygame.image.load('pictures/Options_Button.png').convert_alpha()
continue_button = Button(200, 140, Continue_img, 1.5)
quit_button = Button(228, 290,Quit_img, 1.5)
options_button = Button(207, 190, Options_img, 1.5)

def drawText(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# instanciate groups
#Groups
player = pygame.sprite.GroupSingle()
player1 = Player("Startraum")
player.add(player1)
test = Item('Testname', 'Testbeschreibung', 'pictures/blackBackground.png')
player1.collectItem(test)
# load background image
background_surf = pygame.transform.rotozoom(pygame.image.load('pictures/blackBackground.png').convert_alpha(), 0, 2)

# game loop
run = True
while run:
    if MainMenu:
        pass
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                PauseGame = not PauseGame

        if PauseGame:
            if continue_button.draw(screen):
                PauseGame = not PauseGame
            if options_button.draw(screen):
                pass
            if quit_button.draw(screen):
                run = False
                pass
        else:
        
            screen.blit(background_surf, (0,0))
            # animate groups
            player.draw(screen)
            player.update()

        pygame.display.update()
        clock.tick(60)