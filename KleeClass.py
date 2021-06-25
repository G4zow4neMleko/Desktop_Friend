import pygame
import random
import math


class Klee(pygame.sprite.Sprite):
    """main character class"""

    def __init__(self, pos_x, pos_y):
        super(Klee, self).__init__()
        self.animation = pygame.image.load("./sprites/klee_idle.png")
        self.animationsDict = {"idle": [list(self.animation.subsurface(col * 64, 0, 64, 86) for col in range(6)), 5]}
        self.image = self.animationsDict['idle'][0][0]
        self.rect = pygame.Rect(0, 0, 64, 86)
        self.rect.x, self.rect.y = pos_x, pos_y
        self.mood = 20
        self.frame = 0
        self.frameDelay = 180
        self.animationType = 'idle'
        self.nextFrame = pygame.time.get_ticks()
        self.direction = 'front'
        self.drag = False
        self.directionVector = [0, 0]

    def add_animation(self, animation_name, file_name, r):
        """load animation and add animation to dict of animations"""
        self.animation = pygame.image.load(file_name)
        self.animationsDict.update(
            {animation_name: [list(self.animation.subsurface(col * 64, 0, 64, 86) for col in range(r)), r]})

    def next_frame(self, direction, frame_delay, animation_type):
        """inputs: self, direction, frame delay, animation type
            sets properties for object, change its position and change frame on next """
        self.direction = direction
        self.frameDelay = frame_delay
        self.animationType = animation_type
        if pygame.time.get_ticks() > self.nextFrame:
            self.frame = (self.frame + 1) % self.animationsDict[self.animationType][1]
            if self.direction != 'right':
                self.image = self.animationsDict[self.animationType][0][self.frame]
            else:
                self.image = pygame.transform.flip(self.animationsDict[self.animationType][0][self.frame], True, False)
            self.nextFrame = pygame.time.get_ticks() + self.frameDelay
            if self.animationType == 'walk':
                if self.direction == 'right':
                    self.rect.x += 3
                else:
                    self.rect.x -= 3

    def action(self):
        """returns random number between mood-10 to mood"""
        return random.uniform(self.mood - 10, self.mood)

    def distance_to(self, pos):
        """returns value of distance between object and given position"""
        return math.sqrt(pow(pos[0] - self.rect.x, 2) + pow(pos[1] - self.rect.y, 2))

    def distance_to_from_center(self, pos):
        """returns value of distance between object and given position from center of object"""
        return math.sqrt(pow(pos[0] - (self.rect.x + self.rect.width/2), 2)
                         + pow(pos[1] - (self.rect.y + self.rect.height/2), 2))
