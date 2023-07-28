from collections import defaultdict
import random
from typing import Any
import pygame
import math
from random import randrange
import sys
import json

from pygame.sprite import Group


class Point():
    def __init__(self, X:int = 0, Y:int = 0, Name:str = "") -> None:
        """X and Y are the percent of topleft to bottemright \n
        100x and 100y equals bottomleft"""
        self.X = X
        self.Y = Y
        self.XPercent = X
        self.YPercent = Y
        self.Name = Name

class Image():
    def __init__(self,PictureFilePath : str = "", PointsInPicture: list[Point] = []) -> None:
        self.PictureFilePath = PictureFilePath
        self.PointsInPicture = PointsInPicture
        try: self.Image = pygame.image.load(self.PictureFilePath).convert_alpha()
        except: self.Image = pygame.Surface((16,16))


class State():
    def __init__(self, MillisecondsPerImage = 200) -> None:
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
                INew = Image(I.PictureFilePath, [Point(100/P.XPercent * P.X - P.X, P.Y, P.Name) for P in I.PointsInPicture])
                INew.Image = pygame.transform.flip(INew.Image, True, False)
                Images.append(INew)
            FlippedFace[k] = Images
        return Face(Name, FlippedFace)
    
    def scaleFace(self, Width, Height):
        """scales the points aswell, given they are initialized with the percent values, see point"""
        for v in self.StatesWithImages.values():
            for Image in v:
                Image.Image = pygame.transform.scale(Image.Image, (Width, Height))
                for Point in Image.PointsInPicture:
                    Point.X = Point.XPercent * Width/100
                    Point.Y = Point.YPercent * Height/100

class SpriteBaseClass(pygame.sprite.Sprite):

    def __init__(self, PictureFilepath: str,
                 Width = 16, Height = 16,
                 RightFace = Face(), LeftFace= Face(), 
                 FrontFace = Face(), BackFace = Face(), 
                 CurrentFace = Face(), CurrentState = State()):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(PictureFilepath).convert_alpha(), (Width, Height))
        self.rect = self.image.get_rect()

        self.Right = RightFace
        self.Left = LeftFace
        self.Front = FrontFace
        self.Back = BackFace

        self.CurrentFace = CurrentFace
        self.CurrentState = CurrentState

        self.Right.scaleFace(Width, Height)
        self.Left.scaleFace(Width, Height)
        self.Front.scaleFace(Width, Height)
        self.Back.scaleFace(Width, Height)
        # self.CurrentFace.scaleFace(Width, Height)
        
        self.CurrentImage = Image()
        self.CurrentFace = CurrentFace
        self.CurrentState = CurrentState
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


    def animateSelf(self):
        if self.CurrentState.AnimationStartTime == 0:
            self.CurrentState.AnimationStartTime = pygame.time.get_ticks()
        TimeDiff =  pygame.time.get_ticks() - self.CurrentState.AnimationStartTime
        if TimeDiff > self.CurrentState.MillisecondsPerImage:
            self.CurrentState.CurrentImageIndex += 1
            self.CurrentState.AnimationStartTime = 0
        if self.CurrentState in self.CurrentFace.StatesWithImages.keys():          
            if self.CurrentState.CurrentImageIndex >= len(self.CurrentFace.StatesWithImages[self.CurrentState]) : 
                self.CurrentState.CurrentImageIndex = 0
            if self.CurrentFace.StatesWithImages[self.CurrentState]:
                self.CurrentImage = self.CurrentFace.StatesWithImages[self.CurrentState][self.CurrentState.CurrentImageIndex]
                self.image = self.CurrentImage.Image

    def turn(self, Direction: str):
        """a Direction is a string \n
        Directions are: right, left, front, back"""
        for Face in [x for x in [self.Back, self.Front, self.Right, self.Left] if x.Name == Direction]:
            self.CurrentFace = Face

class ObstacleBaseClass(SpriteBaseClass):
    def keepOut(self, ListofGroups : list[pygame.sprite.Group]):
        for Group in ListofGroups:
            for Sprite in pygame.sprite.spritecollide(self, Group, False):
                XDiff = Sprite.rect.centerx - self.rect.centerx
                YDiff = Sprite.rect.centery - self.rect.centery
                if abs(XDiff) >= abs(YDiff):
                    Sprite.rect.move(XDiff, 0)
                else:
                    Sprite.rect.move(0, YDiff)
                    

