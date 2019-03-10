## First Attempt

For our first attempt, we'll simulate the following flow with `docker-compose`:

```
+------+      +-----+      +------+
|client|----->|proxy|----->|server|
+------+      +-----+      +------+
```

with our proxy having a listener at `0.0.0.0:9000` being routed to `server:8080`

### Verifying the setup

To verify whether the proxy works, simply run `docker-compose up` and exec into the client container once everything is up then just run `curl -v proxy:9000`.


You can also go to [here](http://localhost:8001/) on your host machine to see the admin page of the proxy.

### Relevant Links
* [Service Mesh with Envoy 101](https://hackernoon.com/service-mesh-with-envoy-101-e6b2131ee30b)
* [Getting started with Lyft Envoy for microservices resilience](https://www.datawire.io/envoyproxy/getting-started-lyft-envoy-microservices-resilience/)


[Home](https://github.com/teh-username/service-mesh-the-hard-way) [Next](https://github.com/teh-username/service-mesh-the-hard-way/tree/master/second-attempt)
