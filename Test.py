from Game import *

StartRoom = Room()
Knife = Item("Knife", "usefull to cut stuff")
Player1 = Player(Room)
Player1.collectItem(Knife)
print(Player1.inspectInventory())