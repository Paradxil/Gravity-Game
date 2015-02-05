import pygame
import GlobalVars
from Vector2 import Vector2
from pygame import *
from Entity import Entity
from GlobalVars import *
from player import Player
from Tiles import *
from Level import Level
import gui
from gui import *
from copy import deepcopy

class TileButton(ImageButton):
    def __init__(self, tile, position = (10,10), parent = None, enabled = True):
        surface = tile.image
        tile.draw(surface,Vector2(0,0))
        style = createImageButtonStyle(surface,tile.image.get_size()[0])
        ImageButton.__init__(self,position, parent, style, enabled)
        self.tile = tile

class LevelEditor():
    def __init__(self):
        self.gui = Desktop()
        self.exitEditor = Button(position = (10,10), size = (50,50), parent = self.gui, text = "EXIT")
        self.exitEditor = Button(position = (60,10), size = (50,50), parent = self.gui, text = "NEW")
        self.exitEditor = Button(position = (110,10), size = (50,50), parent = self.gui, text = "SAVE")
        self.exitEditor = Button(position = (160,10), size = (50,50), parent = self.gui, text = "OPEN")

        self.toolsWindow = Window(position = (10,50), size = (170,60), parent = self.gui, text = "TOOLS")
        self.tilesWindow = Window(position = (10,120), size = (100,400), parent = self.gui, text = "TILES")

        self.eraseButton = Button(position = (10,30), size = (50,50), parent = self.toolsWindow, text = "ERASE")
        self.eraseButton.onClick = self.eraseClick

        self.panButton = Button(position = (60,30), size = (50,50), parent = self.toolsWindow, text = "PAN")
        self.panButton.onClick = self.panClick

        self.placeButton = Button(position = (110,30), size = (50,50), parent = self.toolsWindow, text = "PLACE")
        self.placeButton.onClick = self.placeClick

        self.tileButtons = [TileButton(FloorBlock(0,0),position = (10,30),parent = self.tilesWindow),
                            TileButton(WallBlock(0,0),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
                            TileButton(RechargeBlock(0,0),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
                            TileButton(SpikeBlock(0,0,0),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
                            TileButton(SpikeBlock(0,0,90),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
                            TileButton(SpikeBlock(0,0,-90),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
                            TileButton(SpikeBlock(0,0,180),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow)]

        self.selectedTile = FloorBlock(0,0)

        self.camera = [0,0]
        self.change = [0,0]

        self.player = Player(TILESIZE, TILESIZE)

        self.level = Level()
        self.level.loadLevel("empty.txt", self.player)

         #move view
        self.mouseClickPos = [0,0]
        self.change = [0,0]
        self.rmbPressed = False
        self.lmbPressed = False
        self.mmbPressed = False

        #0 = pan
        self.tool = 1
        self.toolFunctions = [self.pan,self.erase,self.place]

    def handleEvent(self, e):
        if self.gui.findTopMost(mouse.get_pos())==self.gui:
            if mouse.get_pressed()[1]:
                self.tool=0
            elif mouse.get_pressed()[2]:
                self.tool=1
            if mouse.get_pressed()[0]:
                self.tool=2
            self.toolFunctions[self.tool](e)

    def pan(self, e):
        if e.type == MOUSEBUTTONDOWN:
            self.mouseClickPos = mouse.get_pos()
            self.lmbPressed = True

        if e.type == MOUSEBUTTONUP:
            self.lmbPressed = False
            self.camera[0] += self.change[0]
            self.camera[1] += self.change[1]
            self.change[0] = 0
            self.change[1] = 0

        if e.type == MOUSEMOTION:
            if self.lmbPressed:
                self.change[0] = (self.mouseClickPos[0] - e.pos[0])
                self.change[1] = (self.mouseClickPos[1] - e.pos[1])

    def erase(self, e):
        mb = mouse.get_pressed()
        if mb[0] or mb[1] or mb[2]:
            i = self.getTileAtPos((mouse.get_pos()[0]+self.camera[0],mouse.get_pos()[1]+self.camera[1]))
            if i!=-1:
                self.level.platforms.remove(self.level.platforms[i])
                self.level.createLevelImage()

    def place(self, e):
        mb = mouse.get_pressed()
        if mb[0] and self.selectedTile!=None:
            i = self.getTileAtPos((mouse.get_pos()[0]+self.camera[0],mouse.get_pos()[1]+self.camera[1]))
            if i!=-1:
                self.level.platforms.remove(self.level.platforms[i])
            x = (((mouse.get_pos()[0]+self.camera[0])/TILESIZE)*TILESIZE)
            y = (((mouse.get_pos()[1]+self.camera[1])/TILESIZE)*TILESIZE)
            tmp = self.selectedTile.copy()
            tmp.rect.x = x
            tmp.rect.y = y
            self.level.platforms.append(tmp)
            self.level.createLevelImage()

    def getTileAtPos(self, pos):
        for i in range(0,len(self.level.platforms)):
            if self.level.platforms[i].rect.collidepoint(pos[0],pos[1]):
                return i
        return -1

    def update(self):
        self.gui.update()
        for tile in self.tileButtons:
            if tile.mouseclick:
                self.selectedTile = tile.tile

        if self.exitEditor.mouseclick:
            return 0
        return 2

    def draw(self, screen):
        #draw everything
        #fill screen with background

        #draw level
        self.level.draw(screen, Vector2(self.camera[0]+self.change[0],self.camera[1]+self.change[1]))

        self.gui.draw()

    def eraseClick(self,button):
        self.tool = 1

    def panClick(self,button):
        self.tool = 0

    def placeClick(self,button):
        self.tool = 2