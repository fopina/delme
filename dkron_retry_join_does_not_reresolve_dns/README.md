## Summary

After both server and agents are up and cluster is running smoothly, if the server goes down and comes back up with a different IP (but same hostname), agents do not reconnect.

## Reproduce

Bring server + agent up (in the compose file)

```
$ docker compose up -d
```

All good
```
$ curl -s localhost:8888/v1/members | jq -r '.[] | "\(.Name) \(.Addr) \(.Status)"'
dkron1 10.5.0.20 1
4b978465064a 10.5.0.2 1
```

Restart server with different IP (but same host and node names)
```
TEST_NUMBER=21 docker-compose up -d
```

Validate `dkron1` was removed from agents as it would be expected
```
docker-compose logs | grep removing
agents_1  | time="2023-01-22T23:04:39Z" level=info msg="removing server dkron1 (Addr: 10.5.0.20:6868) (DC: dc1)" node=4b978465064a
```

But they never reconnect to the new one
```
curl -s localhost:8888/v1/members | jq -r '.[] | "\(.Name) \(.Addr) \(.Status)"'
dkron1 10.5.0.21 1
```

## Workaround

Setup HA...! If there are multiple servers and each "retry-join" the others, they'll pick up on the old node with new IP.

Setup initially (3 servers + 1 agent)
```
$ TEST_EXPECT=1 TEST_NUMBER=20 docker-compose -f docker-compose-ha.yml up -d
$ curl -s localhost:8888/v1/members | jq -r '.[] | "\(.Name) \(.Addr) \(.Status)"'
dkron1 10.5.0.20 1
e571e651a8dc 10.5.0.2 1
dkron2 10.5.0.19 1
dkron3 10.5.0.18 1
$ for i in 8888 8889 8890; do curl -s localhost:$i/v1/leader | jq -r '.Name'; done
dkron1
dkron1
dkron1
```

Restart server 1 with new IP (but no longer with bootstrap expect)
```
$ TEST_EXPECT=0 TEST_NUMBER=21 docker-compose -f docker-compose-ha.yml up -d
$ for i in 8888 8889 8890; do curl -s localhost:$i/v1/leader | jq -r '.Name'; done
null
dkron3
dkron3
```

Killing dkron1 and restarting it makes it connect successfully.

## Issue

https://github.com/distribworks/dkron/issues/1253