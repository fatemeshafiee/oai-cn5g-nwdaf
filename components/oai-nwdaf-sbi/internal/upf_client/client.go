package upf_client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
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
	subscription_request := []byte(jsonData)
	fmt.Println(jsonData)
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
	}

	defer res.Body.Close()

	post := &SubscriptionRequest{}
	derr := json.NewDecoder(res.Body).Decode(post)
	if derr != nil {
		fmt.Println("Error getting response:", err)
		return post, err
	}
	if res.StatusCode != http.StatusCreated {
		fmt.Println("the status is not 201:", err, res.StatusCode)
		return post, err
	}

	return post, nil
}
