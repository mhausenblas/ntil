FROM libmesos/ubuntu
MAINTAINER Michael Hausenblas "michael.hausenblas@gmail.com"
ENV REFRESHED_AT 2015-04-27T14:22:00

WORKDIR /opt
RUN wget https://github.com/mhausenblas/ntil/archive/master.zip
RUN unzip master.zip
EXPOSE 9889
ENTRYPOINT ["python", "ntil-master/ntil-server.py"]
CMD ["-e", "2015-05-15T17:00:00", "-t", "dcos"]
