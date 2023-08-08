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

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"

	amf_client "gitlab.eurecom.fr/development/oai-nwdaf/components/oai-nwdaf-sbi/pkg/amfclient"
	sbi "gitlab.eurecom.fr/development/oai-nwdaf/components/oai-nwdaf-sbi/pkg/sbi"
	smf_client "gitlab.eurecom.fr/development/oai-nwdaf/components/oai-nwdaf-sbi/pkg/smfclient"
)

// ------------------------------------------------------------------------------
func main() {
	log.Printf("Server started")

	// load the environment variables from the file .env (no-docker scenario)
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	// Event notification URI amf
	amfEventNotifyUri := os.Getenv("EVENT_NOTIFY_URI") + os.Getenv("AMF_API_ROUTE")

	// amfNotifyCorrelationId
	amfNotifyCorrelationId := os.Getenv("AMF_NOTIFY_CORRELATION_ID")

	// amfNfId
	amfNfId := os.Getenv("AMF_NOTIFICATION_ID")

	// Event notification URI smf
	smfEventNotifyUri := os.Getenv("EVENT_NOTIFY_URI") + os.Getenv("SMF_API_ROUTE")

	// smfNfId
	smfNfId := os.Getenv("SMF_NOTIFICATION_ID")

	// Subscribe to all event notifications from AMF
	amfEventSubscription(amfEventNotifyUri, amfNotifyCorrelationId, amfNfId)
	// Subscribe to all event notifications from SMF
	smfEventSubscription(smfEventNotifyUri, smfNfId)

	// ++ subscribe to promotheus to get cpu and ram and add a router

	// Router for AMF notifications
	ApiAmfService := sbi.NewApiAmfService()
	ApiAmfController := sbi.NewApiAmfController(ApiAmfService)

	// Router for SMF notifications
	ApiSmfService := sbi.NewApiSmfService()
	ApiSmfController := sbi.NewApiSmfController(ApiSmfService)

	router := sbi.NewRouter(ApiAmfController, ApiSmfController)

	log.Fatal(http.ListenAndServe(":8888", router))
}

// ------------------------------------------------------------------------------
func amfEventSubscription(amfEventNotifyUri string, amfNotifyCorrelationId string, amfNfId string) {

	// Store all AMF event types
	var amfEvents []amf_client.AmfEvent
	for _, amfEventTypeAnyOf := range amf_client.AllowedAmfEventTypeAnyOfEnumValues {
		amfEvents = append(amfEvents, *amf_client.NewAmfEvent(amfEventTypeAnyOf))
	}

	// Subscribe to all AMF event types
	amfCreateEventSubscription := *amf_client.NewAmfCreateEventSubscription(
		*amf_client.NewAmfEventSubscription(
			amfEvents,
			amfEventNotifyUri,
			amfNotifyCorrelationId,
			amfNfId)) // AmfCreateEventSubscription |

	configuration := amf_client.NewConfiguration()
	amfApiClient := amf_client.NewAPIClient(configuration)
	resp, r, err := amfApiClient.SubscriptionsCollectionCollectionApi.CreateSubscription(
		context.Background()).AmfCreateEventSubscription(amfCreateEventSubscription).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `SubscriptionsCollectionCollectionApi.CreateSubscription``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `CreateSubscription`: AmfCreatedEventSubscription
	fmt.Fprintf(os.Stdout, "Response from `SubscriptionsCollectionCollectionApi.CreateSubscription`: %v\n", resp)
}

// ------------------------------------------------------------------------------
func smfEventSubscription(smfEventNotifyUri string, smfNfId string) {

	// Store all SMF event types
	var smfEventSubs []smf_client.EventSubscription
	// for _, smfEventAnyOf := range smf_client.AllowedSmfEventAnyOfEnumValues {
	// 	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smfEventAnyOf))
	// }
	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PDU_SES_EST))
	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_UE_IP_CH))
	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PLMN_CH))
	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_DDDS))
	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PDU_SES_REL))
	smfEventSubs = append(smfEventSubs, *smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_QOS_MON))

	// Subscribe to all SMF event types
	nsmfEventExposure := *smf_client.NewNsmfEventExposure(smfNfId, smfEventNotifyUri, smfEventSubs) // NsmfEventExposure |

	configuration := smf_client.NewConfiguration()
	smfApiClient := smf_client.NewAPIClient(configuration)
	resp, r, err := smfApiClient.SubscriptionsCollectionApi.CreateIndividualSubcription(
		context.Background()).NsmfEventExposure(nsmfEventExposure).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `SubscriptionsCollectionApi.CreateIndividualSubcription``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `CreateIndividualSubcription`: NsmfEventExposure
	fmt.Fprintf(os.Stdout, "Response from `SubscriptionsCollectionApi.CreateIndividualSubcription`: %v\n", resp)
}
