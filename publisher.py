import requests
topics = []
shmids = []
shmsizes = []
url = "http://127.0.01/"

def send_the_topic_to_broker(topic, shmsize):
	r = requests.get( url + topic + "/" + shmsize)
	print(r);
	if ( r[0] == "0"):
		print(r.split(" "))
		return False , None
	elif ( r[0] == "1"):
		shmid = r.split(" ")[1]
		return True , shmid

publish(smids[index] , context)

def make_a_topic(topic, shmsize):
	succeed , shmid = send_the_topic_to_broker(topic , shmsize)
	if ( succeed == TRUE ):
		topics.append(topic)
		shmids.append(shmid)
		shmsizes.append(smhsize)

def publish_to_a_topic(topic, context):
	index = topics.index(topic)
	if (len(context) > shmsizes[index]):
		print("this context is too big for the specified shared memory size : " , shmsizes[index])
	publish(shmids[index] , context)
	
make a topic("ellection" , "1024")
publish_to_a_topic("ellection" , "trump won the ellection")
	

