from collections import defaultdict
import random
import pygame
import math
from random import randrange
import sys


class Point():
    def __init__(self, X:int = 0, Y:int = 0, Name:str = "") -> None:
        self.Coordinates = (X, Y)
        self.Name = Name

class Image():
    def __init__(self,PictureFilePath : str = "", PointsInPicture: list[Point] = []) -> None:
        self.PictureFilePath = PictureFilePath
        self.PointsInPicture = PointsInPicture
        self.Image = pygame.image.load(self.PictureFilePath).convert_alpha()

class State():
    def __init__(self, MillisecondsPerImage = 0) -> None:
        self.MillisecondsPerImage = MillisecondsPerImage
        self.AnimationStartTime = 0
        self.CurrentImageIndex = 0

class Face():
    def __init__(self, Name = "", StatesWithImages: dict[State, list[Image]] = {}) -> None:
        self.Name = Name
        self.StatesWithImages = StatesWithImages
    
    def getFlippedFace(self, Name : str):
        FlippedFace = {}
        for k, v in self.StatesWithImages.items():
            Images = []
            for I in v:
                INew = Image(I.PictureFilePath)
                INew.Image = pygame.transform.flip(INew.Image, True, False)
                Images.append(INew)
            FlippedFace[k] = Images
        return Face(Name, FlippedFace)
    
    def scaleFace(self, Width, Height):
        for v in self.StatesWithImages.values():
            for Image in v:
                Image.Image = pygame.transform.scale(Image.Image, (Width, Height))

class SpriteBaseClass(pygame.sprite.Sprite):
    def __init__(self, PictureFilepath: str,
                 Width = 16, Height = 16,
                 RightFace = Face(), LeftFace= Face(), 
                 FrontFace = Face(), BackFace = Face(), 
                 CurrentFace = Face(), CurrentState = State()):
        super().__init__()
        self.Right = RightFace
        self.Right.scaleFace(Width, Height)
        self.Left = LeftFace
        self.Left.scaleFace(Width, Height)
        self.Front = FrontFace
        self.Front.scaleFace(Width, Height)
        self.Back = BackFace
        self.Back.scaleFace(Width, Height)
        self.CurrentFace = CurrentFace
        self.CurrentFace.scaleFace(Width, Height)
        self.CurrentState = CurrentState
        self.image = pygame.transform.scale(pygame.image.load(PictureFilepath).convert_alpha(), (Width, Height))
        self.rect = self.image.get_rect()
        
    def animateSelf(self):
        """it is important to set currentState und currentFace \n
            to actual values of your class-object before using \n
            this method"""
        if self.CurrentState.AnimationStartTime == 0:
            self.CurrentState.AnimationStartTime = pygame.time.get_ticks()
        TimeDiff =  pygame.time.get_ticks() - self.CurrentState.AnimationStartTime
        if TimeDiff > self.CurrentState.MillisecondsPerImage:
            self.CurrentState.CurrentImageIndex += 1
            self.CurrentState.AnimationStartTime = 0
        if self.CurrentState.CurrentImageIndex >= len(self.CurrentFace.StatesWithImages[self.CurrentState]):
            self.CurrentState.CurrentImageIndex = 0
        if self.CurrentFace.StatesWithImages[self.CurrentState]:
            self.image = self.CurrentFace.StatesWithImages[self.CurrentState][self.CurrentState.CurrentImageIndex].Image

    def turn(self, Direction: str):
        """a Direction is a string \n
        Directions are: right, left, front, back"""
        for Face in [x for x in [self.Back, self.Front, self.Right, self.Left] if x.Name == Direction]:
            self.CurrentFace = Face
                

class Obstacle(SpriteBaseClass):
    def __init__(self, image, x, y) -> None:
        super().__init__(image)
        self.rect.center = (x,y)
        
class Rock(Obstacle):
    def __init__(self, x, y):
        super().__init__("pictures/rock.png", x, y)

