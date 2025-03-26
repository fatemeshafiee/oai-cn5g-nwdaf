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
 * Author: Abdelkader Mekrache <mekrache@eurecom.fr>
 * Description: Functions of the events nbi service (create subscription).
 */

package events

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

/*
NWDAFEventsSubscriptionsCollectionApiService is a service that implements
the logic for the NWDAFEventsSubscriptionsCollectionApiServicer
*/
type NWDAFEventsSubscriptionsCollectionApiService struct {
}

// ------------------------------------------------------------------------------
// Type of num_of_ue data to request engine
type EngineReqData struct {
	StartTs time.Time `json:"startTs,omitempty"`
	EndTs   time.Time `json:"endTs,omitempty"`
	// for num_of_ue
	Tais []Tai `json:"networkArea,omitempty"`
	// for sess_succ_ratio
	Dnns    []string `json:"dnns,omitempty"`
	Snssaia []Snssai `json:"snssaia,omitempty"`
	Supi    string   `json:"supi,omitempty"`
}

// ------------------------------------------------------------------------------
// Type of network_performance response from engine.
type NwPerfResp struct {
	RelativeRatio int32 `json:"relativeRatio,omitempty"`
	AbsoluteNum   int32 `json:"absoluteNum,omitempty"`
	Confidence    int32 `json:"confidence,omitempty"`
}

// ------------------------------------------------------------------------------
// Type of Ue_communication response from engine.
type UeCommResp struct {
	CommDur       int32     `json:"commDur"`
	Ts            time.Time `json:"ts,omitempty"`
	UlVol         int64     `json:"ulVol,omitempty"`
	UlVolVariance float32   `json:"ulVolVariance,omitempty"`
	DlVol         int64     `json:"dlVol,omitempty"`
	DlVolVariance float32   `json:"dlVolVariance,omitempty"`
}

// ------------------------------------------------------------------------------
// Type of Ue_mobility response from engine.
type UeMobResp struct {
	Loc []UserLocation `json:"loc"`
}

// ------------------------------------------------------------------------------
// Type of Ue_communication response from engine.
// [FATEMEH] Add my own responses
type AbnorBehavrsResp struct {
	Ratio       int32       `json:"ratio,omitempty"`
	DDoSEntries []DDoSEntry `json:"ddos_entries,omitempty"`
}

type DDoSEntry struct {
	UeIp      string  `json:"ue_ip,omitempty"`
	TargetIp  string  `json:"target_ip,omitempty"`
	PduSessId uint64  `json:"pdu_sess_id,omitempty"`
	SeId      uint64  `json:"seid"`
	Ratio     float64 `json:"ratio,omitempty"`
}

// NewNWDAFEventsSubscriptionsCollectionApiService creates a default api service
func NewNWDAFEventsSubscriptionsCollectionApiService() NWDAFEventsSubscriptionsCollectionApiServicer {
	return &NWDAFEventsSubscriptionsCollectionApiService{}
}

// CreateNWDAFEventsSubscription - Create a new Individual NWDAF Events Subscription
func (s *NWDAFEventsSubscriptionsCollectionApiService) CreateNWDAFEventsSubscription(
	ctx context.Context,
	nnwdafEventsSubscription NnwdafEventsSubscription,
	urlBasePath string,
) (ImplResponse, error) {
	// TODO - run tests about feasibility of creating subscription according to TS29520
	// create new subscription id
	subscriptionId := uuid.New().String()
	subscriptionCh := make(chan string)
	// add subscription channel to mapping table
	subscriptionTable[subscriptionId] = subscriptionCh
	// start go routine to handle subscription
	for _, eventSub := range nnwdafEventsSubscription.EventSubscriptions {
		go handleSubscriptionEvent(ctx,
			eventSub,
			nnwdafEventsSubscription.NotificationURI,
			subscriptionId,
			subscriptionCh,
		)
	}
	// Add location header in http response
	respHeaders := make(map[string][]string)
	respHeaders["Location"] = []string{
		config.Events.Uri + urlBasePath + "/" + subscriptionId,
	}
	// TODO - implement FailEventReports when events aren't accepted
	eventSubInfo := NnwdafEventsSubscription{
		EventSubscriptions: nnwdafEventsSubscription.EventSubscriptions,
	}
	return ResponseWithHeaders(201, respHeaders, eventSubInfo), nil
}

