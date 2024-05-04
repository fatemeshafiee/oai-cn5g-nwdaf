#!/bin/bash
cd oai-cn5g-fed/docker-compose
sudo python3 ./core-network.py --type start-basic-vpp --scenario 1
cd ../../oai-cn5g-nwdaf
sudo docker-compose -f docker-compose/docker-compose-nwdaf-cn-http2.yaml up -d --force-recreate
cd ../oai-cn5g-fed
sudo docker-compose -f docker-compose/docker-compose-gnbsim-vpp.yaml up -d --force-recreate
docker exec -it gnbsim-vpp bash -c "
    apt update
    apt-get upgrade
    wget https://github.com/appneta/tcpreplay/releases/download/v4.4.2/tcpreplay-4.4.2.tar.xz
    tar xf tcpreplay-4.4.2.tar.xz
    apt-get install build-essential libpcap-dev
    cd tcpreplay-4.4.2.tar.xz
    ./configure
    make
    make install
    apt install git
    git clone https://gitlab.com/sajidkhan382067/ddos-data-sets-2022.git
    cd ddos-data-sets-2022
    cd Benign\ Traffic/
    tcpreplay --intf1 gtp-gnb slice1.pcap

"
