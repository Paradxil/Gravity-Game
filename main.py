import sys
from time import sleep, localtime
import pygame
import math
import random
import GlobalVars
from player import Player
from Vector2 import Vector2
from Entity import Entity
from pygame import *
from GlobalVars import *
from Tiles import *
from Level import Level
from Client import GameClient
from Projectile import Projectile
import gui
from gui import *
FLAGS = RESIZABLE

def main():

    pygame.init()
    screen = display.set_mode(DISPLAY, RESIZABLE)
    myfont = pygame.font.SysFont("monospace", 15)
    menu = pygame.font.SysFont("monospace", 32)
    title = pygame.font.SysFont("monospace", 72)
    display.set_caption("Gravity Game")
    timer = time.Clock()
    done = False
    up = down = left = right = False
    akey = wkey = skey = dkey = False
    player = Player(TILESIZE, TILESIZE)
    camera = Vector2(0,0)

    # build the level
    level = Level()
    level.loadLevel("mainmenu.txt", player)

    #any variables used in other functions need to be global
    global pause
    global play
    global multiplayer
    global host
    global port
    global client

    pause = False
    play = False
    multiplayer = False

    host = ""
    port = ""

    #GUI STUFF
    #This way it's easy to load the example gui skin:
    import defaultStyle

    defaultStyle.init(gui)

    #First, we create a desktop to contain all the widgets
    desktop = Desktop()

    button = Button(position = (10,100), size = (200,50), parent = desktop, text = "SINGLE PLAYER")

    button.onClick = singlePlayerOnClick

    Label(position = (10,130),size = (50,50), parent = desktop, text = "HOST:")
    hostbx = TextBox(position = (60, 130), parent = desktop)
    Label(position = (10,160),size = (50,50), parent = desktop, text = "PORT:")
    portbx = TextBox(position = (60, 160), parent = desktop)

    mbutton = Button(position = (10,190), size = (200,50), parent = desktop, text = "MULTIPLAYER")
    mbutton.onClick = multiPlayerOnClick

    selected = 0

    while not done:
        #Frame rate or FPS
        timer.tick(60)
        sleep(0.01)
        events = gui.setEvents()
        #Check event queue for events and then act on them.
        for e in events:
            #Quit game event
            if e.type == QUIT:
                done = True
            #Resize Window Event
            elif e.type == VIDEORESIZE:
                DISPLAY[0] = e.w
                DISPLAY[1] = e.h
                screen = display.set_mode(DISPLAY, RESIZABLE)
                screen.fill(Color("#FFFFFF"))
            #Key Presses
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
                right = False
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
                left = False
            if e.type == KEYDOWN and e.key == K_a:
                akey = True
            if e.type == KEYDOWN and e.key == K_w:
                wkey = True
            if e.type == KEYDOWN and e.key == K_s:
                skey = True
            if e.type == KEYDOWN and e.key == K_d:
                dkey = True
            if e.type == KEYDOWN and e.key == K_p:
                pause = not pause

            if e.type == KEYUP and e.key == K_UP:
                if play == False:
                    if selected < 0:
                        selected = 0
                    else:
                        selected -= 1
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                if play == False:
                    if selected > 3:
                        selected = 0
                    else:
                        selected += 1
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_a:
                akey = False
            if e.type == KEYUP and e.key == K_w:
                wkey = False
            if e.type == KEYUP and e.key == K_s:
                skey = False
            if e.type == KEYUP and e.key == K_d:
                dkey = False
            if e.type == KEYUP and e.key == K_ESCAPE:
                if play == False:
                    done = True
                if pause:
                    play = False
                    pause = False
                if not pause:
                    pause = True
            if e.type == KEYUP and e.key == K_SPACE:
                if play == False:
                    if selected == 0:
                        play = True
                        multiplayer = False
                    if selected == 3:
                        play = True
                        multiplayer = True
                        try:
                            client = GameClient(hostbx.value, int(portbx.value))
                        except:
                            play = False

        #Then update the desktop you're using
        screen.fill(Color('#000000'))
        if play:
            # update everything
            # update player, pass in different key states
            if not pause:
                player.update(up, down, left, right, akey, dkey, skey, wkey, level)
                if multiplayer:
                    client.Move((player.rect.x,player.rect.y),level.thisLevelFile,player.gravityDirInt)

                #update camera
                #move with player
                camera.x = player.rect.x - DISPLAY[0]/2
                camera.y = player.rect.y - DISPLAY[1]/2

            #draw everything
            #fill screen with background

            #draw level
            level.draw(screen, camera)

            #draw player
            player.draw(screen, camera)
            if multiplayer:
                client.Loop(screen, camera, level.thisLevelFile)
                if client.disconnected:
                    text1 = menu.render("DISCONNECTED FROM SERVER.", 1, (255,255,255))
                    subText = myfont.render("YOU CAN CONTINUE PLAYING IN SINGLE PLAYER OR EXIT TO THE MENU.", 1, (255,255,255))
                    multiplayer = False
                    pause = True
                    screen.blit(text1, (10, screen.get_size()[1]-10-32-16-5))
                    screen.blit(subText, (10, screen.get_size()[1]-10-16))
            #flip backbuffer to screen

            if pause:
                text1 = menu.render("PAUSED", 1, (255,255,255))
                subText = myfont.render("PRESS 'P' TO RESUME", 1, (255,255,255))
                screen.blit(text1, (10, 10))
                screen.blit(subText, (10, 80))
                subText = myfont.render("PRESS 'ESC' TO EXIT TO MENU", 1, (255,255,255))
                screen.blit(subText, (10, 100))
        else:
            #Last thing to draw, desktop
            text1 = title.render("GRAVITY GAME", 1, (255,255,255))
            screen.blit(text1, (10, 10))
            desktop.update()
            host = hostbx.text
            port = portbx.text
            desktop.draw()


        pygame.display.flip()


def singlePlayerOnClick(button):
    #do this to access the global version of the variable
    global pause
    global play
    global multiplayer

    play = True
    pause = False
    multiplayer = False

def multiPlayerOnClick(button):
    #do this to access the global version of the variable
    global pause
    global play
    global multiplayer
    global client
    global host
    global port

    #Don't do anything if trying to create client fails
    try:
        client = GameClient(host, int(port))

        play = True
        pause = False
        multiplayer = True

    except:
        pass

if(__name__ == "__main__"):
    main()
    pygame.quit()
