# Details

- Broker: RabbitMQ
- Backend:
  - RabbitMQ: "rpc://"
  - sqlalchemy(sqlite):"db+sqlite:///celery.sqlite" // Not in use right now.
  

Note: Always add timeouts when getting results from remote workers and not checking r.ready()

# Run RabbitMQ

## Create container
This creates a docker container so it's accessible on lan with the ip
```
$ sudo ip addr add 10.0.0.152/21 dev enp6s0
$ docker run --name rabbitmq -p 10.0.0.152:5672:5672 rabbitmq
```
Note: ```enp6s0``` is the network adapter.
## Run container
```
$ docker start rabbitmq [-a]
```

# Run Worker
```
$ celery -A tasks worker --loglevel=INFO --autoscale 12
```
Note: --autoscale n : n = number of cores