// ------------------------------------------------------------------------------
// send only accepted events to handle subscription after feasibility check
// [FATEMEH] this will check the event subscription every 10 seconds
func handleSubscriptionEvent(
	ctx context.Context,
	eventSub EventSubscription,
	notificationURI string,
	subscriptionId string,
	subscriptionCh <-chan string,
) {
	log.Print("Handling subscription to ", eventSub.Event,
		" with subscription id ", subscriptionId)
loop:
	for {
		// check if channel is closed, break loop if true.
		select {
		case <-subscriptionCh:
			break loop

		default:
			switch eventSub.NotificationMethod {

			case NOTIFICATIONMETHOD_PERIODIC:
				// fill the event subscription information with data from mongoDB
				eventNotif, err := fillEventNotification(ctx, eventSub)
				if err != nil {
					log.Print(err)
					break loop
				}
				// send notification to client
				log.Print(eventNotif)
				err = sendNotification(ctx, eventNotif, notificationURI)

				if err != nil {
					log.Print(err)
					break loop
				}
				// sleep periodically
				time.Sleep(time.Duration(eventSub.RepetitionPeriod) * time.Second)

			default:
				// TODO - implement THRESHOLD case
				log.Print("Not implemented yet")
				break loop
			}
		}
	}
	log.Print("subscription to ", eventSub.Event,
		" with subscription id ", subscriptionId, " is closed.")
}

// ------------------------------------------------------------------------------
// fillEventNotification - return event notification information
func fillEventNotification(ctx context.Context,
	eventSub EventSubscription,
) (EventNotification, error) {
	// only NETWORK_PERFORMACE - NUM_OF_UE is implemented for the moment
	var eventNotif EventNotification
	switch eventSub.Event {

	case NWDAFEVENT_NETWORK_PERFORMANCE:

		nwPerfNotifData, err := getNwPerfNotifData(eventSub)
		if err != nil {
			return eventNotif, err
		}
		eventNotif.NwPerfs = nwPerfNotifData

	case NWDAFEVENT_UE_COMMUNICATION:

		UeCommData, err := getUeCommNotifData(eventSub)
		if err != nil {
			return eventNotif, err
		}
		eventNotif.UeComms = UeCommData

	case NWDAFEVENT_UE_MOBILITY:

		UeMobData, err := getUeMobNotifData(eventSub)
		if err != nil {
			return eventNotif, err
		}
		eventNotif.UeMobs = UeMobData

	case NWDAFEVENT_ABNORMAL_BEHAVIOUR:

		AbnorBehavrsData, err := getAbnormalBehaviourNotifData(eventSub)
		if err != nil {
			return eventNotif, err
		}
		eventNotif.AbnorBehavrs = AbnorBehavrsData

	default:
		// Implement others
		log.Print("Not implemented yet")
	}
	eventNotif.Event = eventSub.Event
	eventNotif.AnaMetaInfo.DataWindow.StartTime = eventSub.ExtraReportReq.StartTs
	eventNotif.AnaMetaInfo.DataWindow.StopTime = eventSub.ExtraReportReq.EndTs
	return eventNotif, nil
}

// ------------------------------------------------------------------------------
// getNwPerfAnalytics - Get list of NetworkPerfInfo
func getNwPerfNotifData(eventSub EventSubscription) ([]NetworkPerfInfo, error) {
	log.Printf("Getting NW Performance Notification Data")
	var nwPerfList []NetworkPerfInfo
	for _, nwPerfReq := range eventSub.NwPerfRequs {
		var nwPerfInfo NetworkPerfInfo
		var err error
		switch nwPerfReq.NwPerfType {

		case NETWORKPERFTYPE_NUM_OF_UE:
			nwPerfInfo, err = requestNwPerfEngine(
				eventSub,
				config.Engine.Uri+config.Routes.NumOfUe,
			)
			if err != nil {
				return nwPerfList, err
			}

		case NETWORKPERFTYPE_SESS_SUCC_RATIO:
			nwPerfInfo, err = requestNwPerfEngine(
				eventSub,
				config.Engine.Uri+config.Routes.SessSuccRatio,
			)
			if err != nil {
				return nwPerfList, err
			}

		default:
			// TODO - Implement other NwPerfTypes
			return nil, errors.New("invalid Network Performance Type")
		}
		nwPerfInfo.NwPerfType = nwPerfReq.NwPerfType
		nwPerfList = append(nwPerfList, nwPerfInfo)
	}
	return nwPerfList, nil
}

