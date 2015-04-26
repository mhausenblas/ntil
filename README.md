# ntil

This is a DCOS demo app, a simple event counter that watches out for a topic on Twitter as well.


## Usage

### Deploy

I will assume that you have a running version of the DCOS. We will use Marathon to deploy the ntil app.
Note that I'm using [HTTPie](http://httpie.org/) here in the example, but you can achieve similar results using `curl`.

Deploy on local [playa-mesos](https://github.com/mesosphere/playa-mesos) sandbox:

    $ http POST http://10.141.141.10:8080/v2/apps < ntil-app.json


## To do

- [x]  CLI params: target event as timestamp in ISO8601 format, #topic
- [ ]  Marathon deployment https://mesosphere.github.io/marathon/docs/application-basics.html
- [ ]  Test in playa
- [ ]  Twitter integration for updates https://github.com/ckoepp/TwitterSearch 
- [ ]  AWS setup
