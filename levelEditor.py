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
import os.path
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

        self.hasTotalFocus = None

        self.exitEditor = Button(position = (10,10), size = (50,50), parent = self.gui, text = "EXIT")

        self.newButton = Button(position = (60,10), size = (50,50), parent = self.gui, text = "NEW")
        self.newButton.onClick = self.newLevel

        self.saveButton = Button(position = (110,10), size = (50,50), parent = self.gui, text = "SAVE")
        self.saveButton.onClick = self.saveLevel

        self.openButton = Button(position = (160,10), size = (50,50), parent = self.gui, text = "OPEN")
        self.openButton.onClick = self.openLevel

        #self.toolsWindow = Window(position = (10,50), size = (170,60), parent = self.gui, text = "TOOLS")

        self.tilesWindow = Window(position = (10,60), size = (100,400), parent = self.gui, text = "TILES")
        self.tilesWindow.closeable = False

        self.saveWindow = Window(position = (50,60), size = (400,100), parent = self.gui, text = "SAVE")
        self.saveWindow.visible = False
        self.saveWindow.closeable = False
        self.saveWindow.onShade = self.shadeSaveWindow
        self.saveTextBox = TextBox(position = (10, 30), size = (380,20), parent = self.saveWindow)
        self.saveWindowSave = Button(position = (175,60), size = (50,50), parent = self.saveWindow, text = "SAVE")
        self.saveWindowSave.onClick = self.saveLevelFile

        self.openWindow = Window(position = (50,60), size = (200,400), parent = self.gui, text = "OPEN")
        self.openWindow.visible = False
        self.openWindow.closeable = False
        self.openWindow.onShade = self.shadeOpenWindow
        self.openWindowOpen = Button(position = (75,370), size = (50,50), parent = self.openWindow, text = "OPEN")
        self.openWindowOpen.onClick = self.openLevelFile
        self.levelsListBox = ListBox(position= (10,30), size=(180,330), parent=self.openWindow)
        
        self.chooseWindow = Window(position = (50,60), size = (200,400), parent = self.gui, text = "CHOOSE")
        self.chooseWindow.visible = False
        self.chooseWindow.closeable = False
        self.chooseWindow.onShade = self.shadechooseWindow
        self.submit = Button(position = (75,370), size = (50,50), parent = self.chooseWindow, text = "CHOOSE")
        self.submit.onClick = self.chooseLevelFile
        self.chooseLevelsListBox = ListBox(position= (10,30), size=(180,330), parent=self.chooseWindow)
        
        for root, dirs, files in os.walk('Levels//'):
            for file in files:
                if file.endswith(".txt"):
                    self.levelsListBox.items.append(file)

        '''self.eraseButton = Button(position = (10,30), size = (50,50), parent = self.toolsWindow, text = "ERASE")
        self.eraseButton.onClick = self.eraseClick

        self.panButton = Button(position = (60,30), size = (50,50), parent = self.toolsWindow, text = "PAN")
        self.panButton.onClick = self.panClick

        self.placeButton = Button(position = (110,30), size = (50,50), parent = self.toolsWindow, text = "PLACE")
        self.placeButton.onClick = self.placeClick'''

        self.tileButtons = [TileButton(StartBlock(0,0),position = (10,self.tilesWindow.nextPosition(5)[1]),parent = self.tilesWindow),
                            TileButton(LoadLevelBlock(0,0,0),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
                            TileButton(FloorBlock(0,0),position = self.tilesWindow.nextPosition(5),parent = self.tilesWindow),
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
        if self.gui.findTopMost(mouse.get_pos())==self.gui and self.hasTotalFocus==None:
            if mouse.get_pressed()[1]:
                self.tool=0
            elif mouse.get_pressed()[2]:
                self.tool=1
            if mouse.get_pressed()[0]:
                self.tool=2
            self.toolFunctions[self.tool](e)
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    self.level.saveLevel("tmp",self.player)
                    self.level.loadLevel("tmp.map",self.player)

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
            change = self.level.addTile(tmp)
            self.camera[0]+=change[0]
            self.camera[1]+=change[1]
            self.level.createLevelImage()

            if isinstance(self.selectedTile, LoadLevelBlock):
                self.chooseLevel()

    def getTileAtPos(self, pos):
        for i in range(0,len(self.level.platforms)):
            if self.level.platforms[i].rect.collidepoint(pos[0],pos[1]):
                return i
        return -1

    def update(self, up, down, left, right, akey, dkey, skey, wkey):

        self.gui.update()

        if self.hasTotalFocus == None:
            self.player.update(up, down, left, right, akey, dkey, skey, wkey, self.level)
            for tile in self.tileButtons:
                if tile.mouseclick:
                    self.selectedTile = tile.tile

            if self.exitEditor.mouseclick:
                return 0
            return 2



        return 2


    def draw(self, screen):
        #draw everything
        #fill screen with background

        #draw level
        self.level.draw(screen, Vector2(self.camera[0]+self.change[0],self.camera[1]+self.change[1]))
        self.player.draw(screen, Vector2(self.camera[0]+self.change[0],self.camera[1]+self.change[1]))
        self.gui.draw()

    '''def eraseClick(self,button):
        self.tool = 1

    def panClick(self,button):
        self.tool = 0

    def placeClick(self,button):
        self.tool = 2'''

    def newLevel(self,button):
        self.level = Level()
        self.level.loadLevel("empty.txt", self.player)

    def saveLevel(self,button):
        self.saveWindow.unshade()
        self.saveWindow.visible = True

    def openLevel(self,button):
        self.levelsListBox.items = []
        for root, dirs, files in os.walk('Levels//'):
            for file in files:
                if file.endswith(".txt") or file.endswith(".map"):
                    self.levelsListBox.items.append(file)

        self.openWindow.unshade()
        self.openWindow.visible = True

    def chooseLevel(self):
        self.hasTotalFocus = self.chooseWindow
        self.chooseLevelsListBox.items = []
        for root, dirs, files in os.walk('Levels//'):
            for file in files:
                if file.endswith(".txt") or file.endswith(".map"):
                    self.chooseLevelsListBox.items.append(file)

        self.chooseWindow.unshade()
        self.chooseWindow.visible = True

    def shadeOpenWindow(self, button):
        self.openWindow.visible = False

    def shadechooseWindow(self, button):
        self.chooseWindow.visible = False

    def shadeSaveWindow(self, button):
        self.saveWindow.visible = False

    def openLevelFile(self, button):
        self.level = Level()
        self.level.loadLevel(self.levelsListBox.items[self.levelsListBox.selectedIndex], self.player)

    def chooseLevelFile(self, button):
        self.level.levelBlockStrings.append(self.chooseLevelsListBox.items[self.chooseLevelsListBox.selectedIndex])
        self.level.platforms[len(self.level.platforms)-1].num = len(self.level.levelBlockStrings)-1
        self.hasTotalFocus = None
        self.chooseWindow.visible = False

    def saveLevelFile(self, button):
        self.level.saveLevel(self.saveTextBox.text,self.player)