## Third Attempt

```
+----------+
| +------+ |
| |client| |            +----------+
| +------+ |            | +------+ |
| +-----+  |----------->| |server| |
| |proxy|  |            | +------+ |
| +-----+  |            +----------+
+----------+
```

TBD

* Interaction between client and proxy is now implicit via iptables (`curl -v http://server:8080`)

### Relevant Links

* [istio-iptables.sh](https://github.com/istio/istio/blob/master/tools/deb/istio-iptables.sh)
* [K8 Istio little Deep Dive](https://hackernoon.com/k8-istio-deep-dive-c0773a204e82)
* [An In-Depth Guide to iptables, the Linux Firewall](https://www.booleanworld.com/depth-guide-iptables-linux-firewall/)
