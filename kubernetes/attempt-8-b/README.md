## Eight Attempt (2/2)

```
                                     +------------+
                                     |+----------+|<---------------------+
                                     ||service-a ||                      |
                                     |+----------+|<---------+           |
                                     |+------+    |          |           |
                  +----------------> ||proxy |    |          |           |
                  |                  |+------+    |          |           |
                  |                  +------------+          |           |
                  |                       |                  |           |
                  v                       |                  v           |
+--------------------+                    |            +-----------+     |
|    +----------+    |                    |            |+---------+|     |
|    |xds-server|    |                    v            ||service-b||     |
|    +----------+    |        +--------------+         |+---------+|     |
|+------------------+|<------>|kube-apiserver|<------- |+-----+    |     |
||service-controller||        +--------------+         ||proxy|    |     |
|+------------------+|                    ^            |+-----+    |     |
+--------------------+                    |            +-----------+     |
            ^     ^                       |                  ^   ^       |
            |     |                       |                  |   |       |
            |     |                       |                  |   |       |
            |     |                  +------------+          |   |       |
            |     |                  |+----------+|          |   |       |
            |     |                  ||service-c ||          |   |       |
            |     |                  |+----------+|          |   |       |
            |     |                  |+-----+     |<---------+   |       |
            |     +----------------> ||proxy|     |              |       |
            |                        |+-----+     |<-------------|-------+
            |                        +------------+              |
            |                                                    |
            +----------------------------------------------------+
```

In this attempt, we now push the dynamic inventory of clusters and routes to our services.

## Verification

* To verify that all services are reachable, [we re-run our 5th attempt test](https://github.com/teh-username/service-mesh-the-hard-way/tree/master/kubernetes/attempt-5#verification)
* Run `kubectl port-forward service-a 8080:8001` and [visit the config dump page of the proxy](http://localhost:8080/config_dump).
* Run `kubectl port-forward control-plane 8080:7001` and [visit the debugging route](http://localhost:8080/debug). It should roughly be the same as config dump page of the proxy.
* For further verification, you can try applying the services individually. You should see the following:

```
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:133] cm init: initializing cds
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:477] add/update cluster kubernetes_443 during init
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:477] add/update cluster control-plane_7001 during init
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:477] add/update cluster service-a_8080 during init
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:137] cm init: all clusters initialized
[1][info][main]     [source/server/server.cc:462]                        all clusters initialized. initializing init manager
[1][info][config]   [source/server/listener_manager_impl.cc:1006]        all dependencies initialized. starting workers
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:483] add/update cluster service-b_8080 starting warming
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:496] warming cluster service-b_8080 complete
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:483] add/update cluster service-c_8080 starting warming
[1][info][upstream] [source/common/upstream/cluster_manager_impl.cc:496] warming cluster service-c_8080 complete
```

Where only `kubernetes_443`, `control-plane_7001` and `service-a_8080` were part of the proxy's initialization phase while `service-b_8080` and `service-c_8080` were added after the fact.
