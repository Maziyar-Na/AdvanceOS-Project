import sysv_ipc
import json
import pycurl
from StringIO import StringIO
from threading import Thread
import numpy as np
from keras.models import Sequential
from keras.layers.core import Activation, Dense
from keras.optimizers import SGD
from keras.models import load_model


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


def get_data(init_off, window_size, shmem, shmSize, msgSize):
  # More work need to be done here (subscriber implementation). E.g. prevet subscriber from skipping data and also from reading same data more than once.
  #I guess the same idea here can be used to expose data to Spark (Get data in batches).
  data_stream=[]
  count = 0
  offset = init_off
  while count <= window_size:
    mem_data = shmem.read(msgSize, offset)
    find_data=mem_data.find('\0')
    data=mem_data[:find_data]
    if (data != ""):
      #We need a schema repository, so that we know how to read the data
      data=data.split(",")
      data_stream.append([int(data[0]), int(data[1])])
    offset = (offset + msgSize) % shmSize
    count += 1
  return data_stream, offset

def predict_xor(model, X, data_stream):
  for i in range(len(data_stream)):
    X[0] = data_stream[i]
    print "Saw: " + str(X[0]) + " " + "predicted: " + str(model.predict_proba(X))


def main():
  #init keras
  X = np.zeros((1, 2), dtype='uint8')
  model = load_model('xor.h5')    

  #init shm
  subs = subsTopic("10.0.2.15", "xor", "c1")
  shmem = subs[0]
  shmSize = subs[1]
  msgSize = subs[2]
  offset = 0;
  window_size = 100
  while True:
    #thread to prevent blocking when reading?
    res = get_data(offset, window_size, shmem, shmSize, msgSize)
    data_stream = res[0]
    #update offset to continue reading where it stopped
    offset = res[1]
    if len(data_stream) > 0:
      predict_xor(model, X, data_stream)

main() 
