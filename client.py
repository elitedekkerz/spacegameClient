#!/usr/bin/python3
import socket
import time
import logging

class gameVar():
      value = ''
      baseArgs = ['']

      def __init__(self, client, baseArgs=['']):
         self.baseArgs = baseArgs
         self.client = client

      def parse(self, value):
         return self.client.send(self.baseArgs+value)

class client():
   name = 'Yuri'
   ship = 'Восток'
   def __init__(self, address='localhost', name='Robbit', ship='Восток'):
      #attempt to connect to given socket
      self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
      self.sock.setblocking(0)
      try:
         self.sock.connect((address,1961))
      except:
         logging.error('unable to connect to server: %s',address)

      #set name
      self.name = name
      self.send(['config','name']+[self.name])
      print("set name to: "+name)

      #join ship
      self.ship = ship
      if 'joined' not in self.send(['config','ship','join']+[ship], timeout=1):
         self.send(['config', 'ship', 'name']+[ship])
      print("joined ship: "+ship)

   #send arguments and wait for a reply
   def send(self, args=['help'], timeout = None):
      if timeout:
         logging.debug('send will timeout in %ss', str(timeout))
         startTime = time.time()

      #set expectation of prompt from server
      self.prompt = '\n'+self.name+'@'+self.ship+':'

      #join arguments to a single string
      message = str.join(' ', args)+'\n'

      #send message
      self.sock.send(message.encode('utf-8'))

      #wait for prompt in reply from server
      data = ''
      while self.prompt != data[-len(self.prompt):]:
         try:
            d = self.sock.recv(1024).decode('utf-8')
            data += d
         except BlockingIOError:
            time.sleep(0.01)
            if timeout and startTime+timeout < time.time():
               logging.warning("communication timed out: %s", repr(data))
               return data
      logging.debug(repr(data))
      return data[:-len(self.prompt)]

   def close(self):
      self.sock.send('bye\n'.encode('utf-8'))
      self.sock.close()

   def gameVariable(self, args):
      return gameVar(self, args)

if __name__ == "__main__":
   import sys
   a = sys.argv
   try:
      c = client()
   except:
      logging.exception('unable to create client')
      quit()
   radio = c.gameVariable(['radio'])
   print(radio.parse(['get']))
   c.send(['bye'],timeout=1)
   c.close()
