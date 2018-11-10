import redis

def write_into_kvs(shmid, size, topic):
	r = redis.Redis(
		host='localhost',
		port=6379,
		password='')
	r.rpush(topic, shmid, size)
	for i in range(0,r.llen(topic)):
	 	print "[dbg] the list created: ", r.lindex(topic, i)


#write_into_kvs(2, 20, "mobile")
#write_into_kvs(3, 40, "radar")

