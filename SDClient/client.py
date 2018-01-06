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
         reply = self.client.send(self.baseArgs+value)
         return message(value, reply[0], str.join('\n',reply[1:]))

class message():
   def __init__(self,command, status, message):
      self.command = command
      self.status = status
      self.message = message

class client():
   name = 'Yuri'
   ship = 'Восток'
   def __init__(self, address='localhost', name='Robbit', ship=''):
      #attempt to connect to given socket
      self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
      logging.debug('connecting to %s:%s',address, "1961")
      try:
         self.sock.connect((address,1961))
      except:
         logging.exception('unable to connect to server: %s',address)
      logging.debug('connected')
      self.sock.setblocking(0)

      #set name
      self.name = name
      self.prompt = '\n'+self.name+'>'
      self.send(['name', self.name])
      logging.debug("set name to: "+name)

      #join ship
      self.ship = ship
      self.prompt = '\n'+self.name+'@'+self.ship+'>'
      self.send(['join', ship])
      logging.debug("joined ship: "+ship)
      #set expectation of prompt from server

   #send arguments and wait for a reply
   def send(self, args=['help'], timeout = None):
      logging.debug("sending %s",args)
      if timeout:
         logging.debug('send will timeout in %ss', str(timeout))
         startTime = time.time()


      #join arguments to a single string
      message = str.join(' ', args)+'\n'

      #send message
      self.sock.send(message.encode('utf-8'))

      #wait for prompt in reply from server
      data = ''
      logging.debug('waiting for %s', repr(self.prompt))
      while self.prompt != data[-len(self.prompt):]:
         try:
            d = self.sock.recv(1024).decode('utf-8')
            data += d
            logging.debug('%s',repr(d))
         except BlockingIOError:
            time.sleep(0.01)
            if timeout and startTime+timeout < time.time():
               logging.warning("communication timed out: %s", repr(data))
               break
      output = data.split('\n')[:-1]
      logging.debug('received %s', repr(output))
      return output

   def close(self):
      self.sock.send('bye\n'.encode('utf-8'))
      self.sock.close()

   def gameVariable(self, args):
      return gameVar(self, args)

if __name__ == "__main__":
   import sys
   logging.basicConfig(level=logging.INFO)
   a = sys.argv
   try:
      c = client()
   except:
      logging.exception('unable to create client')
      quit()
   radio = c.gameVariable(['radio'])
   logging.info(radio.parse(['get']).message)
   c.send(['disconnect'],timeout=1)
   c.close()
