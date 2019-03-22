## Seventh Attempt

```
+-----------+                    +-----------+
|           |<------------------>|           |
|+-----+    |                    |    +-----+|
||proxy|<--------+          +-------->|proxy||
|+-----+    |    |          |    |    +-----+|
|+---------+|    |          |    |+---------+|
||service-a||    |          |    ||service-b||
|+---------+|    +----------+    |+---------+|
+-----------+    |xds-server|    +-----------+
      ^          +----------+          ^
      |               |                |
      |               |                |
      |               |                |
      |         +-----|-----+          |
      |         |     v     |          |
      |         |  +-----+  |          |
      |         |  |proxy|  |          |
      |         |  +-----+  |          |
      +-------->|+---------+|<---------+
                ||service-c||
                |+---------+|
                +-----------+
```

For this attempt, we'll push the "same" config to all services on startup (CDS + RDS) to keep it simple. Then proceed with the attempt-5 setup where in we try to pump traffic to all services involved to verify whether the push was successful.

* stick to 3 services for now, so we can see how we can probably scale it to more services
* build the giant same config to see what can be dynamically repeated
* dynamically tag envoy (node and id) using downward api


## XDS Setup
* Listeners are static
* Routes are dynamic (RDS)
* Clusters are dynamic (CDS)
* Endpoints are static (for now)

How incremental versioning is demonstrated:

* Clusters are updated every 10 seconds, with each new service being added e.g. only `service-a` cluster is available in the first 10 seconds, then `service-b` is added and so on

* Routes are updated every 5 seconds, with the same setup as the CDS e.g. only route to `service-a` is available in the first 5 seconds, then `service-b` is added and so on


Cluster request:

Initial
```
{
    'node': {
        'id': 'service-a-10.1.1.54',
        'cluster': 'service-a',
        'build_version': '3ba949a9cb5b0b1cccd61e76159969a49377fd7d/1.10.0-dev/Clean/RELEASE/BoringSSL'
    }
}
```

Succeeding
```
{
    'version_info': '0',
    'node': {
        'id': 'service-a-10.1.1.54',
        'cluster': 'service-a',
        'build_version': '3ba949a9cb5b0b1cccd61e76159969a49377fd7d/1.10.0-dev/Clean/RELEASE/BoringSSL'
    }
}
```

Route Request:

Initial
```
{
    'node': {
        'id': 'service-c-10.1.1.68',
        'cluster': 'service-c',
        'build_version': '3ba949a9cb5b0b1cccd61e76159969a49377fd7d/1.10.0-dev/Clean/RELEASE/BoringSSL'
    },
    'resource_names': ['egress_routes']
}
```

Succeeding
```
{
    'version_info': '0',
    'node': {
        'id': 'service-c-10.1.1.68',
        'cluster': 'service-c',
        'build_version': '3ba949a9cb5b0b1cccd61e76159969a49377fd7d/1.10.0-dev/Clean/RELEASE/BoringSSL'
    },
    'resource_names': ['egress_routes']
}
```
