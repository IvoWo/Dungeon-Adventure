import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.mixer.music.load('Sounds/Running_Sound.wav')
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slider Demo")
        
class Slider:

    def __init__(self, width, height, radius, x, y) -> None:

        self.rect = pygame.Rect(x,y,width,height)
        self.radius = radius
        self.slider_pos = x + width
        self.clicked = False
        self.prev_mouse_state = False


    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()[0] == 1

        if mouse_state:
            self.clicked = True
            #checks if mouse is on slider
            if self.slider_pos - self.radius <= pos[0] <= self.slider_pos + self.radius:
                #checks if the mouse is on the slider-bar
                if self.rect.topleft[0] <= pos[0] <= self.rect.bottomright[0]:
                    if self.rect.topleft[1] <= pos[1] <= self.rect.bottomright[1]:
                        self.slider_pos = pos[0]

            
            elif self.rect.topleft[0] <= pos[0] <= self.rect.bottomright[0]:
                if self.rect.topleft[1] <= pos[1] <= self.rect.bottomright[1]:
                    self.slider_pos = pos[0]

        if not mouse_state and self.prev_mouse_state:
            if self.clicked:
                action = True
            self.clicked = False  

        screen.fill("Black")
        pygame.draw.rect(screen, ("Grey"), self.rect)
        pygame.draw.circle(screen, "Blue", (self.slider_pos, (self.rect.topleft[0] + self.rect.height/2)), self.radius)
        pygame.display.flip()

        self.prev_mouse_state = mouse_state

        return action

    def value(self):

        value = (self.slider_pos - self.rect.topleft[0]) / (self.rect.topright[0] - self.rect.topleft[0])
        return value

running = True

slider = Slider(200, 20, 15, 200, 200)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if slider.draw(screen):
        volume = slider.value()
        pygame.mixer.music.set_volume(volume)