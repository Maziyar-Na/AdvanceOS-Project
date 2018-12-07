FROM ubuntu:bionic
RUN apt-get update
RUN apt-get install -y  python-pip
RUN pip install keras
RUN pip install --upgrade pip
RUN pip install tensorflow
RUN pip install sysv_ipc
RUN apt-get install -y python-pycurl
COPY spark_pywriter.py /
#CMD ["python","/pywriter.py"] 
