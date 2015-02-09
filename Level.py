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
                elif col == "*":
                    player.rect = Rect(int(x), int(y), player.rect.width, player.rect.height)
                    e = StartBlock(x, y)
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

    def getTileAtPos(self, pos):
        for i in range(0,len(self.platforms)):
            if self.platforms[i].rect.collidepoint(pos[0],pos[1]):
                return self.platforms[i]
        return -1

    def saveLevel(self, fileName, player):
        #player.gravity = Vector2(0,0.3)
        #player.gravityDir[1] = True
        #player.gravityDir[0] = False
        #player.gravityDir[2] = False
        #player.gravityDir[3] = False
        file = open("Levels//"+fileName+".map", 'w+')

        text = []
        header = []
        for y in range(0,self.levelSize.y/TILESIZE):
            line = ""
            for x in range(0,self.levelSize.x/TILESIZE):
                tile = self.getTileAtPos((x*TILESIZE, y*TILESIZE))
                if tile==-1:
                    line+=" "
                if isinstance(tile, WallBlock):
                    line += "#"
                elif isinstance(tile, ExitBlock):
                    line += "x"
                elif isinstance(tile, ShootBlock):
                    line += "+"
                elif isinstance(tile, SpikeBlock):
                    if tile.r == 0:
                        line += "^"
                    elif tile.r == -90:
                        line += ">"
                    elif tile.r == 90:
                        line += "<"
                    elif tile.r == 180:
                        line += "v"
                elif isinstance(tile, RechargeBlock):
                    line += "@"
                elif isinstance(tile, FloorBlock):
                    line += "."
                elif isinstance(tile, StartBlock):
                    line += "*"
                elif isinstance(tile, LoadLevelBlock):
                    line += str(tile.num)
                elif isinstance(tile, TextBlock):
                    line += tile.text
            text.append(line)
        for t in self.levelBlockStrings:
            file.write("levelblock,"+t+"\n")
        file.write("start \n")
        for t in text:
            file.write(t+"\n")

        file.close()

    def addTile(self, tile):
        x = tile.rect.x
        y = tile.rect.y
        change = [0,0]
        if x < 0:
            xdif = -x
            change[0] = xdif
            x = 0
            for p in self.platforms:
                p.rect.x += xdif
            self.levelSize.x += xdif
        elif x+TILESIZE >= self.levelSize.x:
            self.levelSize.x = x+TILESIZE

        if y < 0:
            ydif = -y
            y = 0
            change[1] = ydif
            for p in self.platforms:
                p.rect.y += ydif
            self.levelSize.y += ydif
        elif y+TILESIZE >= self.levelSize.y:
            self.levelSize.y = y+TILESIZE

        tile.rect.x = x
        tile.rect.y = y

        self.platforms.append(tile)
        return change

    def createLevelImage(self):
        self.levelImage = Surface((self.levelSize.x, self.levelSize.y))

        platformPos = []
        self.interactablePlatforms = []
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