__author__ = 'Hunter Stratton'
import sys
from time import sleep
import pygame

from GlobalVars import *

from PodSixNet.Connection import connection, ConnectionListener

class GameClient(ConnectionListener):
    def __init__(self, host, port):
        self.image = pygame.Surface((13, TILESIZE-2))
        self.image = pygame.image.load('Images//player.png')
        self.Connect((host, port))
        self.players = {}
        self.id=""
        self.disconnected = False

    def Loop(self, screen, camera, level):
        self.Pump()
        connection.Pump()
        for i in self.players:
            if self.players[i]['level']==level and i!=self.id:
                self.Draw(self.players[i]['pos'], screen, camera, self.players[i]['gravity'])

        #if "connecting" in self.statusLabel:
         #   self.statusLabel = "connecting" + ("." * ((self.frame / 30) % 4))
    #######################
    ### Event callbacks ###
    #######################
    #def PenDraw(self, e):
    #	connection.Send({"action": "draw", "point": e.pos})

    def Move(self, pos, level, gravity):
        connection.Send({"action": "move", "pos": pos, "gravity": gravity, "level": level})

    ###############################
    ### Network event callbacks ###
    ###############################

    def Network_initial(self, data):
        self.id = data['id']
        self.players = data['players']

    def Network_move(self, data):
        self.players[data['id']]['pos']=(data['pos'][0],data['pos'][1])
        self.players[data['id']]['gravity']=data['gravity']
        self.players[data['id']]['level']=data['level']

    def Network_players(self, data):
        self.playersLabel = str(len(data['players'])) + " players"
        mark = []

        for i in data['players']:
            if not self.players.has_key(i):
                self.players[i] = {'pos': (0,0), 'gravity': 0, 'level': ""}

        for i in self.players:
            if not i in data['players'].keys():
                mark.append(i)

        for m in mark:
            del self.players[m]

    def Network(self, data):
        # print 'network:', data
        pass

    def Network_connected(self, data):
        self.statusLabel = "connected"

    def Network_error(self, data):
        print data
        import traceback
        traceback.print_exc()
        self.statusLabel = data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print "Disconnected.  You can keep playing offline but your progress will not be saved."
        self.disconnected = True

    def Draw(self, pos, surface, camera, gravityDir):
        tmp=self.image
        if gravityDir==2:
            tmp = pygame.transform.rotate(tmp, -90)
            #self.rect = Rect(self.rect.x, self.rect.y, 18, 13)
        elif gravityDir==3:
            tmp = pygame.transform.rotate(tmp, 90)
            #self.rect = Rect(self.rect.x, self.rect.y, 18, 13)

        elif gravityDir==0:
            tmp = pygame.transform.flip(self.image, False, True)

            #self.rect = Rect(self.rect.x, self.rect.y, 13,18)
        else:
            #self.rect = Rect(self.rect.x, self.rect.y, 13,18)
            pass


        if gravityDir==0 or gravityDir==1:
            tmp = pygame.transform.flip(tmp, True, False)
        else:
            tmp = pygame.transform.flip(tmp, False, True)

        surface.blit(tmp, (pos[0] - camera.x, pos[1] - camera.y, TILESIZE, TILESIZE))
