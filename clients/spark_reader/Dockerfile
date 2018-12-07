FROM ubuntu:bionic
RUN apt-get update
RUN apt-get install -y  python-pip
RUN pip install sysv_ipc
RUN apt-get install -y python-pycurl
RUN apt-get install -y openjdk-11-jre
RUN apt-get install -y wget
RUN wget http://apache.claz.org/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
RUN tar xzvf spark-2.4.0-bin-hadoop2.7.tgz
RUN mkdir -p /spark-2.4.0-bin-hadoop2.7/app
COPY detectHigh.py /spark-2.4.0-bin-hadoop2.7/app/ 
COPY log4j.properties /spark-2.4.0-bin-hadoop2.7/conf/
#CMD spark-2.4.0-bin-hadoop2.7/bin/spark-submit spark-2.4.0-bin-hadoop2.7/app/detectHigh.py
