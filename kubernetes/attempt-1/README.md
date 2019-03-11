## First Attempt

We'll now be moving our setup to Kubernetes as our orchestration layer. We'll stick with the simple attempt first just to make sure everything is still working correctly, shown below:

```
+----------+       +---------+       +----------+
| +------+ |       | +-----+ |       | +------+ |
| |client| |------>| |proxy| |------>| |server| |
| +------+ |       | +-----+ |       | +------+ |
+----------+       +---------+       +----------+
```

### Verifying the setup

To run the setup, simply do `kubectl apply -f manifests/` then `kubectl exec -it client sh`. Once inside the container, get the IP of the `proxy` pod then do `curl -v IP_OF_PROXY:9001`.

You can also follow the logs of the `server` pod to see whether the request went through.

Do `kubectl delete -f manifests/` to clean up after the resources we created.
