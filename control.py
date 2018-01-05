#!/usr/bin/env python3
import SDClient
import logging
import pygame
from pygame.locals import *
import time
import threading
import copy

class steering():
    def __init__(self):
        cli = SDClient.client('localhost', 'joystick', 'testship') 
        self.rudder = cli.gameVariable(['rudder'])
        self.shipAxis = {}
        self.joyAxis = {}
        self.aLock = threading.Lock()
        self.stop = False #stop updating ship

    def getJoyAxis(self):
        self.joyAxis = {
            'roll':joy.get_axis(0),
            'pitch':-joy.get_axis(2),
            'yaw':joy.get_axis(1),
        }
        return self.joyAxis

    def getShipAxis(self):
        logging.debug(repr(self.shipAxis))
        return self.shipAxis

    def updateShip(self):
        while self.stop == False:
            uA = copy.copy(self.joyAxis)

            #send joystick data to server
            for key, value in uA.items():
                self.rudder.parse([key,str(value)])

            #get ship status
            for axis in self.rudder.parse(['get']).message.split(','):
                a = axis.split(':')
                self.shipAxis[a[0].strip()] = float(a[1].strip())

logging.basicConfig(level = logging.INFO)

#prepare pygame display
logging.info('setting up pygame')
pygame.init()
pygame.display.init()
resolution = [700,700]
screen = pygame.display.set_mode(resolution)
pygame.joystick.init()

logging.info('setting up game client')
rudder = steering()

logging.info('setting up threads')
shipThread = threading.Thread(target=rudder.updateShip)
shipThread.start()

logging.info('ready!')
try:
    while True:
        pygame.event.get()
        joy = pygame.joystick.Joystick(0)
        joy.init()

        #draw background
        screen.fill((0,0,0))
        pygame.draw.line(screen, (0,0,255), [0, resolution[1]/2], [resolution[0],resolution[1]/2], 1)
        pygame.draw.line(screen, (0,0,255), [resolution[0]/2,0], [resolution[0]/2,resolution[1]], 1)

        #draw ship data
        x = int(rudder.getShipAxis().get('roll',0)*(resolution[0]/2)+resolution[1]/2)
        y = int(-rudder.getShipAxis().get('pitch',0)*(resolution[1]/2)+resolution[1]/2)
        pygame.draw.circle(screen, (255,0,255), [x,y], 3)

        #draw joystick data
        ux = int(rudder.getJoyAxis().get('roll')*(resolution[0]/2)+resolution[1]/2)
        uy = int(-rudder.getJoyAxis().get('pitch')*(resolution[1]/2)+resolution[1]/2)
        pygame.draw.circle(screen, (0,255,0), [ux,uy], 10, 3)

        #done
        pygame.display.flip()

except KeyboardInterrupt:
    logging.info('stopping threads')
    rudder.stop = True
    shipThread.join()

logging.info('bye')
