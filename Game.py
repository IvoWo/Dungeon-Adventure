from sys import exit
from GameAssets import *
from UI import *


pygame.init()
ScreenSize = (600, 600 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()
PauseGame = False
MainMenu = True

#define Fonts
font = pygame.font.SysFont("arialblack", 40)
#define colors
TEXT_COL = (255, 255, 255)
#drawText("press Space to continue", font, TEXT_COL, 50, 250)

Continue_img = pygame.image.load('pictures/Continue_Button.png').convert_alpha()
Quit_img = pygame.image.load('pictures/Quit_Button.png').convert_alpha()
Options_img = pygame.image.load('pictures/Options_Button.png').convert_alpha()

Start_img = pygame.image.load('pictures/Start_Button.png').convert_alpha()
Main_img = pygame.image.load('pictures/Main_Button.png').convert_alpha()

continue_button = Button.Button(200, 170, Continue_img, 1.5)
quit_button = Button.Button(228, 310,Quit_img, 1.5)
options_button = Button.Button(207, 190, Options_img, 1.5)
start_button = Button.Button(228, 130, Start_img, 1.5)
main_button = Button.Button(200, 290, Main_img, 1.5)

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
background_Main = pygame.transform.rotozoom(pygame.image.load('pictures/Main_Menu.png').convert_alpha(), 0, 6)

Sword = Weapon("Sword", "Dangery", "pictures/Sword1.png", 10, 0.3)
Sword.addAnimationImages("pictures/Sword1.png", "pictures/Sword2.png", "pictures/Sword3.png")
SwordGroup = pygame.sprite.Group()
SwordGroup.add(Sword)

# game loop
run = True
while run:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                PauseGame = not PauseGame

    if MainMenu:
        screen.blit(background_Main, (0,0))
        if quit_button.draw(screen):
                 run = False

        if start_button.draw(screen):
                MainMenu = False

        if options_button.draw(screen):
            print('not yet implemented')

        #pygame.display.update()


    else:
        if PauseGame:
            if continue_button.draw(screen):
                PauseGame = not PauseGame

            if options_button.draw(screen):
                print('not yet implemented')

            if main_button.draw(screen):
                MainMenu = True

        else:   
            screen.blit(background_surf, (0,0))
            # animate groups
            player.draw(screen)
            player.update()
            SwordGroup.draw(screen)
            SwordGroup.update(player1.rect.center)

    pygame.display.update()
    clock.tick(60)