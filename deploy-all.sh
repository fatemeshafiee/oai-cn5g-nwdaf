#!/bin/bash
cd oai-cn5g-fed/docker-compose
sudo python3 ./core-network.py --type start-basic-vpp --scenario 1
cd ../../oai-cn5g-nwdaf
sudo docker-compose -f docker-compose/docker-compose-nwdaf-cn-http2.yaml up -d --force-recreate
cd ../oai-cn5g-fed
sudo docker-compose -f docker-compose/docker-compose-gnbsim-vpp.yaml up -d --force-recreate
