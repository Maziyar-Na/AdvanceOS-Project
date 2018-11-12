import sysv_ipc
import json
import pycurl
from StringIO import StringIO



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


#Ex for rading data
subs = subsTopic("127.0.0.1", "speed2", "c1")
shmem = subs[0]
shmSize = subs[1]
msgSize = subs[2]
offset = 0;

while True:
  mem_data = shmem.read(msgSize, offset)
  find_data=mem_data.find('\0')
  data=mem_data[:find_data]
  if data != "":
    print data
  offset = (offset + msgSize) % shmSize    
