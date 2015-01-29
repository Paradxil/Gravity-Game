import pygame
import GlobalVars
from Vector2 import Vector2
from pygame import *
from Entity import Entity
from GlobalVars import *
from Projectile import Projectile
from Tiles import *

class Level():
    def __init__(self):
        self.platforms = []
        self.level = []
        #Strings of filenames for all of the next level blocks in order.
        self.levelBlockStrings = []
        self.thisLevelFile = ""
        self.interactablePlatforms = []
        self.levelImage = Surface((0,0))
        self.levelSize = Vector2(0,0)
        self.blackBlocks = []
        self.projectiles = []

    def buildLevel(self, player):
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "#":
                    p = WallBlock(x, y)
                    self.platforms.append(p)
                elif col == "x":
                    e = ExitBlock(x, y)
                    self.platforms.append(e)
                elif col == "+":
                    e = ShootBlock(x, y)
                    self.platforms.append(e)
                elif col == "v":
                    e = SpikeBlock(x, y, 180)
                    self.platforms.append(e)
                elif col == "^":
                    e = SpikeBlock(x, y, 0)
                    self.platforms.append(e)
                elif col == ">":
                    e = SpikeBlock(x, y, -90)
                    self.platforms.append(e)
                elif col == "<":
                    e = SpikeBlock(x, y, 90)
                    self.platforms.append(e)
                elif col == "@":
                    e = RechargeBlock(x, y)
                    self.platforms.append(e)
                elif col == ".":
                    e = FloorBlock(x, y)
                    self.platforms.append(e)
                elif is_number(col):
                    e = LoadLevelBlock(x, y, int(col))
                    self.platforms.append(e)
                elif col.isalpha():
                    e = TextBlock(x,y,col)
                    self.platforms.append(e)
                x += TILESIZE
            y += TILESIZE
            if x>self.levelSize.x:
                self.levelSize.x = x
            if y>self.levelSize.y:
                self.levelSize.y = y
            x = 0
        return True


    def loadLevel(self, fileName, player):
        player.gravity = Vector2(0,0.3)
        player.gravityDir[1] = True
        player.gravityDir[0] = False
        player.gravityDir[2] = False
        player.gravityDir[3] = False
        self.thisLevelFile = fileName
        self.level = []
        self.platforms = []
        self.levelBlockStrings = []
        self.levelImage = Surface((0,0))
        self.levelSize = Vector2(0,0)
        self.interactablePlatforms = []
        self.projectiles = []
        read = open("Levels//"+fileName, 'r')

        start = False
        for line in read:
            if line[0] == '/' and line[1] == '/':
                pass
            elif start == True:
                self.level.append(line)

            elif line.__contains__('start'):
                start = True
            elif line.__contains__('player'):
                px = line.split(',')[1]
                py = line.split(',')[2]
                player.rect = Rect(int(px)*TILESIZE, int(py)*TILESIZE, player.rect.width, player.rect.height)
            elif line.__contains__('levelblock'):
                self.levelBlockStrings.append(line.split(',')[1].rstrip())
        self.buildLevel(player)
        self.createLevelImage()

    def createLevelImage(self):
        self.levelImage = Surface((self.levelSize.x, self.levelSize.y))

        img = pygame.image.load('Images//background.png')

        for y in range(0,self.levelSize.y,60):
            for x in range(0,self.levelSize.x,60):
                #self.levelImage.blit(img,(x,y))
                pass

        img2 = Surface((TILESIZE, TILESIZE))
        img2.convert()
        img2.fill(Color("#000000"))

        platformPos = []
        for p in self.platforms:
            platformPos.append(Vector2(p.rect.x, p.rect.y))
            if p.interactable == False:
                p.draw(self.levelImage, Vector2(0,0))
            else:
                self.interactablePlatforms.append(p)
                #self.platforms.remove(p)


    def draw(self, surface, camera):
        surface.blit(self.levelImage, (-camera.x,-camera.y))
        for p in self.interactablePlatforms:
            p.draw(surface, camera)
            p.update(self)
        for p in self.projectiles:
            p.draw(surface, camera)
            if p.update(self)==5:
                self.projectiles.remove(p)