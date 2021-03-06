# ntil

This is a DCOS demo app, a simple event counter that watches out for a topic on Twitter as well.

## Deployments

In all scenarios below, we will use [Marathon](https://mesosphere.github.io/marathon/) to deploy the ntil app. Also note that I'm using [HTTPie](http://httpie.org/) here in the example, but you can achieve similar results using `curl`. All deployments are based on the Docker image [mhausenblas/ntil](https://registry.hub.docker.com/u/mhausenblas/ntil/).

In order for the Twitter watch part to work you'll need to supply your Twitter credentials. You can obtain those from creating a Twitter application via [apps.twitter.com](https://apps.twitter.com/).

### Playa Mesos

Ramp up your [playa-mesos](https://github.com/mesosphere/playa-mesos) sandbox, log in and get the ntil app:

    $ vagrant up
    $ vagrant ssh
    $ git clone https://github.com/mhausenblas/ntil.git
    $ cd ntil

If you do a Docker deployment on Marathon the first time, now would be a good time to read [Running Docker Containers on Marathon](https://mesosphere.github.io/marathon/docs/native-docker.html). In a nutshell: make sure Docker is installed and containerizer enabled.

You can test ntil in Docker directly, inside the Playa sandbox, using `docker run -d mhausenblas/ntil:latest` and once the container is launched—you may want to check with `docker ps` (and `docker kill`/`docker rm` respectively afterwards)—you should be able to access the app through pointing your browser to http://localhost:9889/ where the UI is or via the following API commands:

    $ http http://localhost:9889/service/target
    $ http http://localhost:9889/service/topic

Now you're ready to deploy ntil via the Marathon HTTP API, again using the same Docker image from above:

    $ http POST http://10.141.141.10:8080/v2/apps < ntil-app-playa.json
    $ http GET http://10.141.141.10:8080/v2/apps/ntil
    $ http DELETE http://10.141.141.10:8080/v2/apps/ntil

Note that in order for the Twitter watch integration to work, you will have to provide your own Twitter credentials by editing `ntil-app-playa.json`:

    $ cat ntil-app-playa.json
    {
        "id": "ntil",
        "instances": 1,
        "cpus": 1,
        "mem": 100,
        "container": {
            "type": "DOCKER",
            "docker": {
                "image": "mhausenblas/ntil:latest"
            }
        },
        "args": ["-e", "2015-04-28T17:00:00", "-t", "mesos", "-k", "10ad9...", "-s", "a2cd...", "-a", "0ghs...", "-o", "hf95..." ]
    }

Using the following parameters from your app definition at [apps.twitter.com](https://apps.twitter.com/):

* `-k` ... Consumer Key (API Key)
* `-s` ... Consumer Secret (API Secret)
* `-a` ... Access Token
* `-o` ... Access Token Secret

Another note concerning the build process (which should not effect you in normal operation): I sometimes had issues (cache? GC? timeout?) with the Docker image not being up-to-date. The following helped (inside the Playa sandbox):

    $ docker pull
    $ sudo stop mesos-slave
    $ sudo start mesos-slave

### AWS

I assume that you have the [DCOS](https://mesosphere.com/product/) EA or PB version installed, which comes with Marathon pre-installed.

So now it's time to log into a cluster instance and install and deploy ntil:

    $ ssh -i ~/.ssh/mesosphere.pem core@ec2-52-17-39-227.eu-west-1.compute.amazonaws.com
    $ git clone https://github.com/mhausenblas/ntil.git
    $ cd ntil
    $ alias http='docker run -i --rm --net=host clue/httpie'
    $ cp ntil-app-aws.json my-ntil-app-aws.json
    $ vi my-ntil-app-aws.json # edit to include your Twitter credentials
    $ http POST http://ec2-52-17-39-227.eu-west-1.compute.amazonaws.com:8080/v2/apps < my-ntil-app-aws.json

Now, have a look in the Marathon UI:

![AWS deployment: Marathon UI](doc/aws-marathon-deployment.png)

In my case, Mesos has placed the app on instance `ec2-52-17-218-139.eu-west-1.compute.amazonaws.com` (ignore the randomly assigned port `10000`).
Use the FQDN you find here and replace the port with `9889` (ntils default service port) and you're done:

![AWS deployment: ntil](doc/aws-ntil.png)