// ------------------------------------------------------------------------------
// getUeCommNotifData - Get list Ue Communication
func getUeCommNotifData(eventSub EventSubscription) ([]UeCommunication, error) {
	log.Printf("Getting UE Communications Notification Data")
	var ueCommList []UeCommunication
	// this treat just one type of UE_COMMUNICATION
	var ueCommInfo UeCommunication
	var err error
	ueCommInfo, err = requestUeCommEngine(
		eventSub,
		config.Engine.Uri+config.Routes.UeComm,
	)
	if err != nil {
		return ueCommList, err
	}
	ueCommList = append(ueCommList, ueCommInfo)
	return ueCommList, nil
}

// ------------------------------------------------------------------------------
// getUeCommNotifData - Get list Ue Communication
func getUeMobNotifData(eventSub EventSubscription) ([]UeMobility, error) {
	log.Printf("Getting UE Mobility Notification Data")
	var ueMobList []UeMobility
	// check supis not empty
	if len(eventSub.TgtUe.Supis) == 0 {
		return ueMobList, errors.New("missing supis param in TgtUe")
	}
	// for each User imsi, request the engine to get location.
	for _, supi := range eventSub.TgtUe.Supis {
		var ueMobility UeMobility
		var err error
		ueMobility, err = requestUeMobEngine(
			eventSub,
			supi,
			config.Engine.Uri+config.Routes.UeMob,
		)
		if err != nil {
			return ueMobList, err
		}
		// TODO - we need to add supi to the response ueMobInfo.Supi = supi
		ueMobList = append(ueMobList, ueMobility)
	}
	return ueMobList, nil
}

// ------------------------------------------------------------------------------
// getAbnorBehavrsData - Get list Ue Communication
func getAbnormalBehaviourNotifData(
	eventSub EventSubscription,
) ([]AbnormalBehaviour, error) {
	log.Printf("Getting Abnormal Behaviour Notification Data")
	var AbnorBehavrsList []AbnormalBehaviour
	for _, excepReq := range eventSub.ExcepRequs {
		var AbnorBehavrsInfo AbnormalBehaviour
		var err error
		//[FATEMEH] ADD ROUTE TO DDOS ENGINE
		switch excepReq.ExcepId {

		case EXCEPTIONID_UNEXPECTED_LARGE_RATE_FLOW:
			AbnorBehavrsInfo, err = requestAbnorBehavrsEngine(
				eventSub,
				excepReq,
				config.Engine.AdsUri+config.Routes.UnexpectedLargeRate,
			)

			if err != nil {
				return AbnorBehavrsList, err
			}
		case EXCEPTIONID_SUSPICION_OF_DDOS_ATTACK:
			AbnorBehavrsInfo, err = requestAbnorBehavrsEngine(
				eventSub,
				excepReq,
				config.Engine.BotUri+config.Routes.BotDetection,
			)

			if err != nil {
				return AbnorBehavrsList, err
			}

		default:
			return nil, errors.New("invalid Abnormal Behaviour Exception ID")
		}
		AbnorBehavrsInfo.Excep = excepReq
		log_data, err := json.MarshalIndent(AbnorBehavrsInfo, "", "  ")
		log.Println(string(log_data))
		AbnorBehavrsList = append(AbnorBehavrsList, AbnorBehavrsInfo)
	}
	return AbnorBehavrsList, nil
}

