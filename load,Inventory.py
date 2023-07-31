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
        self.images = []
        self.slots = {'slot0': (327, 420), 'slot1': (377, 420), 'slot2': (432, 420), 'slot3': (487, 420), 'slot4': (542, 420),
                      'slot5': (327, 475), 'slot6': (377, 475), 'slot7': (432, 475), 'slot8': (487, 475), 'slot9': (542, 475),
                      'slots10': (327, 525), 'slot11': (377, 525), 'slots12': (432, 525), 'slots13': (487, 525), 'slots14': (542, 525),
                      'weapon': (517, 360), 'potion': (347, 250), 'amulet': (347, 305), 'ofhand': (347, 360), 'helmet': (517, 250), 'armor': (517, 305)}

        self.image = pygame.transform.rotozoom(pygame.image.load('pictures/inventar.png').convert_alpha(), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.topleft = (300, 200)
        self.dragged_item = None
        

        # Create a list to store the item buttons
        self.item_buttons = []

        # Get the slot positions from the slots dictionary
        self.slot_positions = list(self.slots.values())

    def addItem(self, item):
        # Create a new button instance with the item's image, scaled to 45x50 pixels
        x, y = self.slot_positions[len(self.item_buttons)]  # Get next available slot position
        scaled_image = pygame.transform.scale(item.image, (45, 50))
        button = Button(x, y, scaled_image, 1.0)  # Scale of 1.0 to keep the original size
        # Add the button to the item_buttons list
        self.item_buttons.append(button)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        pos = pygame.mouse.get_pos()

        for button in self.item_buttons:
            if button.rect.collidepoint(pos) and button.clicked:
                self.dragged_item = button

            # Draw the button at its respective position
            button.draw(self.screen)

        if self.dragged_item:
            self.dragged_item.rect.center = pos

        if not pygame.mouse.get_pressed()[0] and self.dragged_item:
            min_distance = float('inf')
            nearest_slot = None

            for slot_pos in self.slot_positions:
                distance = pygame.math.Vector2(slot_pos).distance_to(self.dragged_item.rect.center)
                if distance < min_distance:
                    min_distance = distance
                    nearest_slot = slot_pos

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

inv.addItem(i)
inv.addItem(it2)

backimage = pygame.transform.rotozoom(pygame.image.load('pictures/blackBackground.png').convert_alpha(), 0, 2)
Room1 = Room('pictures/blackBackground.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    inv.draw()
     
    pos = pygame.mouse.get_pos()
    Room1.update(screen)
    print(pos)
    pygame.display.update()
    clock.tick(60)