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
 * Author: Karim Boutiba 	   <boutiba@eurecom.fr>
 * Author: Arina Prostakova    <prostako@eurecom.fr>
 * Description: This file contains utils functions.
 */
/*
 * Modified by Fatemeh Shafiei Ardestani on 2025-04-06
 * Based on OpenAirInterface (OAI) 5G software
 * Changes: See GitHub repository for full diff
 */

package sbi

import (
	"context"
	"log"
	"time"

	"github.com/kelseyhightower/envconfig"
	amf_client "gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf/components/oai-nwdaf-sbi/internal/amfclient"
	smf_client "gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf/components/oai-nwdaf-sbi/internal/smfclient"
	upf_client "gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf/components/oai-nwdaf-sbi/internal/upf_client"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// ------------------------------------------------------------------------------
// InitConfig - Initialize global variables (cfg and mongoClient) and subscribe to AMF and SMF
func InitConfig() {
	err := envconfig.Process("", &config)
	if err != nil {
		log.Fatal(err.Error())
	}
	clientOptions := options.Client().ApplyURI(config.Database.Uri)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Connected to MongoDB.")
	mongoClient = client
	// Subscribe to all event notifications from AMF
	amfEventSubscription(
		config.Server.NotifUri+config.Amf.ApiRoute,
		config.Amf.NotifCorrId,
		config.Amf.NotifId,
	)
	// Subscribe to all event notifications from SMF
	smfEventSubscription(
		config.Server.NotifUri+config.Smf.ApiRoute,
		config.Smf.NotifId,
	)
	upfEventEventSubscription(
		config.Server.NotifUri+config.Upf.ApiRoute,
		config.Upf.NotifCorrId,
		config.Upf.NotifId)
}

// ------------------------------------------------------------------------------
func amfEventSubscription(
	amfEventNotifyUri string,
	amfNotifyCorrelationId string,
	amfNfId string,
) {
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
			amfNfId,
		),
	)
	configuration := amf_client.NewConfiguration()
	amfApiClient := amf_client.NewAPIClient(configuration) // TODO: WITH CREATE SUB
	resp, r, err := amfApiClient.SubscriptionsCollectionCollectionApi.CreateSubscription(
		context.Background()).AmfCreateEventSubscription(amfCreateEventSubscription).Execute()
	if err != nil {
		log.Printf(
			"Error when calling `SubscriptionsCollectionCollectionApi.CreateSubscription``: %v\n",
			err,
		)
		log.Printf("Full HTTP response: %v\n", r)
	}
	// response from `CreateSubscription`: AmfCreatedEventSubscription
	log.Printf(
		"Response from `SubscriptionsCollectionCollectionApi.CreateSubscription`: %v\n",
		resp,
	)
}

// ------------------------------------------------------------------------------
func smfEventSubscription(smfEventNotifyUri string, smfNfId string) {

	// Store all SMF event types
	var smfEventSubs []smf_client.EventSubscription
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PDU_SES_EST),
	)
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_UE_IP_CH),
	)
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PLMN_CH),
	)
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_DDDS),
	)
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PDU_SES_REL),
	)

	//Fatemeh
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_PACKET_MON),
	)
	smfEventSubs = append(smfEventSubs,
		*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_QOS_MON),
	)

	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_AC_TY_CH),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_UP_PATH_CH),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_RAT_TY_CH),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_COMM_FAIL),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_QFI_ALLOC),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_SMCC_EXP),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_DISPERSION),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_RED_TRANS_EXP),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_WLAN_INFO),
	// )
	// smfEventSubs = append(smfEventSubs,
	// 	*smf_client.NewEventSubscription(smf_client.SMFEVENTANYOF_UPF_INFO),
	// )
	// Subscribe to all SMF event types
	nsmfEventExposure := *smf_client.NewNsmfEventExposure(
		smfNfId,
		smfEventNotifyUri,
		smfEventSubs,
	)
	configuration := smf_client.NewConfiguration()
	smfApiClient := smf_client.NewAPIClient(configuration)
	resp, r, err := smfApiClient.SubscriptionsCollectionApi.CreateIndividualSubcription(
		context.Background()).NsmfEventExposure(nsmfEventExposure).Execute()
	if err != nil {
		log.Printf(
			"Error when calling `SubscriptionsCollectionApi.CreateIndividualSubcription``: %v\n",
			err,
		)
		log.Printf("Full HTTP response: %v\n", r)
	}
	// response from `CreateIndividualSubcription`: NsmfEventExposure
	log.Printf(
		"Response from `SubscriptionsCollectionApi.CreateIndividualSubcription`: %v\n",
		resp,
	)
}
func upfEventEventSubscription(upfEventNotifyUri string,
	upfNotifyCorrelationId string,
	upfNfId string) {
	cli := upf_client.NewClient()
	// ????
	req_type := []upf_client.EventType{upf_client.USER_DATA_USAGE_MEASURES}
	//measurementType := [][]upf_client.MeasurementType{
	//	{upf_client.THROUGHPUT_MEASUREMENT, upf_client.VOLUME_MEASUREMENT}, // Replace OTHER_MEASUREMENT with the actual second value
	//}
	measurementType := [][]upf_client.MeasurementType{{upf_client.VOLUME_MEASUREMENT}}
	granType := []upf_client.GranularityOfMeasurement{upf_client.PER_FLOW}
	// change the  time of UPF event exposure subscription here.
	subs := upf_client.NewNupfEventExposure(upfNfId, upfEventNotifyUri, upf_client.PERIODIC, upfNotifyCorrelationId, req_type, 2, measurementType, granType, true)
	res, err := cli.CreateSubscription(subs)
	if err != nil {
		log.Printf(
			"Error when calling `SubscriptionsCollectionApi.CreateIndividualSubcription for upf``: %v\n",
			err,
		)
		log.Printf(
			"Response from `SubscriptionsCollectionApi.CreateIndividualSubcription`: %v\n",
			res,
		)

	}
}
