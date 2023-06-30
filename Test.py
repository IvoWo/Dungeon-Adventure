from Game import *

StartRoom = Room()
Knife = Item("Knife", "usefull to cut stuff")
Pan = Item("Pan", "usefull to cook stuff")
Player1 = Player(Room)
Player1.collectItem(Knife)
Player1.collectItem(Pan)
print(Player1.inspectInventory())