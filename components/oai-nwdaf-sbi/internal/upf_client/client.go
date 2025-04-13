/*
 * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The OpenAirInterface Software Alliance licenses this file to You under
 * the OAI Public License, Version 1.1  (the "License"); you may not use this
 * file except in compliance with the License. You may obtain a copy of the
 * License at
 *
 *      http://www.openairinterface.org/?page_id=698
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *-------------------------------------------------------------------------------
 * For more information about the OpenAirInterface (OAI) Software Alliance:
 *      contact@openairinterface.org
 */

/*
/*
  - Author Fatemeh Shafiei Ardestani on 2025-04-06
  - Based on OpenAirInterface (OAI) 5G software
  - Changes: See GitHub repository for full diff
*/
package upf_client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// Upf struct {
// IpAddr            string `envconfig:"UPF_IP_ADDR"`
// SubRoute          string `envconfig:"UPF_SUBSCR_ROUTE"`
// ApiRoute          string `envconfig:"UPF_API_ROUTE"`
// NotifCorrId       string `envconfig:"UPF_NOTIFY_CORRELATION_ID"`
// NotifId           string `envconfig:"UPFF_NOTIFICATION_ID"`
// NorifForwardRoute string `envconfig:"UPF_NOTIFICATION_FORWARD_ROUTE"`
// }
type UpfClient struct {
	Ip    string
	Port  string
	Route string
}

func NewClient() *UpfClient {
	return &UpfClient{
		Ip:    os.Getenv("UPF_IP_ADDR"),
		Port:  os.Getenv("UPF_PORT"),
		Route: os.Getenv("UPF_SUBSCR_ROUTE"),
	}
}

// get object as input
// maybe add response to return type
func (cli *UpfClient) CreateSubscription(sr *SubscriptionRequest) (*SubscriptionRequest, error) {
	jsonData, err := json.MarshalIndent(sr, "", "  ")
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return nil, err
	}
	fmt.Println(string(jsonData))
	subscription_request := []byte(jsonData)

	posturl := cli.Ip + ":" + cli.Port + cli.Route
	r, err := http.NewRequest("POST", posturl, bytes.NewBuffer(subscription_request))
	if err != nil {
		fmt.Println("Error making http request:", err)
		panic(err)
	}
	r.Header.Add("Content-Type", "application/json")

	client := &http.Client{}
	res, err := client.Do(r)
	if err != nil {
		fmt.Println("Error sending http request:", err)
		return nil, err

	}

	defer res.Body.Close()

	post := &SubscriptionRequest{}
	derr := json.NewDecoder(res.Body).Decode(post)
	if derr != nil {
		fmt.Println("Error getting response:", err)
		return post, derr
	}
	if res.StatusCode != http.StatusCreated {
		fmt.Println("the status is not 201:", err, res.StatusCode)
		return nil, fmt.Errorf("unexpected response status: %d", res.StatusCode)

	}
	currentTime := time.Now()
	formattedTime := currentTime.Format("1979-03-10 15:04:05.000")
	log.Printf("[DSN_Latency] sending request for data collection %s", formattedTime)
	return post, nil
}
