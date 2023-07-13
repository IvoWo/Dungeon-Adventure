from collections import defaultdict
import random
import pygame
import math
from random import randrange
import sys



class SpriteBaseClass(pygame.sprite.Sprite):

    class State():
        def __init__(self, MillisecondsPerImage = 0) -> None:
            self.MillisecondsPerImage = MillisecondsPerImage
            self.CurrentImageIndex = 0
            self.AnimationStartTime = 0
            
    def __init__(self, PictureFilePath : str 
                 ,Height = 16, Width = 16
                 ,RightFace : dict[State , list[str]] = {}
                 ,FrontFace : dict[State , list[str]] = {}
                 ,BackFace : dict[State , list[str]] = {}
                 ):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(PictureFilePath).convert_alpha(), (Width, Height))
        self.rect = self.image.get_rect()
        self.RightFace = self.scaleFace(self.loadFace(RightFace), Height, Width)
        self.LeftFace = self.turnFace(self.RightFace)
        self.FrontFace = self.scaleFace(self.loadFace(FrontFace), Height, Width)
        self.BackFace = self.scaleFace(self.loadFace(BackFace), Height, Width)
        self.CurrentFace = self.FrontFace
        self.CurrentState = self.State()

    def turnFace(self, Face):
        turnFace = {}
        for key in Face:
            if hasattr(Face[key], '__iter__') and not isinstance(Face[key], str):
                ImageList = []
                for Image in Face[key]:
                    ImageList.append(pygame.transform.flip(Image, True, False))
                turnFace[key] = ImageList
            else:
                turnFace[key] = pygame.transform.flip(Face[key], True, False)
        return turnFace

    def scaleFace(self, Face, Height = 16, Width = 16 ):
        turnFace = {}
        for key in Face:
            if hasattr(Face[key], '__iter__') and not isinstance(Face[key], str):
                ImageList = []
                for Image in Face[key]:
                    ImageList.append(pygame.transform.scale(Image, (Width, Height)))
                turnFace[key] = ImageList
            else:
                turnFace[key] = pygame.transform.scale(Face[key], (Width, Height))
        return turnFace
    
    def loadFace(self, Face):
        """turns a Face with Filepaths to a Face with Surfaces \n
           checks wether its a string and then turns it to a surf """
        turnFace = {}
        for key in Face:
            if hasattr(Face[key], '__iter__') and not isinstance(Face[key], str):
                ImageList = []
                for Image in Face[key]:
                    if isinstance(Image, str):
                        ImageList.append(pygame.image.load(Image).convert_alpha())
                    else:
                        ImageList.append(Image)
                turnFace[key] = ImageList
            else:
                if isinstance(Face[key], str):
                    turnFace[key] = pygame.image.load(Face[key]).convert_alpha()
                else:
                    turnFace[key] = Face[key]
        return turnFace

    def animateSelf(self):
        if self.CurrentState.AnimationStartTime == 0:
            self.CurrentState.AnimationStartTime = pygame.time.get_ticks()
        TimeDiff =  pygame.time.get_ticks() - self.CurrentState.AnimationStartTime
        if TimeDiff > self.CurrentState.MillisecondsPerImage:
            self.CurrentState.CurrentImageIndex += 1
            self.CurrentState.AnimationStartTime = 0           
        if self.CurrentState.CurrentImageIndex >= len(self.CurrentFace[self.CurrentState]) : 
            self.CurrentState.CurrentImageIndex = 0
        self.image = self.CurrentFace[self.CurrentState][self.CurrentState.CurrentImageIndex]



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
    IsWalking = False
    WalkStartTime = 0
    ActiveItemSlot = pygame.sprite.Group()
    
    def __init__(self, currentRoom):
        self.Default = self.State(MillisecondsPerImage= 5000)
        self.Walking = self.State(MillisecondsPerImage= 200)
        
        self.RightFace = {self.Default: ["pictures/SideWalk1.png"], 
                        self.Walking: ["pictures/SideWalk1.png", "pictures/SideWalk2.png"] }
        self.FrontFace = {self.Default:["pictures/IvoCD.png"], 
                        self.Walking: ["pictures/IvoCD.png"] }
        self.BackFace = {self.Default: ["pictures/BackFace1.png"], 
                        self.Walking: ["pictures/BackFace1.png"]}
        
        super().__init__("pictures/IvoCD.png", 50, 50, self.RightFace, self.FrontFace, self.BackFace)
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
            self.CurrentFace = self.BackFace
            self.CurrentState = self.Walking
        if keys[pygame.K_DOWN]:
            self.rect.y += self.Movementspeed
            self.CurrentFace = self.FrontFace
            self.CurrentState = self.Walking
        if keys[pygame.K_LEFT]:
            self.rect.x += -self.Movementspeed
            self.CurrentFace = self.LeftFace
            self.CurrentState = self.Walking
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.Movementspeed
            self.CurrentFace = self.RightFace
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
            self.ActiveItemSlot.update()
            self.ActiveItemSlot.draw(Screen)

class Item(SpriteBaseClass):
    def __init__(self, 
                 PictureFilePath: str, 
                 Name : str = "",
                 Description: str = "",
                 Height=16, Width=16, 
                 RightFace: dict[SpriteBaseClass.State, list[str]] = {}, 
                 FrontFace: dict[SpriteBaseClass.State, list[str]] = {}, 
                 BackFace: dict[SpriteBaseClass.State, list[str]] = {}):
        self.Name = Name
        self.Description = Description
        super().__init__(PictureFilePath, Height, Width, RightFace, FrontFace, BackFace)
    
    def getDescription(self):
        return(self.Name + ": " + self.Description)
    
    def useItem(self):
        pass

class Weapon(Item):
    
    # the hurtBoxGroup contains the sprites of the attack animation
    # for example bullest, checking bullet collision can then be done be checking againt the whole group
    HurtboxGroup = pygame.sprite.Group()
    AttackStarttime = 0
    Default = SpriteBaseClass.State()
    Attacking = SpriteBaseClass.State(200)

    def __init__(self, 
                 PictureFilePath: str, 
                 Name: str = "", 
                 Description: str = "", 
                 Damage: int = 1,
                 AttackDurationInMilliseconds = 500, 
                 Height=16, Width=16, 
                 RightFaceDefaultImages: list[str] = [],
                 RightFaceAttackingImages: list[str] = [], 
                 FrontFaceDefaultImages: list[str] = [],
                 FrontFaceAttackingImages: list[str] = [], 
                 BackFaceDefaultImages: list[str] = [],
                 BackFaceAttackingImages: list[str] = []):
        self.Damage = Damage
        self.AttackDurationInMilliseconds = AttackDurationInMilliseconds
        self.Default = self.State()
        self.Attacking = self.State(200)
        RightFace = {self.Default: RightFaceDefaultImages,
                     self.Attacking: RightFaceAttackingImages}
        FrontFace = {self.Default: FrontFaceDefaultImages,
                     self.Attacking: FrontFaceAttackingImages}
        BackFace = {self.Default: BackFaceDefaultImages,
                     self.Attacking: BackFaceAttackingImages}

        super().__init__(PictureFilePath, Name, Description, Height, Width, RightFace, FrontFace, BackFace)
        # it is extremly Important to set the state the a know State before self.animate is called
        self.CurrentState = self.Default

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

    def draw(self, surface):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()
    
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

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
        if self.quit_button.draw(self.screen):
            pygame.quit()
            sys.exit()
            
        if self.start_button.draw(self.screen):
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

            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()
            self.clock.tick(self.FPS)

class Gamestate_run:
    def __init__(self, display, gameStateManager): 
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('blue')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('start')