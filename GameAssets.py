from random import choice
from collections import defaultdict
from typing import Any
import pygame

class SpriteBaseClass(pygame.sprite.Sprite):
    def __init__(self, PictureFilePath):
        super().__init__()
        self.image = pygame.image.load(PictureFilePath).convert_alpha()
        self.rect = self.image.get_rect()



class Player(SpriteBaseClass):

    Inventory = []
    Movementspeed = 3
    health = 100

    def __init__(self, startRoom):
        super().__init__("pictures/IvoCD.png")
        self.Room = startRoom

    def enterRoom(self, newRoom):
        self.Room = newRoom
    
    def collectItem(self, Item):
        self.Inventory.append(Item)

    def inspectInventory(self):
        Itemnames = []
        for Item in self.Inventory:
            Itemnames.append(Item.getName())
        return Itemnames
    
    def inspectItem(self, name):
        for Item in self.Inventory:
            if(Item.getName(self).str.lower() == name):
                print(Item.getDescription(self))

    def takeDamage(self, amount):
        self.health -= amount
    
    def playerControll(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y += -self.Movementspeed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.Movementspeed
        if keys[pygame.K_LEFT]:
            self.rect.x += -self.Movementspeed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.Movementspeed
    
    def update(self):
        self.playerControll()



class Item(SpriteBaseClass):
    def __init__(self, Name, Description, pictureFilePath) -> None:
        super().__init__(pictureFilePath)
        self.Description = Description
        self.Name = Name
    
    def getDescription(self):
        return(self.Name + ": " + self.Description)
    
    def getName(self):
        return(self.Name)

class Map():
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
    Itemlist = []
    Enemies = []

    def __init__(self, pictureFilePath) -> None:
         super().__init__(pictureFilePath)
         self.generateRoom()

    def generateRoom(self):
        pass

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
    
class Enemy():
    """A placeholder class for enemys(for now)"""
    
    def __init__(self, Health, Speed) -> None:
        self.Health = Health
        self.Movementspeed = Speed

    def takeDamage(self, Amount):
        Health -= Amount