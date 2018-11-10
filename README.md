# AdvanceOS-Project

The broker is starting with the command below:

sudo docker run --name broker -d -p 5000:5000 broker

To attach other containers to its namespace we should give docker the following parameter (when starting the container):

--ipc container:shm_writer