// ------------------------------------------------------------------------------
func sendNotification(
	ctx context.Context,
	eventNotif EventNotification,
	notificationURI string,
) error {
	log.Print("Sending notification to client")
	jsonStr, _ := json.Marshal(eventNotif)
	client := http.Client{
		//Transport: &http2.Transport{
		//	// So http2.Transport doesn't complain the URL scheme isn't 'https'
		//	AllowHTTP: true,
		//	// Pretend we are dialing a TLS endpoint. (Note, we ignore the passed tls.Config)
		//	DialTLSContext: func(ctx context.Context, network, addr string, cfg *tls.Config) (net.Conn, error) {
		//		var d net.Dialer
		//		return d.DialContext(ctx, network, addr)
		//	},
		//},
	}
	r, err := http.NewRequest("POST", notificationURI, bytes.NewBuffer(jsonStr))
	if err != nil {
		log.Print("Create req error")
		return err
	}
	r.Header.Add("Content-Type", "application/json")
	_, err = client.Do(r)
	return err
	// _, err := http.Post(notificationURI, "application/json", bytes.NewBuffer(jsonStr))
	// return err
}

// ------------------------------------------------------------------------------
func requestNwPerfEngine(
	eventSub EventSubscription,
	enginePath string,
) (NetworkPerfInfo, error) {
	log.Printf("Reaching engine to get number of UE Info from DB")
	var engineReqData EngineReqData
	engineReqData.StartTs = eventSub.ExtraReportReq.StartTs
	engineReqData.EndTs = eventSub.ExtraReportReq.EndTs
	// for num_of_ue
	engineReqData.Tais = eventSub.NetworkArea.Tais
	// for sess_succ_ratio request
	engineReqData.Dnns = eventSub.Dnns
	engineReqData.Snssaia = eventSub.Snssaia
	// Convert the data to a JSON byte array
	engineReqJsonData, err := json.Marshal(engineReqData)
	if err != nil {
		return NetworkPerfInfo{}, err
	}
	// Create a POST request with the JSON data in the body
	req, err := http.NewRequest(
		http.MethodGet,
		enginePath,
		bytes.NewBuffer(engineReqJsonData),
	)
	if err != nil {
		return NetworkPerfInfo{}, err
	}
	req.Header.Set("Content-Type", "application/json")
	// Send the request and print the response body
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return NetworkPerfInfo{}, err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	log.Println(string(body))
	var nwPerfResp NwPerfResp
	err = json.Unmarshal(body, &nwPerfResp)
	if err != nil {
		return NetworkPerfInfo{}, err
	}
	nwPerfInfo := NetworkPerfInfo{
		NetworkArea:   eventSub.NetworkArea,
		AbsoluteNum:   nwPerfResp.AbsoluteNum,
		RelativeRatio: nwPerfResp.RelativeRatio,
		Confidence:    nwPerfResp.Confidence,
	}
	return nwPerfInfo, nil
}

// ------------------------------------------------------------------------------
// FATEMEH
func requestUeCommEngine(
	eventSub EventSubscription,
	enginePath string,
) (UeCommunication, error) {
	log.Printf("Reaching engine to get UE Communication Info from DB")
	var engineReqData EngineReqData
	engineReqData.StartTs = eventSub.ExtraReportReq.StartTs
	engineReqData.EndTs = eventSub.ExtraReportReq.EndTs
	// Convert the data to a JSON byte array
	engineReqJsonData, err := json.Marshal(engineReqData)
	if err != nil {
		return UeCommunication{}, err
	}
	// Create a POST request with the JSON data in the body
	req, err := http.NewRequest(
		http.MethodGet,
		enginePath,
		bytes.NewBuffer(engineReqJsonData),
	)
	if err != nil {
		return UeCommunication{}, err
	}
	req.Header.Set("Content-Type", "application/json")
	// Send the request and print the response body
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return UeCommunication{}, err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	log.Println(string(body))
	var ueCommResp UeCommResp
	err = json.Unmarshal(body, &ueCommResp)
	if err != nil {
		return UeCommunication{}, err
	}
	trafChar := TrafficCharacterization{
		UlVol:         ueCommResp.UlVol,
		UlVolVariance: ueCommResp.UlVolVariance,
		DlVol:         ueCommResp.DlVol,
		DlVolVariance: ueCommResp.DlVolVariance,
	}
	ueCommunication := UeCommunication{
		CommDur:  ueCommResp.CommDur,
		Ts:       eventSub.ExtraReportReq.StartTs,
		TrafChar: trafChar,
	}
	return ueCommunication, nil
}

