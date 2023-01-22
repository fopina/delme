## Summary

After both server and agents are up and cluster is running smoothly, if the server goes down and comes back up with a different IP (but same hostname), agents do not reconnect.

## Reproduce

Bring server + 3 nodes up (in the compose file)

```
$ docker compose up -d
```

All good
```
$ curl -s localhost:8888/v1/members | jq -r '.[] | "\(.Name) \(.Addr) \(.Status)"'
dkron1 10.5.0.20 1
4b978465064a 10.5.0.2 1
ebf32f2338f2 10.5.0.3 1
bfcf208ac7cb 10.5.0.4 1
```

Restart server with different IP (but same host and node names)
```
TEST_NUMBER=21 docker-compose up -d
```

Validate `dkron1` was removed from agents as it would be expected
```
docker-compose logs | grep removing
agents_2  | time="2023-01-22T23:04:39Z" level=info msg="removing server dkron1 (Addr: 10.5.0.20:6868) (DC: dc1)" node=bfcf208ac7cb
agents_1  | time="2023-01-22T23:04:39Z" level=info msg="removing server dkron1 (Addr: 10.5.0.20:6868) (DC: dc1)" node=4b978465064a
agents_3  | time="2023-01-22T23:04:39Z" level=info msg="removing server dkron1 (Addr: 10.5.0.20:6868) (DC: dc1)" node=ebf32f2338f2
```

But they never reconnect to the new one
```
curl -s localhost:8888/v1/members | jq -r '.[] | "\(.Name) \(.Addr) \(.Status)"'
dkron1 10.5.0.21 1
```

## Issue

https://github.com/distribworks/dkron/issues/1253