class Obstacle(SpriteBaseClass):
    def __init__(self, image, x, y) -> None:
        super().__init__(image)
        self.rect.center = (x,y)
        
class Rock(Obstacle):
    def __init__(self, x, y):
        super().__init__("pictures/rock.png", x, y)

class LivingBeing(SpriteBaseClass):
    def __init__(self, PictureFilepath: str, 
                 Width=16, Height=16, 
                 RightFace=Face(), LeftFace=Face(), 
                 FrontFace=Face(), BackFace=Face(), 
                 CurrentFace=Face(), CurrentState=State(), 
                 Health = 10, DeathAnimationImages : list[Image]= []):
        super().__init__(PictureFilepath, 
                         Width, Height, 
                         RightFace, LeftFace, 
                         FrontFace, BackFace, 
                         CurrentFace, CurrentState)
        self.Health = Health
        self.PreDeathState = State()
        self.DeathAnimation = Face("front", {self.PreDeathState: DeathAnimationImages})
        self.DeathAnimationStartTime = 0
        self.DeathAnimation.scaleFace(Width, Height)

    def live(self):
        """call at the end of update to make sure death is not overridden by other states"""
        if self.Health <= 0 and not self.CurrentState == self.PreDeathState:
            self.CurrentState = self.PreDeathState
            self.DeathAnimationStartTime = pygame.time.get_ticks()
            self.CurrentFace = self.DeathAnimation
        if self.CurrentState == self.PreDeathState:
            TimeDiff = pygame.time.get_ticks() - self.DeathAnimationStartTime
            TimeOfAnimation = len(self.DeathAnimation.StatesWithImages[self.PreDeathState]) * self.PreDeathState.MillisecondsPerImage
            if TimeDiff >= TimeOfAnimation:
                print("was killed")
                self.kill() 
            