class Player(SpriteBaseClass):
    
    Inventory = []
    Movementspeed = 3
    Health = 100
    ActiveItemSlot = pygame.sprite.Group()
    
    def __init__(self, currentRoom):

        # States
        self.Default = State(MillisecondsPerImage= 5000)
        self.Walking = State(MillisecondsPerImage= 200)
        # Images
        RightDefaultImages = [Image("pictures/SideWalk1.png")]
        RightWalkingImages = [Image("pictures/SideWalk1.png"), Image("pictures/SideWalk2.png")]
        FrontDefaultImages = [Image("pictures/IvoCD.png")]
        FrontWalkingImages = [Image("pictures/IvoCD.png")]
        BackDefaultImages = [Image("pictures/BackFace1.png")]
        BackWalkingImages = [Image("pictures/BackFace1.png")]

        #Faces
        RightFace = Face("right",{self.Default: RightDefaultImages, self.Walking: RightWalkingImages})
        LeftFace = RightFace.getFlippedFace("left")
        FrontFace = Face("front", {self.Default: FrontDefaultImages, self.Walking: FrontWalkingImages})
        BackFace = Face("back",{self.Default: BackDefaultImages, self.Walking: BackWalkingImages})


        super().__init__("pictures/IvoCD.png",32, 32 ,RightFace, LeftFace, FrontFace, BackFace, FrontFace, self.Default)
        self.Room = currentRoom

    def update(self, Screen):
        self.playerControll()
        self.animateSelf()
        self.animateActiveItem(Screen)
        self.stayOnScreen()


    def enterRoom(self, newRoom):
        self.Room = newRoom
    
    def collectItem(self):
        Item =  pygame.sprite.spritecollideany(self, self.Room.Itemlist)
        if Item:
            if not self.ActiveItemSlot:
                self.Room.Itemlist.remove(Item)
                self.ActiveItemSlot.add(Item)
                
    def inspectInventory(self):
        Itemnames = []
        for Item in self.Inventory:
            Itemnames.append(Item.Name)
        for Item in self.ActiveItemSlot:
            Itemnames.append(Item.Name)
        return Itemnames
    
    def inspectItem(self, name):
        for Item in self.Inventory:
            if(Item.Name.str.lower() == name):
                print(Item.getDescription(self))

    def takeDamage(self, amount):
        self.health -= amount
    
    def playerControll(self):
        self.CurrentState = self.Default
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y += -self.Movementspeed
            self.CurrentFace = self.Back
            self.CurrentState = self.Walking
        if keys[pygame.K_DOWN]:
            self.rect.y += self.Movementspeed
            self.CurrentFace = self.Front
            self.CurrentState = self.Walking
        if keys[pygame.K_LEFT]:
            self.rect.x += -self.Movementspeed
            self.CurrentFace = self.Left
            self.CurrentState = self.Walking
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.Movementspeed
            self.CurrentFace = self.Right
            self.CurrentState = self.Walking
        if keys[pygame.K_e]:
            print(self.inspectInventory())
        if keys[pygame.K_q]:
            self.collectItem()
        if keys[pygame.K_a]:
            for Item in self.ActiveItemSlot:
                Item.useItem()

    def stayOnScreen(self):
        '''prevents from leaving the screen'''
        if self.rect.right > 600:
            print(' X Border right')
            self.rect.right = 600
        if self.rect.left < 0:
            print('X Border left')
            self.rect.left = 0
        if self.rect.bottom > 600:
            print(' Y Border Bottom')
            self.rect.bottom = 600
        if self.rect.top < 0:
            print('Y Border Top')
            self.rect.top = 0
    
    def animateActiveItem(self, Screen):
        if self.ActiveItemSlot:
            for item in self.ActiveItemSlot:
                item.rect.center = self.rect.center
                item.turn(self.CurrentFace.Name)
            self.ActiveItemSlot.update()
            self.ActiveItemSlot.draw(Screen)

class Item(SpriteBaseClass):
    def __init__(self, PictureFilepath: str, 
                 Name :str, Description : str, 
                 Width=16, Height=16, 
                 RightFace=Face(), LeftFace=Face, 
                 FrontFace=Face(), BackFace=Face(), 
                 CurrentFace=Face(), CurrentState=State()):
        super().__init__(PictureFilepath, 
                         Width, Height, 
                         RightFace, LeftFace, 
                         FrontFace, BackFace, 
                         CurrentFace, CurrentState)
        self.Name = Name
        self.Description = Description

    def getDescription(self):
        return(self.Name + ": " + self.Description)
    
    def useItem(self):
        pass

