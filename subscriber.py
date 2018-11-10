import redis

def read_from_topic(shmid, shmsize):
	# I don't know how to read from shared memry

def get_the_info_for_a_topic(topic):
	r = redis.Redis(
		host= 'localhost' ,
		port=6379,
		password='')
	return r.lindex(topic , 0) , r.lindex(topic , 1)

def read_topic("ellection"):
	shmid , shmsize = get_the_info_for_a_topic("ellection")
	if (shmid and shmsize):
		read_from_topic(shmid , shmsize)

read_topic("ellection")