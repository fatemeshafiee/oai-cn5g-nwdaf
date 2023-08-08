# Scenario 3. **UE_COMMUNICATION**


## Some examples

Run the following `curl` commands to test `Traffic Characterization` (downlink/upling volume and variance) of UE COMMUNICATION.

A sample of **expected output** can be found [here](https://gitlab.eurecom.fr/development/oai-nwdaf/-/blob/master/examples/nbi_output_uecomms.json).

```bash
curl -i -X 'GET' \
  'http://nwdaf.cnx.eurecom.fr/nnwdaf-analyticsinfo/v1/analytics?event-id=UE_COMMUNICATION&ana-req=%7B%0A%20%20%22startTs%22%3A%20%222022-08-01T09%3A15%3A33.018Z%22%2C%0A%20%20%22endTs%22%3A%20%222022-10-30T09%3A15%3A33.018Z%22%0A%7D' \
  -H 'accept: application/json'
```

```bash
# 1 minute interval on 26/sept/2022 from 16:57 to 16:58
curl -i -X 'GET' \
  'http://nwdaf.cnx.eurecom.fr/nnwdaf-analyticsinfo/v1/analytics?event-id=UE_COMMUNICATION&ana-req=%7B%0A%20%20%22startTs%22%3A%20%222022-09-26T14%3A57%3A33.018Z%22%2C%0A%20%20%22endTs%22%3A%20%222022-09-26T14%3A58%3A33.018Z%22%0A%7D' \
  -H 'accept: application/json'
```

```bash
# another 1 minute interval from 17:06 to 17:07
curl -i -X 'GET' \
  'http://nwdaf.cnx.eurecom.fr/nnwdaf-analyticsinfo/v1/analytics?event-id=UE_COMMUNICATION&ana-req=%7B%0A%20%20%22startTs%22%3A%20%222022-09-26T15%3A06%3A33.018Z%22%2C%0A%20%20%22endTs%22%3A%20%222022-09-26T15%3A07%3A33.018Z%22%0A%7D' \
  -H 'accept: application/json'
```
