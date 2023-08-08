# Scenario 3. **UE_MOBILITY**

## Some examples

Run the following `curl` commands to test UE mobility information.

A sample of **expected output** can be found [here](https://gitlab.eurecom.fr/development/oai-nwdaf/-/blob/master/examples/nbi_output_uemob.json).

```bash
# get the latest location of user with imsi: imsi-208990100001120
curl -X 'GET' \
  'http://nwdaf.cnx.eurecom.fr/nnwdaf-analyticsinfo/v1/analytics?event-id=UE_MOBILITY&ana-req=%7B%7D&event-filter=%7B%7D&tgt-ue=%7B%0A%20%20%22anyUe%22%3A%20true%2C%0A%20%20%22supis%22%3A%20%5B%0A%20%20%20%20%22imsi-208990100001120%22%0A%20%20%5D%0A%7D' \
  -H 'accept: application/json'
```