class Weapon(Item):
    
    # the hurtBoxGroup contains the sprites of the attack animation
    # for example bullest, checking bullet collision can then be done be checking againt the whole group
    HurtboxGroup = pygame.sprite.Group()
    AttackStarttime = 0

    def __init__(self, 
                 PictureFilePath: str, 
                 Name: str = "", 
                 Description: str = "", 
                 Damage: int = 1,
                 AttackDurationInMilliseconds = 500, 
                 Width=16, Height=16, 
                 RightFaceDefaultImages: list[Image] = [],
                 RightFaceAttackingImages: list[Image] = [], 
                 FrontFaceDefaultImages: list[Image] = [],
                 FrontFaceAttackingImages: list[Image] = [], 
                 BackFaceDefaultImages: list[Image] = [],
                 BackFaceAttackingImages: list[Image] = []):
        self.Damage = Damage
        self.AttackDurationInMilliseconds = AttackDurationInMilliseconds
        self.Default = State()
        self.Attacking = State(self.AttackDurationInMilliseconds/len(RightFaceAttackingImages))
        RightFace = {self.Default: RightFaceDefaultImages,
                     self.Attacking: RightFaceAttackingImages}
        FrontFace = {self.Default: FrontFaceDefaultImages,
                     self.Attacking: FrontFaceAttackingImages}
        BackFace = {self.Default: BackFaceDefaultImages,
                     self.Attacking: BackFaceAttackingImages}
        RightFace = Face("right", RightFace)
        LeftFace = RightFace.getFlippedFace("left")
        FrontFace = Face("front", FrontFace)
        BackFace = Face("back", BackFace)
        super().__init__(PictureFilePath, 
                         Name, Description, 
                         Width, Height,
                         RightFace, LeftFace, FrontFace, BackFace, RightFace, self.Attacking)

    def update(self):
        self.animateSelf()
        TimeDiff = pygame.time.get_ticks() - self.AttackStarttime
        if TimeDiff > self.AttackDurationInMilliseconds:
            self.CurrentState = self.Default

    def useItem(self):
        if not self.CurrentState == self.Attacking: 
            self.AttackStarttime = pygame.time.get_ticks()
            self.CurrentState = self.Attacking

class Map():
    #Map ist für die allgemeine Map - Verbindung der Räume
    #finde zwei Klasse für ein und dasselbe nicth gut
    """ Graph data structure, undirected \n
        Connections look like: [(Room1, Room2), (Room2, Room3)]"""

    def __init__(self, connections):
        self._graph = defaultdict(set)
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for Room1, Room2 in connections:
            self.add(Room1, Room2)

    def add(self, Room1, Room2):
        """ Add connection between Room1 and Room2 """

        self._graph[Room1].add(Room2)
        self._graph[Room2].add(Room1)

    def remove(self, Room):
        """ Remove all references to Room """

        for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
            try:
                cxns.remove(Room)
            except KeyError:
                pass
        try:
            del self._graph[Room]
        except KeyError:
            pass

    def is_connected(self, Room1, Room2):
        """ Is Room1 directly connected to Room2 """

        return Room1 in self._graph and Room2 in self._graph[Room1]

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
    
class Room(SpriteBaseClass):
    # idea: Exits stores which rooms are connected to this room 
    # should propably also hold the asociated Items for the Room
    
    Exits = []
    Itemlist = pygame.sprite.Group()
    Enemies = pygame.sprite.Group()
    Obstacles = pygame.sprite.Group()

    def __init__(self, PictureFilePath) -> None:
         super().__init__(PictureFilePath)
         self.generateRoom()

    def draw(self, SCREEN):
        self.Itemlist.draw(SCREEN)
        self.Enemies.draw(SCREEN)
        self.Obstacles.draw(SCREEN)

    def generateRoom(self):
        pass

