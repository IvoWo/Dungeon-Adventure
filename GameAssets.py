from collections import defaultdict
import pygame
import math

class SpriteBaseClass(pygame.sprite.Sprite):
    def __init__(self, PictureFilePath : str):
        super().__init__()
        self.image = pygame.image.load(PictureFilePath).convert_alpha()
        self.rect = self.image.get_rect()

def turnFace(Face):
    turnFace = {}
    for key in Face:
        if hasattr(Face[key], '__iter__'):
            ImageList = []
            for Image in Face[key]:
                ImageList.append(pygame.transform.flip(Image, True, False))
            turnFace[key] = ImageList
        else:
            turnFace[key] = pygame.transform.flip(Face[key], True, False)
    return turnFace




class Player(SpriteBaseClass):
    
    Inventory = []
    Movementspeed = 3
    Health = 100
    IsWalking = False
    WalkStartTime = 0
    
    def __init__(self, startRoom):
        super().__init__("pictures/IvoCD.png")
        self.Room = startRoom
        self.WalkDurationInSeconds = 1
        self.WalkDurationInMilliseconds = self.WalkDurationInSeconds * 1000
        self.MillisecondsPerImage = 1000
        self.currentImageIndex = 0
        self.RightFace = {"Default": pygame.image.load("pictures/SideWalk1.png").convert_alpha(), 
                    "Walking": [pygame.image.load("pictures/SideWalk1.png").convert_alpha(), pygame.image.load("pictures/SideWalk2.png").convert_alpha()] }
        
        self.LeftFace = turnFace(self.RightFace)
        
        self.FrontFace = {"Default": pygame.image.load("pictures/IvoCD.png").convert_alpha(), 
                    "Walking": [pygame.image.load("pictures/IvoCD.png").convert_alpha()] }
        
        self.BackFace = {"Default": pygame.image.load("pictures/BackFace1.png").convert_alpha(), 
                    "Walking": [pygame.image.load("pictures/BackFace1.png").convert_alpha()]}
        self.Facing = self.FrontFace

    def update(self):
        self.playerControll()
        self.animateWalk()
        self.stayOnScreen()


    def enterRoom(self, newRoom):
        self.Room = newRoom
    
    def collectItem(self):
        if pygame.sprite.spritecollideany(self, self.Room.Itemlist):
            self.Inventory.append(pygame.sprite.spritecollideany(self, self.Room.Itemlist))

    def inspectInventory(self):
        Itemnames = []
        for Item in self.Inventory:
            Itemnames.append(Item.Name)
        return Itemnames
    
    def inspectItem(self, name):
        for Item in self.Inventory:
            if(Item.Name.str.lower() == name):
                print(Item.getDescription(self))

    def takeDamage(self, amount):
        self.health -= amount
    
    def playerControll(self):
        self.IsWalking = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y += -self.Movementspeed
            self.Facing = self.BackFace
            self.IsWalking = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.Movementspeed
            self.Facing = self.FrontFace
            self.IsWalking = True
        if keys[pygame.K_LEFT]:
            self.rect.x += -self.Movementspeed
            self.Facing = self.LeftFace
            self.IsWalking = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.Movementspeed
            self.Facing = self.RightFace
            self.IsWalking = True
        if keys[pygame.K_e]:
            print(self.inspectInventory())
        if keys[pygame.K_q]:
            self.collectItem()

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

    def switchWalkAnimationImage(self):
        NumberOfImages = len(self.Facing["Walking"])
        if  NumberOfImages> 1:
            self.MillisecondsPerImage = self.WalkDurationInMilliseconds/NumberOfImages
        TimeDiff =  pygame.time.get_ticks() -self.WalkStartTime
        # print("msPerI:", self.MillisecondsPerImage, "TimeDiff:", TimeDiff)
        if TimeDiff > self.MillisecondsPerImage:
            self.currentImageIndex += 1
            self.WalkStartTime = pygame.time.get_ticks()
        if self.currentImageIndex > NumberOfImages-1:
            self.currentImageIndex = 0
        print("current image Index:", self.currentImageIndex)
        self.image = self.Facing["Walking"][self.currentImageIndex]

        



    def animateWalk(self):
        # print("Is Walking:", self.IsWalking)
        if not self.IsWalking:
            self.image = self.Facing["Default"]
            self.WalkStartTime = pygame.time.get_ticks()
        else:
            self.switchWalkAnimationImage()

class Item(SpriteBaseClass):
    def __init__(self, Name, Description, PictureFilePath) -> None:
        super().__init__(PictureFilePath)
        self.Description = Description
        self.Name = Name
    
    def getDescription(self):
        return(self.Name + ": " + self.Description)
    
    def useItem(self):
        pass

class Weapon(Item):
    
    # the hurtBoxGroup contains the sprites of the attack animation
    # for example bullest, checking bullet collision can then be done be checking againt the whole group
    HurtboxGroup = pygame.sprite.Group()
    # the attack Animation contains several Images in a List, that are played in a loop when attacking
    AttackAnimationImages = []
    IsAttacking = False
    AttackStartTime = 0

    def __init__(self, Name, Description, pictureFilePath, Damage: int, AttackDurationInSeconds = 0.5) -> None:
        super().__init__(Name, Description, pictureFilePath)
        self.Damage = Damage
        self.AttackDurationInSeconds = AttackDurationInSeconds
        self.AttackDurationInMilliseconds = self.AttackDurationInSeconds * 1000
        self.MillisecondsPerImage = 1000

    def update(self):
        super().useItem()
        self.startAttack()
        self.animateWeapon()

    def addAnimationImages(self, *Images):
        """pass in any amount of file location strings, seperate by comma \n
           Example: addImages("pictures/pic1.png", "pictures/pic2.png", ...) """
        for Image in Images:
            self.AttackAnimationImages.append(pygame.image.load(Image))
    
    # TO-DO: use MousePos to get the direction of the attack
    def startAttack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.IsAttacking:
            # MousePos = pygame.mouse.get_pos()
            # AttackDirection = (MousePos[0] -self.rect.centerx, MousePos[1] - self.rect.centery)
            # LenVector = math.sqrt(math.pow(AttackDirection[0],2) + math.pow(AttackDirection[1],2))
            # # normalising the vector
            # AttackDirection[0] = AttackDirection[0]/LenVector
            # AttackDirection[1] = AttackDirection[1]/LenVector
            self.IsAttacking = True

    def createHurtbox(self):
        pass

    def switchAnimationImage(self):
        if len(self.AttackAnimationImages) > 0:
            self.MillisecondsPerImage = self.AttackDurationInMilliseconds/len(self.AttackAnimationImages)
        TimeDiff = pygame.time.get_ticks() - self.AttackStartTime
        if TimeDiff < self.AttackDurationInMilliseconds:
            CurrentImageNum = math.floor(TimeDiff/self.MillisecondsPerImage)
            self.image = self.AttackAnimationImages[CurrentImageNum]
        else:
            self.IsAttacking = False
            self.AttackStartTime = 0
            self.image = self.AttackAnimationImages[0]

    def animateWeapon(self):
        if not self.IsAttacking:
            self.AttackStartTime = pygame.time.get_ticks()
        else:
            self.switchAnimationImage()

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

    def __init__(self, PictureFilePath) -> None:
         super().__init__(PictureFilePath)
         self.generateRoom()

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
class Enemy():
    """A placeholder class for enemys(for now)"""
    
    def __init__(self, Health, Speed) -> None:
        self.Health = Health
        self.Movementspeed = Speed

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