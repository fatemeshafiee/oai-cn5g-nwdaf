# Scenario 2. **SESS_SUCC_RATIO** of NETWORK_PERFORMANCE

## Some examples

Run the following `curl` command to test PDU session success ratio.

A sample of **expected output** can be found [here](https://gitlab.eurecom.fr/development/oai-nwdaf/-/blob/master/examples/nbi_output_sess_succ_ratio.json).

```bash
curl -i -X 'GET' \
  'http://nwdaf.cnx.eurecom.fr/nnwdaf-analyticsinfo/v1/analytics?event-id=NETWORK_PERFORMANCE&ana-req=%7B%0A%20%20%22startTs%22%3A%20%222022-08-01T09%3A15%3A33.018Z%22%2C%0A%20%20%22endTs%22%3A%20%222022-10-30T09%3A15%3A33.018Z%22%0A%7D&event-filter=%7B%0A%20%20%20%20%22nwPerfTypes%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%22SESS_SUCC_RATIO%22%0A%20%20%20%20%5D%0A%7D' \
  -H 'accept: application/json'
```
