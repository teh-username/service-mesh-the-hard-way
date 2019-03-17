## Sixth Attempt

```
+-----------+
|+---------+|
||service-a||           +----------+
|+---------+|       --->|xds-server|
|+-----+    -------/    +----------+
||proxy|<--/|
|+-----+    |
+-----------+
```

* Implementing a simple XDS server that responds to CDS requests

Discovery Request:
```
{
    'version_info': '0',
    'node': {
        'id': 'id-service-a',
        'cluster': 'cluster-service-a',
        'build_version': '628d1668d7dc9244e3a8fa3d3fbabca23e92e23d/1.10.0-dev/Clean/RELEASE/BoringSSL'
    }
}
```

Discovery Response:
```
{
    'version_info': '0',
    'resources': [
        {
            '@type': 'type.googleapis.com/envoy.api.v2.Cluster',
            'name': 'local_service',
            'connect_timeout': '0.25s',
            'type': 'strict_dns',
            'lb_policy': 'round_robin',
            'load_assignment': {
                'cluster_name': 'local_service',
                'endpoints': [
                    {
                        'lb_endpoints': [
                            {
                                'endpoint': {
                                    'address': {
                                        'socket_address': {
                                            'address': '127.0.0.1',
                                            'port_value': '8080'
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```

## Verification

Run `kubectl port-forward service-a 8081:8001` and go to `http://localhost:8081/clusters`. You should see the `local_service` cluster along with `local_service::added_via_api::true`.


### Relevant Links

* [Guidance for Building a Control Plane to Manage Envoy Proxy at the edge, as a gateway, or in a mesh](https://medium.com/solo-io/guidance-for-building-a-control-plane-to-manage-envoy-proxy-at-the-edge-as-a-gateway-or-in-a-mesh-badb6c36a2af)
* [Envoy Bootstrap configuration](https://www.envoyproxy.io/docs/envoy/latest/configuration/overview/v2_overview#bootstrap-configuration)
* [proto3 JSON mapping](https://developers.google.com/protocol-buffers/docs/proto3#json)
* [xDS REST and gRPC protocol](https://github.com/envoyproxy/data-plane-api/blob/master/XDS_PROTOCOL.md#rest-json-polling-subscriptions)
* [Common discovery API components](https://www.envoyproxy.io/docs/envoy/latest/api-v2/api/v2/discovery.proto#)