// ------------------------------------------------------------------------------
func requestUeMobEngine(
	eventSub EventSubscription,
	supi string,
	enginePath string,
) (UeMobility, error) {
	log.Printf("Reaching engine to get UE Mobility Info from DB")
	log.Printf("Supi : %s", supi)
	var engineReqData EngineReqData
	engineReqData.StartTs = eventSub.ExtraReportReq.StartTs
	engineReqData.EndTs = eventSub.ExtraReportReq.EndTs
	engineReqData.Supi = supi
	// Convert the data to a JSON byte array
	engineReqJsonData, err := json.Marshal(engineReqData)
	if err != nil {
		return UeMobility{}, err
	}
	// Create a POST request with the JSON data in the body
	req, err := http.NewRequest(
		http.MethodGet,
		enginePath,
		bytes.NewBuffer(engineReqJsonData),
	)
	if err != nil {
		return UeMobility{}, err
	}
	req.Header.Set("Content-Type", "application/json")
	// Send the request and print the response body
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return UeMobility{}, err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	var ueMobResp UeMobResp
	err = json.Unmarshal(body, &ueMobResp)
	if err != nil {
		return UeMobility{}, err
	}
	// Create a variable of type UeMobility
	var ueMobility UeMobility
	// Fill the Ts field with the current time, and duration
	ueMobility.Ts = time.Now()
	ueMobility.Duration = 10
	for _, userLocation := range ueMobResp.Loc {
		locationInfo := LocationInfo{
			Loc:        userLocation,
			Ratio:      100,
			Confidence: 0,
		}
		ueMobility.LocInfos = append(ueMobility.LocInfos, locationInfo)
	}
	return ueMobility, nil
}

// ------------------------------------------------------------------------------
func requestAbnorBehavrsEngine(
	eventSub EventSubscription,
	excepReq Exception,
	enginePath string,
) (AbnormalBehaviour, error) {
	log.Printf("Reaching engine to get abnormal behaviour")
	var engineReqData EngineReqData
	// Convert the data to a JSON byte array
	engineReqJsonData, err := json.Marshal(engineReqData)
	if err != nil {
		log.Printf("Error marshaling JSON: %v", err)
		return AbnormalBehaviour{}, err
	}
	// Log the enginePath before making the request
	log.Printf("Engine path: %s", enginePath)
	// Create a POST request with the JSON data in the body
	req, err := http.NewRequest(
		http.MethodGet, enginePath, bytes.NewBuffer(engineReqJsonData))
	if err != nil {
		log.Printf("Error making http request: %v", err)
		return AbnormalBehaviour{}, err
	}
	req.Header.Set("Content-Type", "application/json")
	// Send the request and print the response body
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Printf("Error in the default client http: %v", err)
		return AbnormalBehaviour{}, err
	}
	log.Printf("This is line 558")
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	var abnorBehavrsResp AbnorBehavrsResp
	log.Println(string(body))
	err = json.Unmarshal(body, &abnorBehavrsResp)
	if err != nil {
		return AbnormalBehaviour{}, err
	}
	//log.Println("unexpected_large_rate_flow probability is: ",
	//	float64(abnorBehavrsResp.Ratio)/float64(100))

	supis := make([]string, 0)

	for _, obj := range abnorBehavrsResp.DDoSEntries {
		entry := fmt.Sprintf("%s-%s", obj.UeIp, obj.SeId)
		supis = append(supis, entry)
	}

	//abnormalBehaviour := AbnormalBehaviour{
	//	Ratio:       abnorBehavrsResp.Ratio,
	//	DDoSEntries: ddEntries,
	//}
	abnormalBehaviour := AbnormalBehaviour{
		Supis: supis,
		Ratio: abnorBehavrsResp.Ratio
	}
	return abnormalBehaviour, nil
}
