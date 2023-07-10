import math   
import pygame

class Animation():

    def __init__(self,AnimationTimeInMilliseconds = 1000, ImageList = []) -> None:
        self.AnimationTimeInMilliseconds = AnimationTimeInMilliseconds
        self.ImageList = ImageList

    def startAnimation(self):
        self.StartTime = pygame.time.get_ticks()
        self.UpdateImage()

    def updateImage(self):
            if len(self.ImageList) > 0:
                MillisecondsPerImage = self.AnimationTimeInMilliseconds/len(self.ImageList)
            TimeDiff = pygame.time.get_ticks() - self.StartTime
            if TimeDiff < self.AnimationTimeInMilliseconds:
                CurrentImageNum = math.floor(TimeDiff/MillisecondsPerImage)
                image = self.ImageList[CurrentImageNum]
                return image
            else:
                self.StartTime = 0
