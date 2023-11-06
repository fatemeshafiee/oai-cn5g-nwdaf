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

#import argparse
import os
import re

from common.python.pipeline_args_parse import (
    _parse_args,
)

from common.python.generate_html import (
    generate_header,
    generate_footer,
    generate_git_info,
    generate_chapter,
    generate_list_header,
    generate_list_footer,
    generate_list_row,
)

REPORT_NAME = 'test_results_oai_nwdaf.html'
SERVICE_NAMES = ['nbi-analytics', 'nbi-events', 'nbi-ml', 'engine', 'engine-ads', 'sbi']

class HtmlReport():
    def __init__(self):
        pass

    def generate(self, args):
        cwd = os.getcwd()
        with open(os.path.join(cwd, REPORT_NAME), 'w') as wfile:
            wfile.write(generate_header(args))
            wfile.write(generate_git_info(args))
            wfile.write(self.nwdafBuildSummary())
            wfile.write(generate_footer())

    def nwdafBuildSummary(self):
        cwd = os.getcwd()
        details = ''
        status = True
        chapterName = 'Container Images Build Summary'
        details += generate_list_header()
        for service in SERVICE_NAMES:
            message, serviceStatus = self.microserviceDetails(service)
            details += message
            status = status and serviceStatus
        details += generate_list_footer()
        if status:
            details = generate_chapter(chapterName, 'All Container Target Images were created.', True) + details
        else:
            details = generate_chapter(chapterName, 'Some/All Container Target Images were NOT created.', False) + details

        return details

    def microserviceDetails(self, serviceName):
        cwd = os.getcwd()
        buildStatus = False
        logFileName = f'nwdaf-{serviceName}_docker_image_build.log'
        if os.path.isfile(f'{cwd}/archives/{logFileName}'):
            imageTag = 'notAcorrectTagForTheMoment'
            size = ''
            with open(f'{cwd}/archives/{logFileName}', 'r') as logfile:
                for line in logfile:
                    result = re.search(f'naming to docker.io/library/oai-nwdaf-{serviceName}:([0-9a-zA-Z\-\_\.]+)', line)
                    if result is not None:
                        buildStatus = True
                        imageTag = result.group(1)
            with open(f'{cwd}/archives/nwdaf_docker_image_build.log', 'r') as logfile:
                for line in logfile:
                    result = re.search(f'oai-nwdaf-{serviceName} *{imageTag}', line)
                    if result is not None:
                        result = re.search('ago  *([0-9A-Z \.]+)', line)
                        if result is not None:
                            size = result.group(1)
                            size = re.sub('MB', ' MB', size)
                            size = re.sub('GB', ' GB', size)
            if buildStatus:
                details = generate_list_row(f'oai-nwdaf-{serviceName} is OK: size is {size}', 'info-sign')
            else:
                details = generate_list_row(f'oai-nwdaf-{serviceName} is NOT OK!', 'remove-sign')
        else:
            details = generate_list_row(f'oai-nwdaf-{serviceName}i WAS NOT BUILT', 'question-sign')
        return details, buildStatus

    def appendToTestReports(self, args):
        gitInfo = generate_git_info(args)
        cwd = os.getcwd()
        for reportFile in os.listdir(cwd):
            if reportFile.endswith('.html') and re.search('results_oai_cn5g_', reportFile) is not None:
                newFile = ''
                gitInfoAppended = False
                with open(os.path.join(cwd, reportFile), 'r') as rfile:
                    for line in rfile:
                        if re.search('<h2>', line) is not None and not gitInfoAppended:
                            gitInfoAppended = True
                            newFile += gitInfo
                        newFile += line
                with open(os.path.join(cwd, reportFile), 'w') as wfile:
                    wfile.write(newFile)

if __name__ == '__main__':
    # Parse the arguments
    args = _parse_args()

    # Generate report
    HTML = HtmlReport()
    HTML.generate(args)
    HTML.appendToTestReports(args)