class Player(LivingBeing):
    
    Inventory = pygame.sprite.Group()
    Movementspeed = 3
    ActiveItemSlot = pygame.sprite.Group()
    
    
    def __init__(self, currentRoom):
        # Player Animation 
        # States
        self.Default = State(MillisecondsPerImage= 5000)
        self.Walking = State(MillisecondsPerImage= 200)
        # Images
        RightDefaultImages = [Image("pictures/SideWalk1.png", [Point(67,53, "Hand")])]
        RightWalkingImages = [Image("pictures/SideWalk1.png", [Point(67,53, "Hand")]), Image("pictures/SideWalk2.png", [Point(61, 60, "Hand")])]
        FrontDefaultImages = [Image("pictures/IvoCD.png", [Point(71, 86, "Hand")])]
        FrontWalkingImages = [Image("pictures/IvoCD.png", [Point(71, 86, "Hand")])]
        BackDefaultImages = [Image("pictures/BackFace1.png", [Point(73, 74, "Hand")])]
        BackWalkingImages = [Image("pictures/BackFace1.png", [Point(73, 74, "Hand")])]

        #Faces
        RightFace = Face("right",{self.Default: RightDefaultImages, self.Walking: RightWalkingImages})
        FrontFace = Face("front", {self.Default: FrontDefaultImages, self.Walking: FrontWalkingImages})
        BackFace = Face("back",{self.Default: BackDefaultImages, self.Walking: BackWalkingImages})
        LeftFace = RightFace.getFlippedFace("left")
        super().__init__("pictures/IvoCD.png",50, 50 ,RightFace, LeftFace, FrontFace, BackFace, FrontFace, self.Default)
        self.Room = currentRoom

        # TO DO
        #Arm Animation Images
        # RightWalking = []
        # RightDefault = []
        # RightBoxing = []
        # RightArmSwing = []

        # LeftWalking = []
        # LeftDefault = []
        # LeftBoxing = []
        # LeftArmSwing = []

        # FrontWalking = []
        # FrontDefault = []
        # FrontBoxing = []
        # FrontArmSwing = []

        # BackWalking = []
        # BackDefault = []
        # BackBoxing = []
        # BackArmSwing = []

        # Default =  State()
        # Walking = State(200)
        # Boxing = State(100)
        # Swing = State(100)

        # ArmRightFace = Face("right", {})


        # self.Arm = SpriteBaseClass("pictures/FlameSword1.png")
        # self.Arm.Default =  Default
        # self.Arm.Walking = Walking
        # self.Arm.Boxing = Boxing
        # self.Arm.Swing = Swing

    def update(self, Screen):
        self.animateSelf()
        self.animateActiveItem(Screen)
        if not self.CurrentState == self.PreDeathState:
            self.playerControll()
        self.stayOnScreen()
        self.checkCollision()
        self.live()

    def checkCollision(self):
        obstacle = pygame.sprite.spritecollideany(self, self.Room.Obstacles)
        if obstacle: 
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                print ('hit von unten')
                self.rect.y -= -self.Movementspeed
            if key[pygame.K_DOWN]:
                print('hit von oben')
                self.rect.y -= self.Movementspeed
            if key[pygame.K_LEFT]:
                print('hit von rechts')
                self.rect.x -= -self.Movementspeed
            if key[pygame.K_RIGHT]:
                print('hit von links')
                self.rect.x -= self.Movementspeed

    def enterRoom(self, newRoom):
        self.Room = newRoom
    
    def collectItem(self):
        Item =  pygame.sprite.spritecollideany(self, self.Room.Itemlist)
        if Item:
            if not self.ActiveItemSlot:
                self.Room.Itemlist.remove(Item)
                self.ActiveItemSlot.add(Item)
                self.Inventory.add(Item)
            else:
                self.Room.Itemlist.remove(Item)
                self.Inventory.add(Item)

    def dropItem(self):
        if self.ActiveItemSlot.sprites():
            self.Inventory.remove(self.ActiveItemSlot.sprites())
            self.Room.Itemlist.add(self.ActiveItemSlot.sprites()[0])
            self.ActiveItemSlot.remove(self.ActiveItemSlot.sprites()[0])
            
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
            # self.inspectInventory()
            pass
        if keys[pygame.K_q]:
            self.collectItem()
        if keys[pygame.K_d]:
            self.dropItem()
        if keys[pygame.K_a]:
            for Item in self.ActiveItemSlot:
                Item.useItem()

    def stayOnScreen(self):
        '''prevents from leaving the screen'''
        if self.rect.right > 600:
            self.rect.right = 600
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        if self.rect.top < 0:
            self.rect.top = 0
    
    def animateActiveItem(self, Screen):
        if self.ActiveItemSlot:
            for item in self.ActiveItemSlot:
                for p in [p for p in self.CurrentImage.PointsInPicture if p.Name == "Hand"]:
                    for p2 in [p for p in item.CurrentImage.PointsInPicture if p.Name == "Handle"]:
                        item.rect.topleft = (self.rect.topleft[0] + p.X, self.rect.topleft[1] + p.Y)
                        item.rect.topleft = (item.rect.topleft[0] - p2.X,item.rect.topleft[1] - p2.Y )

                item.turn(self.CurrentFace.Name)
            self.ActiveItemSlot.update(self.Room.Enemies)
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
    def getItemPictureFilePath(self):
        return self.PictureFilepath
    
    def useItem(self):
        pass

class Weapon(Item):
    
    # the hurtBoxGroup contains the sprites of the attack animation
    # for example bullest, checking bullet collision can then be done be checking againt the whole group
    HurtboxGroup = pygame.sprite.Group()
    Default = State()
    Attacking = State(200)

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
        self.AttackStarttime = 0
        self.Default = State()
        self.Attacking = State(self.AttackDurationInMilliseconds/len(RightFaceAttackingImages))
        RightDict = {self.Default: RightFaceDefaultImages,
                     self.Attacking: RightFaceAttackingImages}
        FrontDict = {self.Default: FrontFaceDefaultImages,
                     self.Attacking: FrontFaceAttackingImages}
        BackDict = {self.Default: BackFaceDefaultImages,
                     self.Attacking: BackFaceAttackingImages}
        RightFace = Face("right", RightDict)
        LeftFace = RightFace.getFlippedFace("left")
        FrontFace = Face("front", FrontDict)
        BackFace = Face("back", BackDict)
        super().__init__(PictureFilePath, 
                         Name, Description, 
                         Width, Height,
                         RightFace, LeftFace, FrontFace, BackFace, RightFace, self.Default)

    def update(self, Enemies: pygame.sprite.Group()):
        # attack might get started by useItem
        self.animateSelf()
        self.dealDamage(Enemies)
        # ending the attack if attack duration is over
        if self.CurrentState == self.Attacking:
            TimeDiff = pygame.time.get_ticks() - self.AttackStarttime
            if TimeDiff > self.AttackDurationInMilliseconds:
                self.CurrentState = self.Default
                # clearing to list of already hit enemies
                self.CurrentlyHitEnemies.clear()

    def useItem(self):
        if not self.CurrentState == self.Attacking: 
            self.AttackStarttime = pygame.time.get_ticks()
            self.CurrentState = self.Attacking

    CurrentlyHitEnemies = []
    def dealDamage(self, Enemies: pygame.sprite.Group):
        # can only do damage if is attacking
        if self.CurrentState == self.Attacking:
            HitEnemies = pygame.sprite.spritecollide(self, Enemies, False)
            # removing already hit enemies in this attack sequence to deal damage only once
            for Enemy1 in self.CurrentlyHitEnemies:
                if Enemy1 in HitEnemies:
                    HitEnemies.remove(Enemy1)
            # dealing damage to remaining Enemies
            for Enemy2 in HitEnemies:
                Enemy2.Health -= self.Damage
            # adding already damaged enemies to list of excluded enemies
            for Enemy3 in HitEnemies:
                self.CurrentlyHitEnemies.append(Enemy3)


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
    Player = pygame.sprite.Group()

    def __init__(self, PictureFilePath) -> None:
         super().__init__(PictureFilePath)
         self.generateRoom()

    def update(self, SCREEN):
        self.Itemlist.update(self.Enemies)
        self.Player.update(SCREEN)
        self.Enemies.update()
        self.Obstacles.update()
        self.Itemlist.draw(SCREEN)
        self.Enemies.draw(SCREEN)
        self.Obstacles.draw(SCREEN)
        self.Player.draw(SCREEN)

    def generateRoom(self):
        pass

