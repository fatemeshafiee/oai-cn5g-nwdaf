------------------------------------------------------------------------------

                             OPENAIR-CN-5G
 An implementation of the 5G Core network by the OpenAirInterface community.

------------------------------------------------------------------------------

OPENAIR-CN-5G is an implementation of the 3GPP specifications for the 5G Core Network.
At the moment, it contains the following network elements:

* Access and Mobility Management Function (**AMF**)
* Authentication Server Management Function (**AUSF**)
* Location Management Function (**LMF**)
* Network Exposure Function (**NEF**)
* Network Slicing Selection Function (**NSSF**)
* Network Repository Function (**NRF**)
* Network Data Analytics Function (**NWDAF**)
* Policy Control Function (**PCF**)
* Session Management Function (**SMF**)
* Unified Data Management (**UDM**)
* Unified Data Repository (**UDR**)
* Unstructured Data Storage Function (**UDSF**)
* User Plane Function (**UPF**)

Each has its own repository: this repository (`oai-cn5g-nwdaf`) is meant for NWDAF.

# Licence info

It is distributed under `OAI Public License V1.1`.
See [OAI Website for more details](https://www.openairinterface.org/?page_id=698).

The text for `OAI Public License V1.1` is also available under [LICENSE](LICENSE)
file at the root of this repository.

# Where to start

The Openair-CN-5G NWDAF code is written, executed, and tested on UBUNTU server focal version.
Other Linux distributions support will be added later on.

A detailed [tutorial](docs/TUTORIAL.md) is available.

# Collaborative work

This source code is managed through a GITLAB server, a collaborative development platform:

*  URL: [https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf).

Process is explained in [CONTRIBUTING](CONTRIBUTING.md) file.

# Contribution requests

In a general way, anybody who is willing can contribute on any part of the
code in any network component.

Contributions can be simple bugfixes, advices and remarks on the design,
architecture, coding/implementation.

# Release Notes

They are available on the [CHANGELOG](CHANGELOG.md) file.

# Repository Structure:

The OpenAirInterface CN NWDAF software is composed of the following parts: 

<pre>
openair-cn5g-nwdaf
├── ci-scripts                    : Directory containing the script files for CI framework.
├── cli
│   └── examples
├── components                    : Directory containing the source code divided in micro-services
│   ├── oai-nwdaf-engine
│   ├── oai-nwdaf-engine-ads
│   ├── oai-nwdaf-nbi-analytics
│   ├── oai-nwdaf-nbi-events
│   ├── oai-nwdaf-nbi-ml
│   └── oai-nwdaf-sbi
├── deployment
├── docker-compose
│   └── conf
└── docs
    └── images
</pre>
