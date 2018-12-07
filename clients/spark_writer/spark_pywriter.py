import sysv_ipc
import json
import pycurl
from StringIO import StringIO
import random

#Program to generate data to send to a spark app that can detect numbers greater than a specific threshold


def createTopic(brokerAddr, topicName, shmSize, msgSize):
  buffer = StringIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(5000) + '/createTopic/' + topicName + '/' + str(shmSize) + '/' + str(msgSize)
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue()
  if body.split(" ")[0] == '1':
    return int(body.split(" ")[1])
  else:
    return 0

def getShmId(brokerAddr, topicName):
  buffer = StringIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(5000) + '/getTopic/' + topicName
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue()
  return int(body.split(" ")[0])
 

def delTopic(brokerAddr, topicName):
  shmid = getShmId(brokerAddr, topicName)
  shm =  sysv_ipc.SharedMemory(shmid)
  shm.detach()
  buffer = StringIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(5000) + '/delTopic/' + topicName
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue()
  if body == '1':
    return 1
  else:
    return 0


def initTopic(brokerAddr, topicName):
  buffer = StringIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(5000) + '/getTopic/' + topicName
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue()
  shmid = int(body.split(" ")[0])
  shmSize = int(body.split(" ")[1])
  msgSize = int(body.split(" ")[2])
  shmem = sysv_ipc.SharedMemory(shmid)
  return shmem, shmSize, msgSize  

#returns tupple with shmem,  
def subsTopic(brokerAddr, topicName, clientID):
  buffer = StringIO()
  c = pycurl.Curl()
  url = 'http://' + brokerAddr + ':' + str(5000) + '/subsTopic/' + topicName + '/' + clientID
  c.setopt(c.URL, url)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue()
  if body.split(" ")[0] == '1':
    shmid = int(body.split(" ")[1])
    shmSize = int(body.split(" ")[2])
    msgSize = int(body.split(" ")[3])
    shmem = sysv_ipc.SharedMemory(shmid)
    return shmem, shmSize, msgSize
  else:
    return 0,0,0



def main():
  createTopic('10.0.2.15', 'xor', 1024, 16)
  pub = initTopic('10.0.2.15', 'xor')
  shmem = pub[0]
  shmSize = pub[1]
  msgSize = pub[2]
  offset = 0
  #data = "Hello World"
#  i = 0
  while True:
#  while i < 1000:
#    data = str(i)
#    data=str(random.randint(0,1)) + "," + str(random.randint(0,1))
    data=str(random.randint(0,10000))
    print data
    shmem.write(data, offset)
    offset = (offset + msgSize) % shmSize    
#    i += 1
#	   data = data + str(i)
  return 0
main()
#memory = sysv_ipc.SharedMemory(123456)


#while True:
#  memory_value = memory.read()
#  i=memory_value.find('\0')
#  data=memory_value[:i]
#  print data

#memory.detach()

#memory.remove()
#print len(memory_value) 
