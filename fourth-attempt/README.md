## Fourth Attempt

In this iteration, we'll now form an actual "mesh" between 3 services illustrated below:

```
                                                  +---------------+     +---------+
                                              --->|service-b-proxy|<--->|service-b|
                                      -------/    +---------------+     +---------+
+---------+     +---------------+<---/                   ^
|service-a|<--->|service-a-proxy|                        |
+---------+     +---------------+<---\                   v
                                      -------\    +---------------+     +---------+
                                              --->|service-c-proxy|<--->|service-c|
                                                  +---------------+     +---------+
```

As per our convention, each service will have 1 ingress talking to the "local service" and 1 egress with virtual hosts to the other services.

### Verifying the setup

Run `docker-compose up` and you may now exec into any of the services running and run the following:

`curl -v -H 'Host: service-$TARGET_SERVICE' service-$CURRENT_SERVICE-proxy:9001`

Example:

`curl -v -H 'Host: service-a' service-b-proxy:9001`

translated as Service B calling Service A

Verification method (stats etc) is the same as the previous setup
