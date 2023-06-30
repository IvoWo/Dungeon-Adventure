from random import choice



class Player:

    Inventory = []

    def __init__(self, startRoom) -> None:
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


class Item():
    def __init__(self, Name, Description) -> None:
        self.Description = Description
        self.Name = Name
    
    def getDescription(self):
        return(self.Name + ": " + self.Description)

class Map:
    Rooms = []

    def generateMap(self):
        pass


class Room:
    # idea: Exits stores which rooms are connected to this room 
    # should propably also hold the asociated Items for the Room
    Exits = []
    Itemlist = []
    
    
    def __init__(self) -> None:
         self.generateRoom()

    def generateRoom(self):
        for i in range(4):
            self.Exits.append(choice([True, False]))


class Item():
    def __init__(self, Name, Description) -> None:
        self.Description = Description
        self.Name = Name
    
    def getDescription(self):
        return(self.Name + ": " + self.Description)
    
    def getName(self):
        return(self.Name)
    
    
    
    