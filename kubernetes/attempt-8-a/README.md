## Eight Attempt (1/2)

```
+----------------------+
|     +----------+     |                                         +---------+
|     |xds-server|     |                                    +----|service-a|
|     +----------+     |                                    |    +---------+
|          ^           |             +--------------+       |    +---------+
|          |           |           ->|kube-apiserver|<-----------|service-b|
|          |           |       ---/  +--------------+       |    +---------+
| +------------------+ |   ---/                             |    +---------+
| |service-controller| |<-/                                 +----|service-c|
| +------------------+ |                                         +---------+
+----------------------+
```

For this attempt, we accomplish the following:

* Create a Kubernetes controller that listens to new services and pushes service updates to the xds-server

* Update xds-server implementation to accept updates from the controller and dynamically update route and cluster inventory

Pulling of the route and cluster inventories from the xds-server will be tackled on the second installment of this attempt.

## Verification

Run attempt-5 setup for dummy services `kubectl apply -f ../attempt-5/manifests/` then apply manifest for this attempt `kubectl apply -f manifests/`. Port forward to the xds-server `kubectl port-forward control-plane 8080:7001` then visit the included debugging route at `http://localhost:8080/debug`.

## Todos:

* Support modify and delete actions for services
* Add EDS and watcher for the Endpoint object

### Relevant Links

* (Kubernetes Python Client)[https://github.com/kubernetes-client/python]
