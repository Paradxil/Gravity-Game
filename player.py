import pygame
import GlobalVars
from Vector2 import Vector2
from pygame import *
from Entity import Entity
from GlobalVars import *
from Tiles import *
from Level import Level
from Client import GameClient

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((13, TILESIZE-2))
        self.image = pygame.image.load('Images//player.png')
        self.rect = Rect(x, y, 18, 18)
        self.gravity = Vector2(0,0.3)
        #up down left right
        self.gravityDir = [False, True, False, False]
        self.friction = 0.4
        self.moveSpeed = 7
        self.acceleration = 3
        self.energy = 100
        self.gravityDirInt=1
        self.client = None

    def initClient(self, host, port):
        self.client = GameClient(host, int(port))
        self.client.getLevels()

    def update(self, up, down, left, right, akey, dkey, skey, wkey, level):
        if self.energy > 0:
            if akey:
                self.gravity = Vector2(-0.3,0)
                self.gravityDir[0] = False
                self.gravityDir[1] = False
                self.gravityDir[2] = True
                self.gravityDir[3] = False
                self.gravityDirInt=2
            if dkey:
                self.gravity = Vector2(0.3,0)
                self.gravityDir[0] = False
                self.gravityDir[1] = False
                self.gravityDir[2] = False
                self.gravityDir[3] = True
                self.gravityDirInt=3
            if skey:
                self.gravity = Vector2(0,0.3)
                self.gravityDir[0] = False
                self.gravityDir[1] = True
                self.gravityDir[2] = False
                self.gravityDir[3] = False
                self.gravityDirInt=1
            if wkey:
                self.gravity = Vector2(0,-0.3)
                self.gravityDir[0] = True
                self.gravityDir[1] = False
                self.gravityDir[2] = False
                self.gravityDir[3] = False
                self.gravityDirInt=0
        if up:
            # only jump if on the ground
            if self.onGround:
                if self.gravity.x == 0:
                    self.yvel -= self.gravity.y * 25 + abs(self.xvel)/3
                else:
                    self.xvel -= self.gravity.x * 25 + abs(self.yvel)/3
        if down:
            pass
        if left:
            if self.gravity.x == 0 and abs(self.xvel)<self.moveSpeed:
                self.xvel += self.gravity.rotate(90).x*self.acceleration
            elif self.gravity.y == 0 and abs(self.yvel)<self.moveSpeed:
                self.yvel += self.gravity.rotate(90).y*self.acceleration
        if right:
            if self.gravity.x == 0 and abs(self.xvel)<self.moveSpeed:
                self.xvel += self.gravity.rotate(-90).x*self.acceleration
            elif self.gravity.y == 0 and abs(self.yvel)<self.moveSpeed:
                self.yvel += self.gravity.rotate(-90).y*self.acceleration

        if self.gravity.x == 0 and self.xvel != 0:
                if self.xvel>0:
                    self.xvel -= self.friction
                elif self.xvel<0:
                    self.xvel += self.friction
                if abs(self.xvel) < self.friction:
                    self.xvel = 0
        elif self.gravity.y == 0 and self.yvel != 0:
            if self.yvel>0:
                self.yvel -= self.friction
            elif self.yvel<0:
                self.yvel += self.friction
            if abs(self.yvel) < self.friction:
                self.yvel = 0

        if self.gravityDir[1] == False:
            self.energy -= 0.1

        if self.energy <= 0:
            self.energy = 0
            self.gravityDir[0] = False
            self.gravityDir[1] = True
            self.gravityDir[2] = False
            self.gravityDir[3] = False
            self.gravity = Vector2(0,0.3)
            self.gravityDirInt=1
        elif self.energy > 100:
            self.energy = 100

        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += self.gravity.y
            self.xvel += self.gravity.x

            # max falling speed
            if self.yvel > 30: self.yvel = 30
            if self.yvel < -30: self.yvel = -30
            if self.xvel > 30: self.xvel = 30
            if self.xvel < -30: self.xvel = -30


        self.onGround = False
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, level)
        # increment in y direction
        self.rect.top += self.yvel
        # do y-axis collisions
        self.collide(0, self.yvel, level)

        if self.client != None:
            self.client.Move((self.rect.x,self.rect.y),level.thisLevelFile,self.gravityDirInt)

    def death(self, level):
        string3 = level.thisLevelFile
        #level.__init__()
        level.loadLevel("deathlevel.txt", self)
        level.levelBlockStrings[0] = string3
        self.xvel = 0
        self.yvel = 0
        self.energy = 100

    def collide(self, xvel, yvel, level):
        for p in level.projectiles:
            if sprite.collide_rect(self, p):
                self.death(level)
        for p in level.platforms:
            if sprite.collide_rect(self, p):
                if p.solid == True:
                    if isinstance(p, ExitBlock):
                        event.post(event.Event(QUIT))
                    if isinstance(p, LoadLevelBlock):
                        filen = level.levelBlockStrings[p.num]
                        #level.__init__()
                        while(level.loadLevel(filen, self)):
                            pass
                        self.xvel = 0
                        self.yvel = 0
                        self.energy = 100
                        return
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        if(self.gravity.x>0):
                            self.onGround = True
                        self.xvel = 0
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        if(self.gravity.x<0):
                            self.onGround = True
                        self.xvel = 0
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        if(self.gravity.y>0):
                            self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        if(self.gravity.y<0):
                            self.onGround = True
                        self.yvel = 0
                elif p.solid == False:
                    if isinstance(p, RechargeBlock):
                        if self.energy < 100:
                            self.energy += 0.2
                    if isinstance(p, SpikeBlock):
                        srect = Rect(p.rect.x + 6, p.rect.y + 6, p.rect.width - 12, p.rect.height - 12)
                        if srect.colliderect(self.rect):
                            self.death(level)
                            return


    def draw(self, surface, camera):

        pygame.draw.rect(surface, Color("#DD5566"), [DISPLAY[0] - 110, 10, 100, 20])
        if self.energy>0:
            pygame.draw.rect(surface, Color("#55DD66"), [DISPLAY[0] - 110, 10, self.energy, 20])

        tmp = self.image

        if self.gravityDir[2]:
            tmp = pygame.transform.rotate(tmp, -90)
            #self.rect = Rect(self.rect.x, self.rect.y, 18, 13)
        elif self.gravityDir[3]:
            tmp = pygame.transform.rotate(tmp, 90)
            #self.rect = Rect(self.rect.x, self.rect.y, 18, 13)

        elif self.gravityDir[0]:
            tmp = pygame.transform.flip(self.image, False, True)

            #self.rect = Rect(self.rect.x, self.rect.y, 13,18)
        else:
            #self.rect = Rect(self.rect.x, self.rect.y, 13,18)
            pass

        if self.xvel<0:

            surface.blit(tmp, Rect(self.rect.x - camera.x, self.rect.y - camera.y, TILESIZE, TILESIZE))
        else:
            if self.gravityDir[0] or self.gravityDir[1]:
                tmp = pygame.transform.flip(tmp, True, False)
            else:
                tmp = pygame.transform.flip(tmp, False, True)
            surface.blit(tmp, Rect(self.rect.x - camera.x, self.rect.y - camera.y, TILESIZE, TILESIZE))