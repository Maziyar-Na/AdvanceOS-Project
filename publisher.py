import requests
import sysv_ipc

topics = []
keys = []
shmsizes = []
msgsizes = []
msgnumbers =[]
url = "http://127.0.01/"

def send_the_topic_to_broker(topic, shmsize , msgsize):
	r = requests.get( url + topic + "/" + shmsize + "/" + Msgsize)
	print(r);
	if ( r[0] == "0"):
		print(r.split(" ")[1])
		return False , None
	elif ( r[0] == "1"):
		key = r.split(" ")[1]
		return True , key

def publish(key , context , offset):
	shm =  sysv_ipc.SharedMemory(key)
	shm.attach()
	shmem.write(key, context, offset)
	

def make_a_topic(topic, shmsize , msgsize):
	succeed , key = send_the_topic_to_broker(topic , shmsize, msgsize)
	if ( succeed == TRUE ):
		topics.append(topic)
		keys.append(key)
		shmsizes.append(smhsize)
		msgsizes.append(msgsize)
		msgnumbers.append(0)

def publish_to_a_topic(topic, context):
	index = topics.index(topic)
	if (len(context) > msgsizes[index]):
		print("this context is too big for the specified message size : " , msgsizes[index])
	elif ( msgnumbers[index] * msgsizes[index] >= shmsizes[index])
		msgnumbers[index] = 0
		publish(keys[index] , context , msgnumbers[index] * msgsizes[index])
	else
		publish(keys[index] , context , msgnumbers[index] * msgsizes[index])
		msgnumbers[index] = msgnumbers[index] + 1
	
make a topic("ellection" , "1024" , "128")
publish_to_a_topic("ellection" , "trump won the ellection")
	

