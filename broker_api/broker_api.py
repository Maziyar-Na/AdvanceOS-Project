import sysv_ipc
import json
from flask import Flask
import random 

max_key = 10000

app = Flask(__name__)

#create shared memory
#save shmid, topic name 
#returns shmid
@app.route("/createTopic/<string:topicName>/<int:shmSize>")
def createTopic(topicName, shmSize):
  key = random.randint(0, max_key)
  try:
    sysv_ipc.SharedMemory(key, sysv_ipc.IPC_CREAT, 0666, shmSize, ' ') 
  except:
     error_msg = "Could not create shm because ...\n"
     return str(0) + " " + error_msg
  #write_into_kvs(shmid, size, topic)
  return "1" + " " + str(key)

#registers subscriber at topic in kv store
@app.route("/subsTopic/<string:topicName>/<string:clientID>")
def subsTopic(topicName, clientID):
  pass

#deletes shared memory
#deletes related data in kv store
@app.route("/delTopic/<string:topicName>")
def delTopic(topicName):
  pass

#lists current topics. who is the publiser, subscribers
@app.route("/listTopics/")
def listTopics():
  pass

#gets insformation about a specific topic
@app.route("/getTopic/<string:topicName>")
def getTopic():
  pass


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
