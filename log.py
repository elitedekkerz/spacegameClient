#!/usr/bin/python3
import client
import sys
import time

logging.basicConfig(level=logging.WARNING)

#setup client for server
cli = client.client(sys.argv[1], 'logBot', sys.argv[2])
log = cli.gameVariable(['log'])

lastLog=''
#spam "log read" until told not to
try:
   while True:
      time.sleep(0.3)
      logData = log.parse(['read'])
      #ignore if log appears same
      if lastLog != logData:
         #output only new part of log
         for l in reversed(range(len(logData))):
            if lastLog[-l:] == logData[:l] or l == 0:
               sys.stdout.write(logData[l:])
               sys.stdout.flush()
               #reset log diff and get back to spamming
               lastLog = logData
               break
except KeyboardInterrupt:
   pass
