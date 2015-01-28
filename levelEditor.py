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

class LevelEditor():
    def __init__(self):
        self.gui = Desktop()
        self.exitEditor = Button(position = (10,10), size = (50,50), parent = self.gui, text = "EXIT")

        self.toolsWindow = Window(position = (300,220), size = (170,60), parent = self.gui, text = "TOOLS")


        self.eraseButton = Button(position = (10,30), size = (50,50), parent = self.toolsWindow, text = "ERASE")
        self.eraseButton.onClick = self.eraseClick

        self.panButton = Button(position = (60,30), size = (50,50), parent = self.toolsWindow, text = "PAN")
        self.panButton.onClick = self.panClick

        self.placeButton = Button(position = (110,30), size = (50,50), parent = self.toolsWindow, text = "PLACE")
        self.placeButton.onClick = self.placeClick

        self.camera = [0,0]
        self.change = [0,0]

        self.player = Player(TILESIZE, TILESIZE)

        self.level = Level()
        self.level.loadLevel("mainmenu.txt", self.player)

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
        if not self.toolsWindow.mouseover:
            self.toolFunctions[self.tool](e)

    def pan(self, e):
        if e.type == MOUSEBUTTONDOWN:
            self.mouseClickPos = mouse.get_pos()
            mb = mouse.get_pressed()
            if mb[0]:
                self.lmbPressed = True

        if e.type == MOUSEBUTTONUP:
            mb = mouse.get_pressed()
            if not mb[0]:
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
        if e.type == MOUSEBUTTONDOWN:
            i = self.getTileAtPos((mouse.get_pos()[0]+self.camera[0],mouse.get_pos()[1]+self.camera[1]))
            if i!=-1:
                self.level.platforms.remove(self.level.platforms[i])
                self.level.createLevelImage()

    def place(self, e):
        pass

    def getTileAtPos(self, pos):
        for i in range(0,len(self.level.platforms)):
            if self.level.platforms[i].rect.collidepoint(pos[0],pos[1]):
                return i
        return -1

    def update(self):
        self.gui.update()

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