class Enemy(LivingBeing):
    def __init__(self, PictureFilepath: str, 
                 CurrentRoom : Room,
                 Width=16, Height=16, 
                 Health = 10, Movementspeed = 2,
                 RightFace=Face(), LeftFace=Face(), 
                 FrontFace=Face(), BackFace=Face(), 
                 CurrentFace=Face(), CurrentState=State(),
                 DeathAnimationImages: list[Image] = []):
        super().__init__(PictureFilepath, 
                         Width, Height, 
                         RightFace, LeftFace, 
                         FrontFace, BackFace, 
                         CurrentFace, CurrentState, 
                         Health,DeathAnimationImages)
                
        self.Room = CurrentRoom
        self.Movementspeed = Movementspeed

    def update(self):
        self.animateSelf()
        if not self.CurrentState == self.PreDeathState:
            self.chasePlayer()
        self.live()
    
    def chasePlayer(self):
        DirectionToPlayer = (0, 0)
        DistanceToPlayer = 0
        for Player in self.Room.Player:
            Direction = (Player.rect.center[0] - self.rect.center[0], Player.rect.center[1]- self.rect.center[1])
            Length =math.sqrt(Direction[0] ** 2 + Direction[1] ** 2)
            if Length >= DistanceToPlayer:
                DirectionToPlayer = Direction
                DistanceToPlayer = Length
        Frac = DistanceToPlayer/self.Movementspeed
        if Frac > 0:
            XSpeed = DirectionToPlayer[0]/Frac
            YSpeed = DirectionToPlayer[1]/Frac
            self.rect.x += XSpeed
            self.rect.y += YSpeed

    
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
            self.gameStateManager.set_state('options')

