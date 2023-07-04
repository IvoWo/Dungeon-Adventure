from sys import exit
from GameAssets import *


pygame.init()
ScreenSize = (600, 600 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()
PauseGame = False

#define Fonts
font = pygame.font.SysFont("arialblack", 40)

#define colors
TEXT_COL = (255, 255, 255)

def drawText(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

Start_img = pygame.image.load('pictures/Start_Button.jpg').convert_alpha()
start_button = Button(50, 240, Start_img, 0.1)

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
while True:

    #wenn der Startbutton gedrückt wird mach was
    if start_button.draw(screen):
        PauseGame = not PauseGame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            PauseGame = not PauseGame

    if PauseGame:
        drawText("press Space to continue", font, TEXT_COL, 50, 250)
        pass
    else:
        
        screen.blit(background_surf, (0,0))
        # animate groups
        player.draw(screen)
        player.update()

    pygame.display.update()
    clock.tick(60)