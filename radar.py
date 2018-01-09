#!/usr/bin/python3
import pygame
import time
import logging
import sys
import math
from pygame.locals import *
import SDClient

logging.basicConfig(level=logging.INFO)

#prepare pygame display
pygame.init()
pygame.display.init()
resolution = [700,700]
screen = pygame.display.set_mode(resolution)
font = pygame.font.Font(None, 15)
frameRate = 10

#setup client for server
cli = SDClient.client(sys.argv[1], 'radarBot', sys.argv[2])
radar = cli.gameVariable(['radar'])
#radar.parse(['on'])

while True:
   frameStart = time.time()
   screen.fill((0,0,0))

   #try to scan
   sector = float(radar.parse(['sector']).message)

   #draw guidelines
   pygame.draw.line(screen, (0,0,255), [0, resolution[1]/2], [resolution[0],resolution[1]/2], 1)
   pygame.draw.line(screen, (0,0,255), [resolution[0]/2,0], [resolution[0]/2,resolution[1]], 1)
   #draw 90 degree guideline
   x = int((sector - 90)/180 * resolution[0]/2)
   y = int((sector - 90)/180 * resolution[1]/2)
   pygame.draw.ellipse(screen, (0,255,0), [x, y, resolution[0]-2*x, resolution[1]-2*y], 1)
   items = []

   #attempt to scan
   scan = radar.parse(['scan'])
   if scan.status != 'Ok':
      #ensure radar is on
      radarOn = radar.parse(['on'])
      if radarOn.status != 'Ok':
         logging.error('unable to turn on radar')
         time.sleep(1)
      continue

   #process results
   for line in scan.message.split('\n'):
      if line == '':
         break
      line = line.split()
      obj = {
         'name':line[0].strip(':'),
         'range':float(line[1]),
         'pitch':float(line[3]),
         'yaw':float(line[2]),
      }
      scale = [resolution[0]/360,resolution[1]/360]
      x=int(resolution[0]/2+(obj['yaw']/sector)*resolution[0]/2)
      y=int(resolution[1]/2+(obj['pitch']/sector)*resolution[1]/2)
      pygame.draw.circle(screen, (255,255,255), [x,y],1+int(10000/obj['range']))
      text = font.render(obj['name'], 0, (255,255,255))
      screen.blit(text,(x+5,y+5))
      text = font.render(str(obj['range']), 0, (255,255,255))
      screen.blit(text,(x+5,y+15))
   pygame.display.flip()
   try:
      time.sleep(1/frameRate -time.time() - frameStart)
   except ValueError:
      pass

pygame.quit()
