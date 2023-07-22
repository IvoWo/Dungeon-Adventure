import pygame

RightFace = {"Default": pygame.image.load("pictures/SideWalk1.png"), 
            "Walking": [pygame.image.load("pictures/SideWalk1.png"), pygame.image.load("pictures/SideWalk2.png")] }

def turnFace(Face):
    turnFace = {}
    for key in Face:
        if hasattr(Face[key], '__iter__'):
            ImageList = []
            for Image in Face[key]:
                ImageList.append(pygame.transform.flip(Image, True, False))
            turnFace[key] = ImageList
            print(key, ImageList)
        else:
            turnFace[key] = pygame.transform.flip(Face[key], True, False)
            print(key, turnFace[key])

LeftFace = turnFace(RightFace)
print(LeftFace)