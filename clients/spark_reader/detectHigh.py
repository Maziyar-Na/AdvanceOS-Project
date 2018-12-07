import sysv_ipc
import json
import pycurl
from StringIO import StringIO
from pyspark import SparkContext

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
  # More work need to be done here (subscriber implementation). E.g. prevet subscriber from skipping data and also from reading same data more than once.i
  # Another problem here: if there is not enough data to fill the window size, this function will never return. Maybe we need a timeout.
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
      #data=data.split(",")
      data_stream.append(int(data)/10)
    offset = (offset + msgSize) % shmSize
    count += 1
  return data_stream, offset

def detectHigh(sc, data_stream, maximum):
  rdd=sc.parallelize(data_stream)
  values = rdd.filter(lambda x: x > maximum).collect()
  if len(values) > 0:
    print "Warning: " + str(len(values)) + " values above " + str(maximum) + " were detected in this window."


#while True:
def main():
  #init_spark
  sc = SparkContext("local", "detectHigh","localhost") 

  #init shm
  subs = subsTopic("192.168.0.11", "numbers", "c1")
  shmem = subs[0]
  shmSize = subs[1]
  msgSize = subs[2]
  offset = 0;
  window_size = 10000
  maximum = 9998
  total_processed = 0
  while True:
    #thread to prevent blocking when reading?
    res = get_data(offset, window_size, shmem, shmSize, msgSize)
    data_stream = res[0]
    #update offset to continue reading where it stopped
    offset = res[1]
    if len(data_stream) > 0:
      detectHigh(sc, data_stream, maximum)
      total_processed += window_size
    print "Total entries processed: " + str(total_processed)

main()
  

