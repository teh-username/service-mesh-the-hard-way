## Fifth Attempt

```
+-----------+               +-----------+
|+---------+|               |+---------+|
||service-a||               ||service-c||
|+---------+|               |+---------+|
|+-----+    |<------------->|+-----+    |
||proxy|    |               ||proxy|    |
|+-----+    |               |+-----+    |
+-----------+               +-----------+
     ^                             ^
     |                             |
     |                             |
     |        +-----------+        |
     |        |+---------+|        |
     |        ||service-b||        |
     |        |+---------+|        |
     +------->|+-----+    |--------+
              ||proxy|    |
              |+-----+    |
              +-----------+
```

* Initiate a request in service-a that flows to all the services (chained calls)
* Prove bi-directional calls to all services
* Improved naming convention, taking into consideration multiple ports


## Verification

Run `kubectl port-forward service-a 8080:9211` then `curl 'http://localhost:8080/service?flow=abcabcbcbca'`.

For each service, take a look at the following stats and corresponding service log count:
* `listener.0.0.0.0_9001.http.egress_http.downstream_rq_2xx:` <-> "Requesting: ..."
* `listener.0.0.0.0_9211.http.ingress_http.downstream_rq_2xx:` <-> "Hello from service x"

### Relevant Links

* [Understanding How Envoy Sidecar Intercept and Route Traffic in Istio Service Mesh](https://jimmysong.io/posts/understanding-how-envoy-sidecar-intercept-and-route-traffic-in-istio-service-mesh/)
