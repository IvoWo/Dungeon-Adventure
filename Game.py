from sys import exit
from GameAssets import *
from UI import *
from pygame import mixer


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

mixer.music.load('Sounds/Main_Menu_Sound.wav')
mixer.music.play(-1)
Music_Playing = 'M'

Continue_img = pygame.image.load('pictures/Continue_Button.png').convert_alpha()
Quit_img = pygame.image.load('pictures/Quit_Button.png').convert_alpha()
Options_img = pygame.image.load('pictures/Options_Button.png').convert_alpha()

Start_img = pygame.image.load('pictures/Start_Button.png').convert_alpha()
Main_img = pygame.image.load('pictures/Main_Button.png').convert_alpha()

# load background image
background_surf = pygame.transform.rotozoom(pygame.image.load('pictures/map.jpg').convert_alpha(), 0, 0.5)
background_Main = pygame.transform.rotozoom(pygame.image.load('pictures/Main_Menu.png').convert_alpha(), 0, 6)

continue_button = Button.Button(250, 145, Continue_img, 1.5)
quit_button = Button.Button(278, 240,Quit_img, 1.5)
options_button = Button.Button(254, 190, Options_img, 1.5)
start_button = Button.Button(268, 145, Start_img, 1.5)
main_button = Button.Button(278, 240, Main_img, 1.5)

def drawText(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# instanciate Objects

Room1 = Room('pictures/blackBackground.png')


player = pygame.sprite.GroupSingle()
player1 = Player(Room1)
player.add(player1)


Sword = Weapon("Sword", "Dangery", "pictures/Sword1.png", 10, 0.3)
Sword.addAnimationImages("pictures/Sword1.png", "pictures/Sword2.png", "pictures/Sword3.png")
Room1.Itemlist.add(Sword)

# game loop
run = True
while run:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                PauseGame = not PauseGame

    if MainMenu:

        if(Music_Playing != 'M'):
            mixer.music.load('Sounds/Main_Menu_Sound.wav')
            mixer.music.play(-1)
            Music_Playing = 'M'

        screen.blit(background_Main, (0,0))
        if quit_button.draw(screen):
                 run = False

        if start_button.draw(screen):
                PauseGame = False
                MainMenu = False

        if options_button.draw(screen):
            print('not yet implemented')

        pygame.display.update()


    else:
        if PauseGame:

            if continue_button.draw(screen):
                PauseGame = not PauseGame

            if options_button.draw(screen):
                print('not yet implemented')

            if main_button.draw(screen):
                MainMenu = True

        else:   
            if(Music_Playing != 'r'):
                mixer.music.load('Sounds/Running_Sound.wav')
                mixer.music.play(-1)
                Music_Playing = 'r'
            screen.blit(background_surf, (0,0))
            # animate groups
            player.draw(screen)
            player.update(screen)
            Room1.Itemlist.draw(screen)
            Room1.Itemlist.update()

    pygame.display.update()
    clock.tick(60)