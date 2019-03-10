## Second Attempt

We'll now be enabling communication between 2 envoy proxies as shown below:

```
+------+      +------------+      +------------+      +------+
|client|----->|client-proxy|----->|server-proxy|----->|server|
+------+      +------------+      +------------+      +------+
```

With the additional server-proxy, we need to start using some conventions with regards to the proxy configs to make them manageable. Using the convention at Lyft we say:

* Use port 9001 for egress
* Use port 9211 for ingress

With these in mind, our traffic flow is now:
client -> client-proxy:9001 -> server-proxy:9211 -> server:8080

### Verifying the setup

Run `docker-compose up` then exec into the client container and run `curl client-proxy:9901`.

We then verify the flow by way of the following stats:

* `http.egress_http.downstream_rq_2xx` ([client-proxy](http://localhost:8001/stats))
* `http.ingress_http.downstream_rq_2xx` ([server-proxy](http://localhost:8002/stats))
