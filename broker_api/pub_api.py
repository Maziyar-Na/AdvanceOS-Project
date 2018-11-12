import sysv_ipc
import json
import pycurl
from StringIO import StringIO



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
  shm.remove()
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
  c.setopt(c.WRITEDATA, buffer
  c.perform()
  c.close()
  body = buffer.getvalue()
  shmid = int(body.split(" ")[0])
  shmSize = int(body.split(" ")[1])
  msgSize = int(body.split(" ")[2])
  shmem = sysv_ipc.SharedMemory(shmid)
  return shmem, shmSize, msgSize  

    
  #Ex for publishing data
  createTopic('127.0.0.1', 'speed2', 1024, 16)
  pub = initTopic('127.0.0.1', 'speed2')
  shmem = pub[0]
  shmSize = pub[1]
  msgSize = pub[2]
  offset = 0;
  data = "Hello World"
  while True:
   shmem.write(data, offset)
   offset = (offset + msgSize) % shmSize 
