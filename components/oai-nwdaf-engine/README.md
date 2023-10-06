# NWDAF Engine

----------------------------------------------------------

                        NWDAF
An implementation of the 3GPP specifications for the NWDAF.

----------------------------------------------------------

NWDAF is an implementation of the 3GPP specifications for the NWDAF.
It contains:

- NWDAF Analytics Info Service API [**NBI Analytics**]
- NWDAF Events Subscription Service API [**NBI Events**]
- NWDAF ML Model Provision Service API [**NBI Ml**]
- NWDAF Engine [**Engine**]
- NWDAF Engine ADS [**Engine ADS**]
- NWDAF Southbound Interface [**SBI**]

Each has its own repository: this repository (`Engine`) is meant for NWDAF Engine.


## Running the server
To run the server, follow these steps:

```bash
# make sure you are in the oai-nwdaf-engine project repository
$ cd oai-nwdaf-engine

# run the server
$ go run cmd/oai-nwdaf-engine/main.go
```

To run the server in a docker container, build the docker image as follows:
```bash
# build the oai-nwdaf-engine image
$ docker build --network=host --no-cache  \
            --target oai-nwdaf-engine --tag oai-nwdaf-engine:latest \
            --file docker/Dockerfile.engine.ubuntu .

# remove dangling images
$ docker image prune --force
```

Once image is built, use the command below to run the container:
```bash
$ docker run --rm -it oai-nwdaf-engine
```