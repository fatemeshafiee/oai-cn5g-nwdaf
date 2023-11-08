#!/usr/bin/env python3
"""
Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The OpenAirInterface Software Alliance licenses this file to You under
the OAI Public License, Version 1.1  (the "License"); you may not use this file
except in compliance with the License.
You may obtain a copy of the License at

  http://www.openairinterface.org/?page_id=698

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------
For more information about the OpenAirInterface (OAI) Software Alliance:
  contact@openairinterface.org
---------------------------------------------------------------------
"""

import argparse
import logging
import os
import re
import time
import sys
import pexpect
import common.python.cls_cmd as cls_cmd

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="[%(asctime)s] %(levelname)8s: %(message)s"
)

PrivateRegistryURL = 'selfix.sboai.cs.eurecom.fr'
ms_names = ["nbi-analytics", "nbi-events", "nbi-ml", "engine", "engine-ads", "sbi"]
cn_names = ["amf", "ausf", "nrf", "smf", "udm", "udr"]

cn5g_deploy_file = 'docker-compose-basic-vpp-nrf.yaml'
nwdaf_deploy_file = 'docker-compose-nwdaf-cn-http2.yaml'

def _parse_args() -> argparse.Namespace:
    """Parse the command line args

    Returns:
        argparse.Namespace: the created parser
    """
    example_text = '''example:
        ./run-full-test.py --help'''

    parser = argparse.ArgumentParser(description='OAI 5G CORE NETWORK Utility tool',
                                    epilog=example_text,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    # NWDAF Micro-Services' Images Tag
    parser.add_argument(
        '--tag', '-t',
        action='store',
        help='NWDAF Micro-Services Images Tag',
    )

    # Pull from local private registry
    parser.add_argument(
        '--pull',
        action='store_true',
        default=False,
        help='Pull from local private registry',
    )

    # Capture PCAP
    parser.add_argument(
        '--capture',
        action='store_true',
        default=False,
        help='Capture',
    )

    args, unknown = parser.parse_known_args()
    return args

def pullFromPrivateRegistry(tag):
    logging.debug(f'\u001B[1mPulling images with tag {tag}\u001B[0m')
    myCmds = cls_cmd.LocalCmd()
    ret = myCmds.run(f'docker login -u oaicicd -p oaicicd {PrivateRegistryURL}')
    if ret.returncode != 0:
        myCmds.close()
        return -1

    for service in ms_names:
        ret = myCmds.run(f'docker pull {PrivateRegistryURL}/oai-nwdaf-{service}:{tag}')
        if ret.returncode != 0:
            myCmds.close()
            return -1

    ret = myCmds.run(f'docker logout {PrivateRegistryURL}')
    if ret.returncode != 0:
        myCmds.close()
        return -1

    myCmds.close()
    return 0

def removePulledImages(tag):
    logging.debug(f'\u001B[1mRemoving images with tag {tag}\u001B[0m')
    myCmds = cls_cmd.LocalCmd()
    for service in ms_names:
        myCmds.run(f'docker rmi {PrivateRegistryURL}/oai-nwdaf-{service}:{tag} || true')

    myCmds.run(f'docker logout {PrivateRegistryURL}')
    myCmds.close()
    return 0

def deployOAICN5G():
    logging.debug('\u001B[1mDeploying the OAI CN5G v2.0.0\u001B[0m')
    myCmds = cls_cmd.LocalCmd()
    myCmds.run('mkdir -p tests archives')
    myCmds.run('git clone --branch develop https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git tests')
    myCmds.run('cd tests && git submodule update --init ci-scripts')
    ret = myCmds.run('cd tests/docker-compose && python3 ./core-network.py --type start-basic-vpp --scenario 1')
    cwd = os.getcwd()
    with open(f'{cwd}/archives/cn5g_deploy.log', 'w') as wfile:
        wfile.write(ret.stdout)
    ret2 = myCmds.run(f'cd tests/docker-compose && docker-compose -f {cn5g_deploy_file} ps --all')
    for line in ret2.stdout.split('\n'):
        logging.debug(line)
    myCmds.close()
    if ret.returncode != 0:
        logging.error('\u001B[1mDeploying the OAI CN5G FAILED!\u001B[0m')
    return int(ret.returncode)

def undeployOAICN5G(do_capture):
    logging.debug('\u001B[1mUn-deploying the OAI CN5G\u001B[0m')
    myCmds = cls_cmd.LocalCmd()
    ret = myCmds.run('docker ps -a | grep oai-amf')
    if ret.returncode != 0:
        logging.debug('No trace of deployed container')
        myCmds.close()
        return 0
    myCmds.run(f'cd tests/docker-compose && docker-compose -f {cn5g_deploy_file} stop')
    for nf in cn_names:
        myCmds.run(f'docker logs oai-{nf} > archives/{nf}.log 2>&1')
    myCmds.run('cd tests/docker-compose && python3 ./core-network.py --type stop-basic-vpp --scenario 1')
    ret2 = myCmds.run(f'cd tests/docker-compose && docker-compose -f {cn5g_deploy_file} ps --all')
    for line in ret2.stdout.split('\n'):
        logging.debug(line)
    if do_capture:
        myCmds.run('cp /tmp/oai-nwdaf.* archives')
        myCmds.run('sudo rm -f /tmp/oai-nwdaf.*')
    myCmds.run('docker volume prune -f')
    myCmds.run('docker network prune -f')
    myCmds.close()
    return 0

def deployNWDAF(tag, do_capture, pulledImages):
    logging.debug('\u001B[1mDeploying the OAI NWDAF micro-services\u001B[0m')
    time.sleep(5)
    myCmds = cls_cmd.LocalCmd()
    for service in ms_names:
        if pulledImages:
            myCmds.run(f'sed -i -e "s@oai-nwdaf-{service}:latest@{PrivateRegistryURL}/oai-nwdaf-{service}:{tag}@" docker-compose/{nwdaf_deploy_file}')
        else:
            myCmds.run(f'sed -i -e "s@oai-nwdaf-{service}:latest@oai-nwdaf-{service}:{tag}@" docker-compose/{nwdaf_deploy_file}')
    myCmds.run(f'cp docker-compose/{nwdaf_deploy_file} archives')
    # Deploying in 2 steps, so the nwdaf network is created and we can cpature on it
    myCmds.run(f'docker-compose -f docker-compose/{nwdaf_deploy_file} up -d oai-nwdaf-nbi-gateway')
    captureStatus = 0
    if do_capture:
        time.sleep(5)
        # Using pexpect for background task
        myShell = pexpect.spawn('ssh oaicicd@localhost')
        myShell.timeout = 5
        response = myShell.expect(['Last login', pexpect.EOF, pexpect.TIMEOUT])
        if response == 0:
            time.sleep(1)
            myShell.expect(["\$"])
            capture_cmd = 'nohup sudo tshark -i demo-oai -i cn5g-nwdaf -w /tmp/oai-nwdaf.pcap > /tmp/oai-nwdaf.log 2>&1 &'
            logging.info(capture_cmd)
            myShell.sendline(capture_cmd)
            myShell.expect(["\$", pexpect.EOF, pexpect.TIMEOUT])
        else:
            logging.error(f'Could not spawn ssh because {response}')
            captureStatus = -1
        time.sleep(5)
        myShell.sendline('exit')
        myCmds.run('sudo chmod 666 /tmp/oai-nwdaf.*')
    ret0 = myCmds.run(f'docker-compose -f docker-compose/{nwdaf_deploy_file} up -d')
    # Testing the status of each container
    container_names = ["database", "nbi-gateway", "nbi-analytics", "nbi-events", "nbi-ml", "engine", "engine-ads", "sbi"]
    deployStatus = captureStatus + int(ret0.returncode)
    for container in container_names:
        ret1 = myCmds.run(f'./tests/ci-scripts/checkContainerStatus.py --container_name oai-nwdaf-{container} --timeout 30')
        deployStatus += int(ret1.returncode)
    ret2 = myCmds.run(f'docker-compose -f docker-compose/{nwdaf_deploy_file} ps --all')
    for line in ret2.stdout.split('\n'):
        logging.debug(line)
    cwd = os.getcwd()
    myCmds.run(f'docker run --name test-cli --network host -d --volume {cwd}/cli:/nwdaf-cli nwdaf-cli:latest')
    myCmds.close()
    if deployStatus != 0:
        logging.error('\u001B[1mDeploying the OAI NWDAF micro-services FAILED!\u001B[0m')
    return deployStatus

def undeployNWDAF():
    logging.debug('\u001B[1mUn-deploying the OAI NWDAF micro-services\u001B[0m')
    myCmds = cls_cmd.LocalCmd()
    myCmds.run('docker rm -f test-cli')
    ret = myCmds.run(f'docker-compose -f docker-compose/{nwdaf_deploy_file} stop')
    for service in ms_names:
        myCmds.run(f'docker logs oai-nwdaf-{service} > archives/nwdaf-{service}.log 2>&1')
    ret = myCmds.run(f'docker-compose -f docker-compose/{nwdaf_deploy_file} down')
    myCmds.run(f'git checkout -- docker-compose/{nwdaf_deploy_file}')
    myCmds.close()
    if ret.returncode != 0:
        logging.error('\u001B[1mUn-deploying the OAI NWDAF micro-services FAILED!\u001B[0m')
    return int(ret.returncode)

def testNWDAF():
    testStatus = 0
    logging.debug('\u001B[1mTesting the Analytics Info API\u001B[0m')
    myCmds = cls_cmd.LocalCmd()
    myCmds.run('mkdir -p archives/tests')
    analyticsTests = []
    analyticsTests.append(('numUe', '.nwPerfs[0].absoluteNum', '0', '1'))
    analyticsTests.append(('numPdu', '.nwPerfs[0].absoluteNum', '0', '1'))
    analyticsTests.append(('ueComm', '.ueComms[0].trafChar.ulVol', '0', '52200'))
    analyticsTests.append(('numPdu_snssais_dnns', '.nwPerfs[0].absoluteNum', '0', '1'))
    # First round of testing (no UEs yet)
    for name, jqPattern, test0Res, test1Res in analyticsTests:
        myCmds.run(f'docker exec test-cli /bin/bash -c "python nwdaf.py analytics examples/analytics/{name}.json" > archives/tests/{name}_test0.json 2>&1')
        ret = myCmds.run(f'jq {jqPattern} archives/tests/{name}_test0.json', silent=True)
        if ret.stdout.strip() != test0Res:
            logging.error(f'Test {name} expected was {test0Res}')
            testStatus = -1
    myCmds.run('cd tests/docker-compose && docker-compose -f docker-compose-gnbsim-vpp.yaml up -d')
    myCmds.run('./tests/ci-scripts/checkContainerStatus.py --container_name gnbsim-vpp --timeout 30')
    time.sleep(10)
    # Retrieve the UE allocated IP address
    ret = myCmds.run('docker logs gnbsim-vpp 2>&1 | grep "UE address:"')
    ipAddr = ''
    if ret.returncode == 0:
        ipRet = re.search('UE address: ([0-9.]+)', ret.stdout)
        if ipRet is not None:
            ipAddr = ipRet.group(1)
            logging.debug(f'UE was allocated this IP address ({ipAddr}) by the CN5G')
    if ipAddr != '':
        myCmds.run(f'docker exec gnbsim-vpp /bin/bash -c "ping -c50 -i 0.2 -s 1016 -I {ipAddr} 192.168.73.135" > archives/ping_test.log 2>&1')
    time.sleep(20)
    # Second round of testing after connecting one UE and done some traffic
    for name, jqPattern, test0Res, test1Res in analyticsTests:
        myCmds.run(f'docker exec test-cli /bin/bash -c "python nwdaf.py analytics examples/analytics/{name}.json" > archives/tests/{name}_test1.json 2>&1')
        ret = myCmds.run(f'jq {jqPattern} archives/tests/{name}_test1.json', silent=True)
        if ret.stdout.strip() != test1Res:
            logging.error(f'Test {name} expected was {test1Res}')
            testStatus = -1
    time.sleep(10)
    myCmds.run('cd tests/docker-compose && docker-compose -f docker-compose-gnbsim-vpp.yaml stop')
    myCmds.run('docker logs gnbsim-vpp > archives/gnbsim-vpp.log 2>&1')
    myCmds.run('cd tests/docker-compose && docker-compose -f docker-compose-gnbsim-vpp.yaml down')
    if testStatus != 0:
        logging.error('\u001B[1mTesting the Analytics Info API FAILED!\u001B[0m')
    return testStatus
    
if __name__ == '__main__':
    # Parse the arguments
    args = _parse_args()
    status = 0

    # In CI context, the local register is clean and images shall be pulled
    if args.pull:
        status += pullFromPrivateRegistry(args.tag)

    # First deploy the core network
    if status == 0:
        status += deployOAICN5G()

    if status == 0:
        status += deployNWDAF(args.tag, args.capture, args.pull)

    if status == 0:
        status += testNWDAF()

    status += undeployNWDAF()
    # Undeploy all the time the core network (even if not deployed)
    status += undeployOAICN5G(args.capture)

    # In CI context, we shall leave test server clean
    if args.pull:
        removePulledImages(args.tag)

    sys.exit(status)
