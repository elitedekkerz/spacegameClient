#!/usr/bin/env python3
import client
import logging
import pygame
from pygame.locals import *
import time
import sys

#prepare pygame display
pygame.init()
pygame.display.init()
resolution = [700,700]
screen = pygame.display.set_mode(resolution)

logging.basicConfig(level = logging.INFO)

cli = client.client(sys.argv[1], 'spaceRudder7800', sys.argv[2])

rudder = cli.gameVariable(['rudder'])

def updateShip(args):
    global rudder
    for key, value in args.items():
        rudder.parse([key,str(value)])

while True:
    pygame.event.get()
    pygame.mouse.set_pos([resolution[0]/2,resolution[1]/2])

    #draw background
    screen.fill((0,0,0))
    pygame.draw.line(screen, (0,0,255), [0, resolution[1]/2], [resolution[0],resolution[1]/2], 1)
    pygame.draw.line(screen, (0,0,255), [resolution[0]/2,0], [resolution[0]/2,resolution[1]], 1)

    #get user input
    x, y = pygame.mouse.get_pos()
    userAxis = {
        'yaw':(x-resolution[0]/2)/resolution[0],
        'pitch':-(y-resolution[1]/2)/resolution[1],
    }
    
    #send ship input
    updateShip(userAxis)

    #get ship status
    shipAxis = {}
    for axis in rudder.parse(['get']).message.split(','):
        a = axis.split(':')
        shipAxis[a[0].strip()] = float(a[1].strip())

    #draw ship data
    x = int(shipAxis.get('yaw')*(resolution[0]/2)+resolution[1]/2)
    y = int(-shipAxis.get('pitch')*(resolution[1]/2)+resolution[1]/2)
    pygame.draw.circle(screen, (255,255,255), [x,y],10)

    #done
    pygame.display.flip()
    logging.info(repr(shipAxis))
