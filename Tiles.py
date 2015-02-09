import pygame
import GlobalVars
from Vector2 import Vector2
from pygame import *
from Entity import Entity
from GlobalVars import *
from Projectile import Projectile
from copy import deepcopy

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((TILESIZE, TILESIZE))
        self.image.convert()
        self.image = pygame.image.load('Images//background.png')
        self.rect = Rect(x, y, TILESIZE, TILESIZE)
        self.solid = True
        self.interactable = False
    def update(self, player):
        pass

    def draw(self, surface, camera):
        surface.blit(self.image, Rect(self.rect.x - camera.x, self.rect.y - camera.y, TILESIZE, TILESIZE))

    def copy(self):
        tmp = deepcopy(self)
        tmp.image = self.image
        return tmp

class ShootBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.pimage = pygame.image.load('Images//projectile.png')
        self.pimage = pygame.transform.scale(self.pimage, (8,8))
        self.image2 = pygame.image.load('Images//shoot.png')
        self.reloadTime = 69
        self.updateTime = 0
        self.interactable = True
        self.solid = False

    def update(self, level):
        self.updateTime += 1

        if self.updateTime > self.reloadTime:
            self.updateTime = 0
            level.projectiles.append(Projectile(Rect(self.rect.x+self.rect.width/2-3, self.rect.y+self.rect.height/2-3, 8, 8), self.pimage, Vector2(8,0)))
            level.projectiles.append(Projectile(Rect(self.rect.x+self.rect.width/2-3, self.rect.y+self.rect.height/2-3, 8, 8), self.pimage, Vector2(0,8)))
            level.projectiles.append(Projectile(Rect(self.rect.x+self.rect.width/2-3, self.rect.y+self.rect.height/2-3, 8, 8), self.pimage, Vector2(-8,0)))
            level.projectiles.append(Projectile(Rect(self.rect.x+self.rect.width/2-3, self.rect.y+self.rect.height/2-3, 8, 8), self.pimage, Vector2(0,-8)))

    def draw(self, surface, camera):
        Platform.draw(self, surface, camera)
        surface.blit(self.image2, (self.rect.x-camera.x, self.rect.y-camera.y))

class WallBlock(Platform):
    def __init__(self, x, y):
            Platform.__init__(self, x, y)
            self.image = pygame.image.load('Images//wall.png')

class BlackBlock(Platform):
    def __init__(self, x, y):
            Platform.__init__(self, x, y)
            self.image.fill(Color("#000000"))

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('Images//exit.png')

class LoadLevelBlock(Platform):
    def __init__(self, x, y, levelNum):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('Images//exit.png')
        self.num = levelNum

class FloorBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.solid = False
        self.image = pygame.image.load('Images//background.png')

class RechargeBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('Images//power.png')
        self.solid = False

class SpikeBlock(Platform):
    def __init__(self, x, y, r):
        Platform.__init__(self, x, y)
        self.solid = False
        self.tim = Surface((TILESIZE, TILESIZE))
        self.tim = pygame.image.load('Images//spike.png')
        self.tim = pygame.transform.rotate(self.tim, r)
        self.r = r


    def draw(self, surface, camera):
        Platform.draw(self, surface, camera)
        surface.blit(self.tim, (self.rect.x-camera.x, self.rect.y-camera.y))

    def copy(self):
        tmp=Platform.copy(self)
        tmp.tim = self.tim
        return tmp

class TextBlock(Platform):
    def __init__(self,x,y,char):
        Platform.__init__(self,x,y)
        self.text = char
        self.solid = False
        self.font = pygame.font.SysFont("monospace", TILESIZE)

    def draw(self, surface, camera):
        Platform.draw(self, surface, camera)
        label = self.font.render(self.text, 1, (0,0,0))
        surface.blit(label, (self.rect.x-camera.x, self.rect.y-camera.y))

class StartBlock(Platform):
    def __init__(self, x, y):
            Platform.__init__(self, x, y)
            self.solid = False
            self.image = pygame.image.load('Images//start.png')