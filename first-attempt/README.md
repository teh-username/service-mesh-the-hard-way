## First Attempt

For our first attempt, we'll simulate the following flow with `docker-compose`:

```
+------+      +-----+      +------+
|client|----->|proxy|----->|server|
+------+      +-----+      +------+
```

with our proxy having a listener at `0.0.0.0:9000` being routed to `server:8080`

### Verifying the setup

To verify whether the proxy works, simply run `docker-compose up` and exec into the client container once everything is up and running then just run `curl -v proxy:9000`.


You can also go to `http://localhost:8001/` on your host machine to see the admin page of the proxy.
