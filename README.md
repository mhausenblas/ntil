# ntil

This is a DCOS demo app, a simple event counter that watches out for a topic on Twitter as well.

## Deployments

I will assume that you have the [DCOS](https://mesosphere.com/product/) installed. We will use Marathon to deploy the ntil app.
Note that I'm using [HTTPie](http://httpie.org/) here in the example, but you can achieve similar results using `curl`.

### Playa Mesos

Ramp up your [playa-mesos](https://github.com/mesosphere/playa-mesos) sandbox, log in and get the ntil app:

    $ vagrant up
    $ vagrant ssh
    $ git clone https://github.com/mhausenblas/ntil.git
    $ cd ntil

If you do a Docker deployment on Marathon the first time, now would be a good time to read [Running Docker Containers on Marathon](https://mesosphere.github.io/marathon/docs/native-docker.html). In a nutshell: make sure Docker is installed and containerizer enabled.

Test ntil in Docker directly (inside the Playa sandbox):

    $ docker run -d --net=host --name ntil-test -p 127.0.0.1:9889:9889 -v "$PWD":/usr/ntil -w /usr/ntil python:2.7 python ntil-server.py -e 2015-05-15T17:00:00 -t dcos

After the above docker container is launched (check with `docker ps`) you should be able to access the app through pointing your browser to http://localhost:9889/

Now, deploy ntil app via the Marathon HTTP API:

    $ http POST http://10.141.141.10:8080/v2/apps < ntil-app.json


### AWS




## To do

- [x]  CLI params: target event as timestamp in ISO8601 format, #topic
- [x]  Marathon deployment https://mesosphere.github.io/marathon/docs/application-basics.html
- [x]  Test in playa
- [ ]  Twitter integration for updates https://github.com/ckoepp/TwitterSearch 
- [ ]  AWS setup
