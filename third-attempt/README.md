## Third Attempt

We'll now add another service to our setup as shown below:

```
                                     +---------------+     +---------+
                                   ->|service-a-proxy|---->|service-a|
                                 -/  +---------------+     +---------+
                              --/
+------+      +------------+-/
|client|----->|client-proxy|
+------+      +------------+-\
                              --\
                                 -\  +---------------+     +---------+
                                   ->|service-b-proxy|---->|service-b|
                                     +---------------+     +---------+
```

To materialize the 2 services in client-proxy, we have 2 options:

* Create 2 egress listeners, one for each service
* Stick to 1 egress listener and do routing based on request features

We'll be going with option 2 since that is the cleaner implementation between the two and is less repetitive. To achieve this, we'll simply add the two services as virtual hosts on the single egress listener:

```yml
virtual_hosts:
  - name: service_a
    domains:
      - "service-a"
    routes:
      - match:
          prefix: "/"
        route:
          cluster: service_a
  - name: service_b
    domains:
      - "service-b"
    routes:
      - match:
          prefix: "/"
        route:
          cluster: service_b
```

We simply route the request based on the Host header present on each request.

### Verifying the setup

Run `docker-compose up` then exec into the client container and run the following commands:

* `curl -v -H 'Host: service-a' client-proxy:9001`
* `curl -v -H 'Host: service-b' client-proxy:9001`

You can then check and compare the following stats:

* `http.egress_http.downstream_rq_2xx` and `cluster.service_b.upstream_rq_2xx` ([client-proxy](http://localhost:8001/stats))
* `http.ingress_http.downstream_rq_2xx` ([service-a-proxy](http://localhost:8002/stats))
* `http.ingress_http.downstream_rq_2xx` ([service-b-proxy](http://localhost:8003/stats))

### Routing

To verify that Envoy is correctly routing the requests to either service, you can try editing the cluster of the `service_b` virtual host to `service_a`. Running `curl -v -H 'Host: service-b' client-proxy:9001` should return a response from `service-a`.

### Relevant Links
* [Envoy Service to Service Deployment](https://www.envoyproxy.io/docs/envoy/v1.9.0/intro/deployment_types/service_to_service)
* [Envoy Service to Service Template Example](https://github.com/envoyproxy/envoy/blob/master/configs/envoy_service_to_service_v2.template.yaml)
* [Envoy as a generic forward proxy](https://github.com/vadimeisenbergibm/envoy-generic-forward-proxy)

[Previous](https://github.com/teh-username/service-mesh-the-hard-way/tree/master/second-attempt)
