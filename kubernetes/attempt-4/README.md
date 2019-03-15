## Fourth Attempt

```
+----------+
| +------+ |
| |server| |            +----------+
| +------+ |            | +------+ |
| +-----+  |<-----------| |client| |
| |proxy|  |            | +------+ |
| +-----+  |            +----------+
+----------+
```

TBD

* iptables should now proxy incoming requests to the service as well

### Verification

`kubectl port-forward server 8001:8001`
`listener.0.0.0.0_9211.http.ingress_http.downstream_rq_2xx`
