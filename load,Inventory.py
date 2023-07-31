from typing import Any
from GameAssets import*


pygame.init()
ScreenSize = (800, 680 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()

class Inventory:
    def __init__(self, room, screen) -> None:
        self.screen = screen
        self.room = room
        
        self.contents = []
        self.slots = {'slot0': (5, 195), 'slot1': (55, 195), 'slot2': (110, 195), 'slot3': (165, 195), 'slot4': (220, 195),
                      'slot5': (5, 250), 'slot6': (55, 250), 'slot7': (110, 250), 'slot8': (165, 250), 'slot9': (220, 250),
                      'slots10': (5, 300), 'slot11': (55, 300), 'slots12': (110, 300), 'slots13': (165, 300), 'slots14': (220, 300),
                      'activeItem': (197, 135)}
        self.buttons = []

        self.image = pygame.transform.rotozoom(pygame.image.load('pictures/inventar.png').convert_alpha(), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = (300, 200)

        # Add items to self.contents
        i = Weapon("pictures/Sword1.png", 
                   "Sword", "Dangerous",
                   1, 200, 23, 23,
                   [Image("pictures/Sword1.png")], 
                   [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                   [Image("pictures/Sword1.png")],
                   [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                   [Image("pictures/Sword1.png")],
                   [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")])

        it2 = Weapon("pictures/FlameSword1.png", 
                     "pictures/FlameSword", "careful: hot", 
                     2, 200, 150, 150, 
                     [Image("pictures/FlameSword1.png")],
                     [Image("pictures/FlameSword1.png"), Image("pictures/FlameSword2.png"), Image("pictures/FlameSword3.png")])

        self.contents.append(i)
        self.contents.append(it2)

        # Create buttons for each item in self.contents
        for x, Sprite in enumerate(self.contents):
            pic = pygame.transform.scale(Sprite.image, (45, 50))
            slot = 'slot' + str(x)
            w = self.slots[slot]
            button = Button(w[0] + self.rect.topleft[0], w[1] + self.rect.topleft[1], pic, 1)
            self.buttons.append(button)

        self.slot_positions = [self.slots['slot0'], self.slots['slot1'], self.slots['slot2'],
                               self.slots['slot3'], self.slots['slot4'], self.slots['slot5'],
                               self.slots['slot6'], self.slots['slot7'], self.slots['slot8'],
                               self.slots['slot9'], self.slots['slots10'], self.slots['slot11'],
                               self.slots['slots12'], self.slots['slots13'], self.slots['slots14']]
        self.dragged_item = None

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        pos = pygame.mouse.get_pos()  # Move this line inside the draw method

        for button in self.buttons:
            if button.rect.collidepoint(pos) and button.clicked:
                # Set the currently dragged item to the button being clicked
                self.dragged_item = button

            # Call the draw method of each button to update their display
            button.draw(self.screen)

        if self.dragged_item:
            # If an item is being dragged, update its position based on mouse movement
            self.dragged_item.rect.center = pos

        if not pygame.mouse.get_pressed()[0] and self.dragged_item:
            # If the left mouse button is released, snap the dragged item to the nearest slot
            min_distance = float('inf')
            nearest_slot = None

            for slot_pos in self.slot_positions:
                distance = pygame.math.Vector2(slot_pos).distance_to(self.dragged_item.rect.center)
                if distance < min_distance:
                    min_distance = distance
                    nearest_slot = slot_pos

            # Snap the dragged item to the center of the nearest slot
            self.dragged_item.rect.center = nearest_slot
            self.dragged_item = None



inv = Inventory(1,screen)

i = Weapon("pictures/Sword1.png", 
                "Sword", "Dangery",
                1, 200, 23, 23,
                [Image("pictures/Sword1.png")], 
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")])

it2 = Weapon("pictures/FlameSword1.png", 
                    "pictures/FlameSword", "carefull: hot", 
                    2, 200, 150, 150, 
                    [Image("pictures/FlameSword1.png")],
                    [Image("pictures/FlameSword1.png"), Image("pictures/FlameSword2.png"), Image("pictures/FlameSword3.png")])

inv.contents.append(i)
inv.contents.append(it2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    inv.draw()
     
    pos = pygame.mouse.get_pos()

    print(pos)
    pygame.display.update()
    clock.tick(60)