class Game:  
    def __init__(self, gameStateManager, states, FPS):
        self.clock = pygame.time.Clock()

        pygame.init()
        self.gameStateManager = gameStateManager
        self.FPS = FPS
        self.states = states
        self.data = {'volume': float}
        self.load = True

        try:
            with open('save/options.txt') as score_file:
                self.data = json.load(score_file)
        except:
            self.load = False

        if self.load:
            pygame.mixer.music.set_volume(self.data['volume'])

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
        self.options = False

        self.image = pygame.transform.rotozoom(pygame.image.load('pictures/blackBackground.png').convert_alpha(), 0, 2)
        self.Continue_img = pygame.image.load('pictures/Continue_Button.png').convert_alpha()
        self.Options_img = pygame.image.load('pictures/Options_Button.png').convert_alpha()
        self.Main_img = pygame.image.load('pictures/Main_Button.png').convert_alpha()

        self.continue_button = Button(250, 145, self.Continue_img, 1.5)
        self.options_button = Button(254, 190, self.Options_img, 1.5)
        self.main_button = Button(278, 240, self.Main_img, 1.5)

        self.options_slider = Slider(200, 20, 15, 200, 200)

        #das folgende soll über laden gelößt werden
        self.Room1 = Room('pictures/blackBackground.png')

        self.player = pygame.sprite.GroupSingle()
        self.player1 = Player(self.Room1)
        self.player.add(self.player1)


        self.Sword = Weapon("pictures/Sword1.png", 
                "Sword", "Dangery",
                1, 200, 23, 23,
                [Image("pictures/Sword1.png")], 
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")],
                [Image("pictures/Sword1.png")],
                [Image("pictures/Sword1.png"), Image("pictures/Sword2.png"), Image("pictures/Sword3.png")])

        self.FlameSword = Weapon("pictures/FlameSword1.png", 
                    "pictures/FlameSword", "carefull: hot", 
                    2, 200, 150, 150, 
                    [Image("pictures/FlameSword1.png")],
                    [Image("pictures/FlameSword1.png"), Image("pictures/FlameSword2.png"), Image("pictures/FlameSword3.png")])
        self.FlameSword.rect.center = (10, 50)

        self.Room1.Itemlist.add(self.Sword, self.FlameSword)

        self.rock1 = Rock(450, 450)
        self.Room1.Obstacles.add(self.rock1)
        self.rock2 = Rock(150, 450)
        self.Room1.Obstacles.add(self.rock2)

        print('height rock1:' + str(self.rock1.rect.height))
        print('width rock1:' + str(self.rock1.rect.width))
        print('heigt player:' + str(self.player1.rect.height))
        print('width player:' + str(self.player1.rect.width))

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

            self.Room1.draw(self.screen)
            self.player.draw(self.screen)
            self.player.update(self.screen)
            #Room1.Itemlist.draw(screen)
            self.Room1.Itemlist.update()

        else:
            if (self.options == False):
                pygame.mixer.music.pause()

                if self.continue_button.draw(self.screen):
                    self.PauseGame = not self.PauseGame

                if self.options_button.draw(self.screen):
                    self.options = True

                if self.main_button.draw(self.screen):
                    pygame.mixer.music.stop()
                    self.PauseGame = False
                    self.gameStateManager.set_state('start')

            else:
                if self.options_slider.draw(self.screen):
                    pygame.mixer.music.set_volume(self.options_slider.value())

                if self.continue_button.draw(self.screen):
                    self.options = False


class Gamestate_options:

    def __init__(self, screen, gameStateManager) -> None:
        self.screen = screen
        self.gameStateManager = gameStateManager 
        self.data = {'volume': float}

        try:
            with open('saves/options.txt') as score_file:
                self.data = json.load(score_file)
        except:
            self.data['volume'] = 1.0

        self.image = pygame.transform.rotozoom(pygame.image.load('pictures/Main_Menu.png').convert_alpha(), 0, 6)
        self.Continue_img = pygame.image.load('pictures/Continue_Button.png').convert_alpha()
        
        self.continue_button = Button(200, 500, self.Continue_img, 1.5)

        self.sound_slider = Slider(200, 20, 15, 200, 200)
        self.sound_slider.setSliderPosition(self.data['volume'])

    def run(self):
        self.screen.blit(self.image, (0,0))

        if self.continue_button.draw(self.screen):
            with open('save/options.txt','w') as score_file:
                json.dump(self.data, score_file)
            self.gameStateManager.set_state('start')
            

        if self.sound_slider.draw(self.screen):
            pygame.mixer.music.set_volume(self.sound_slider.value())
            self.data['volume'] = pygame.mixer.music.get_volume()

        

class Slider:

    def __init__(self, width, height, radius, x, y) -> None:

        self.rect = pygame.Rect(x,y,width,height)
        self.radius = radius
        self.slider_pos = x + width
        self.clicked = False
        self.prev_mouse_state = False

    def setSliderPosition(self, x:float):
        self.slider_pos = (x * (self.rect.topright[0] - self.rect.topleft[0]) + self.rect.topleft[0])

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()[0] == 1

        if mouse_state:
            self.clicked = True
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

        pygame.draw.rect(screen, "Grey", self.rect)
        pygame.draw.circle(screen, "Black", (self.slider_pos, (self.rect.topleft[0] + self.rect.height/2)), self.radius)

        if action:
            pygame.display.flip()

        self.prev_mouse_state = mouse_state

        return action

    def value(self):

        value = (self.slider_pos - self.rect.topleft[0]) / (self.rect.topright[0] - self.rect.topleft[0])
        return value