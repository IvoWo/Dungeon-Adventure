from typing import Any
from GameAssets import*


pygame.init()
ScreenSize = (800, 680 )
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption('Dungeon-Adventure')
clock = pygame.time.Clock()

class InventoryItemButton:
    def __init__(self, x, y, image, scale=1.0) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.initial_pos = (x, y)  # Store the initial position of the button
        self.current_pos = (x, y)  # Store the current position of the button
        self.is_dragged = False
        self.prev_mouse_state = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()[0] == 1

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            # Check if mouse button is pressed down
            if mouse_state and not self.prev_mouse_state:
                self.is_dragged = True

            # Check if mouse button is released
            if not mouse_state and self.prev_mouse_state:
                if self.is_dragged:
                    action = True
                self.is_dragged = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        # Update previous mouse state
        self.prev_mouse_state = mouse_state

        return action
    
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
        button = InventoryItemButton(x, y, scaled_image, 1.0)  # Scale of 1.0 to keep the original size
        button.initial_pos = (x, y)
        # Add the button to the item_buttons list
        self.item_buttons.append(button)

    def deleteItem(self, Item):
        self.item_buttons.remove(Item)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        pos = pygame.mouse.get_pos()

        for button in self.item_buttons:
            if button.rect.collidepoint(pos) and button.is_dragged:
                self.dragged_item = button

            # Draw the button at its respective position
            button.draw(self.screen)

        if self.dragged_item:
            self.dragged_item.rect.center = pos

        if not pygame.mouse.get_pressed()[0] and self.dragged_item:
            if not self.rect.collidepoint((self.dragged_item.rect.center)):
                self.deleteItem(self.dragged_item)
            else:
                min_distance = float('inf')
                nearest_slot = None

                for slot_pos in self.slot_positions:
                    distance = pygame.math.Vector2(slot_pos).distance_to(self.dragged_item.rect.center)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_slot = slot_pos
                    for button in self.item_buttons:
                        if button.rect.center == nearest_slot:
                            button.rect.center = self.dragged_item.initial_pos

                self.dragged_item.rect.center = nearest_slot
                self.dragged_item.initial_pos = nearest_slot
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
    #print(pos)
    screen.blit(backimage,(0,0))
    pygame.display.update()
    clock.tick(60)