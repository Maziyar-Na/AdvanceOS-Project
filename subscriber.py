import redis
import sysv_ipc

def read_from_topic(key, shmsize):
	shm =  sysv_ipc.SharedMemory(key)
	shm.attach()
	shmem.read(shmsize, 0)

def get_the_info_for_a_topic(topic):
	r = redis.Redis(
		host= 'localhost' ,
		port=6379,
		password='')
	return r.lindex(topic , 0) , r.lindex(topic , 1)

def read_topic("ellection"):
	key , shmsize = get_the_info_for_a_topic("ellection")
	if (key and shmsize):
		read_from_topic(key , shmsize)

read_topic("ellection")