#noch nicht ingame
class Itemholder():
    """A base class for storing item \n
       Might be for a backpack, the players Inventory and the like"""
    Itemlist = []
    
    def __init__(self, MaxCapacity: int) -> None:
         self.MaxCapacity = MaxCapacity
    
    def addToItemlist(self, Item: Item):
        if len(self.Itemlist) < self.MaxCapacity:
            self.Itemlist.append(Item)
        else:
            return "is already full"
    
    def removeFromItemList(self, Item):
        self.Itemlist.remove(Item)

#noch nicht ingame
class Enemy(SpriteBaseClass):
    """A placeholder class for enemys(for now)"""
    
    def __init__(self, Health, Speed, image, scale, PictureFilePath) -> None:
        super().__init__(PictureFilePath)
        self.Health = Health
        self.Movementspeed = Speed
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()


    def takeDamage(self, Amount):
        Health -= Amount
    
#Button class
class Button():
    def __init__(self, x, y, image, scale) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.prev_mouse_state = False

    def draw(self, surface):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()[0] == 1

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            # Check if mouse button is pressed down
            if mouse_state and not self.prev_mouse_state:
                self.clicked = True

         # Check if mouse button is released
        if not mouse_state and self.prev_mouse_state:
            if self.clicked:
                action = True
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

         # Update previous mouse state
        self.prev_mouse_state = mouse_state

        return action
    
class gameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

class Gamestate_start:

    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager

        self.image = pygame.transform.rotozoom(pygame.image.load('pictures/Main_Menu.png').convert_alpha(), 0, 6)
        self.Start_img = pygame.image.load('pictures/Start_Button.png').convert_alpha()
        self.Options_img = pygame.image.load('pictures/Options_Button.png').convert_alpha()
        self.Quit_img = pygame.image.load('pictures/Quit_Button.png').convert_alpha()

        self.quit_button = Button(278, 240, self.Quit_img, 1.5)
        self.options_button = Button(254, 190, self.Options_img, 1.5)
        self.start_button = Button(268, 145, self.Start_img, 1.5)

    def run(self):
        self.screen.blit(self.image, (0,0))

        if(not pygame.mixer.music.get_busy()):
            pygame.mixer.music.load('Sounds/Main_Menu_Sound.wav')
            pygame.mixer.music.play(-1)

        if self.quit_button.draw(self.screen):
            pygame.quit()
            sys.exit()
            
        if self.start_button.draw(self.screen):
            pygame.mixer.music.stop()
            self.gameStateManager.set_state('run')

        if self.options_button.draw(self.screen):
            print('not yet implemented')

class Game:  
    def __init__(self, gameStateManager, states, FPS):
        self.clock = pygame.time.Clock()

        self.gameStateManager = gameStateManager
        self.FPS = FPS
        self.states = states

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Handle Escape key press
                        if self.gameStateManager.get_state() == 'run':
                            self.states['run'].PauseGame =True

            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()
            self.clock.tick(self.FPS)

class Gamestate_run:
    def __init__(self, screen, gameStateManager): 
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.PauseGame = False

        self.image = pygame.transform.rotozoom(pygame.image.load('pictures/blackBackground.png').convert_alpha(), 0, 2)
        self.Continue_img = pygame.image.load('pictures/Continue_Button.png').convert_alpha()
        self.Options_img = pygame.image.load('pictures/Options_Button.png').convert_alpha()
        self.Main_img = pygame.image.load('pictures/Main_Button.png').convert_alpha()

        self.continue_button = Button(250, 145, self.Continue_img, 1.5)
        self.options_button = Button(254, 190, self.Options_img, 1.5)
        self.main_button = Button(278, 240, self.Main_img, 1.5)

    def run(self):
        self.screen.blit(self.image, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.PauseGame = not self.PauseGame

        if(self.PauseGame == False):

            pygame.mixer.music.unpause()

            if(not pygame.mixer.music.get_busy()):
                pygame.mixer.music.load('Sounds/Running_Sound.wav')
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.pause()

            if self.continue_button.draw(self.screen):
                self.PauseGame = not self.PauseGame

            if self.options_button.draw(self.screen):
                print('not yet implemented')

            if self.main_button.draw(self.screen):
                pygame.mixer.music.stop()
                self.PauseGame = False
                self.gameStateManager.set_state('start')