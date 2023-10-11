# NWDAF Engine ADS

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

Each has its own repository: this repository (`Engine ADS`) is meant for NWDAF Anomaly Detection Engine.

## Running the server
To run the server, follow these steps:

```bash
# make sure you are in the oai-nwdaf-engine-ads project repository
$ cd oai-nwdaf-engine-ads

# create and activate a python virtual environment
$ python3.6 -m venv env 
$ source env/bin/activate

# Upgrade pip and install requirements
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt

# run the server
$ python run.py
```

To run the server in a docker container, build the docker image as follows:

```bash
# build the oai-nwdaf-engine-ads image
$ docker build --network=host --no-cache  \
            --target oai-nwdaf-engine-ads --tag oai-nwdaf-engine-ads:latest \
            --file docker/Dockerfile.engineAds.ubuntu .

# remove dangling images
$ docker image prune --force
```

Once image is built, use the command below to run the container:
```bash
$ docker run --rm -it oai-nwdaf-engine-ads
```