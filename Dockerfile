FROM libmesos/ubuntu
MAINTAINER Michael Hausenblas "michael.hausenblas@gmail.com"
ENV REFRESHED_AT 2015-04-27T21:28:00

WORKDIR /opt
RUN wget https://github.com/mhausenblas/ntil/archive/master.zip
RUN unzip master.zip
RUN pip install TwitterSearch
WORKDIR /opt/ntil-master
EXPOSE 9889
ENTRYPOINT ["python", "ntil-server.py"]
CMD ["-e", "2015-05-15T17:00:00", "-t", "dcos"]
