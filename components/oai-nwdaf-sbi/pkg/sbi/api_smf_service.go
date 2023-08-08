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

package sbi

import (
	"context"
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"

	smf_client "gitlab.eurecom.fr/development/oai-nwdaf/components/oai-nwdaf-sbi/pkg/smfclient"
)

//------------------------------------------------------------------------------
// ApiSmfService is a service that implements the logic for the ApiSmfServicer
type ApiSmfService struct {
}

type pduSesEst struct {
	AdIpv4Addr  *string
	Dnn         *string
	PduSeId     *int32
	PduSessType *smf_client.PduSessionType
	Snssai      *smf_client.Snssai
	TimeStamp   int64
}

type ueIpCh struct {
	AdIpv4Addr *string
	PduSeId    *int32
	TimeStamp  int64
}

type ddds struct {
	DddStatus *smf_client.DlDataDeliveryStatus
	PduSeId   *int32
	TimeStamp int64
}

type qosMon struct {
	Customized_data *smf_client.CustomizedData
	PduSeId         *int32
	TimeStamp       int64
}

//------------------------------------------------------------------------------
// NewApiSmfService creates a default api service
func NewApiSmfService() ApiSmfServicer {
	return &ApiSmfService{}
}

//------------------------------------------------------------------------------
// StoreSmfNotificationOnDB - Store event notification related to SMF in the Database.
func (s *ApiSmfService) StoreSmfNotificationOnDB(ctx context.Context, smfNotificationJson []byte) (ImplResponse, error) {

	// connect to Mongo DB
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(os.Getenv("MONGODB_URI")))
	log.Printf("Connected to Mongo DB")

	defer func() {
		if err = client.Disconnect(ctx); err != nil {
			log.Fatal(err)
		}
	}()

	// verify connection (ping db client)
	ctx, cancel = context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	err = client.Ping(ctx, readpref.Primary())
	if err != nil {
		return Response(http.StatusBadRequest, nil), err
	}

	// specify DB and collection names for SMF notifications
	smfCollection := client.Database(os.Getenv("MONGODB_DATABASE_NAME")).Collection(os.Getenv("MONGODB_COLLECTION_NAME_SMF"))

	// specify the Upsert option to insert a new document if a document matching
	// the filter isn't found.
	opts := options.Update().SetUpsert(true)

	// Unmarshal JSON to SMF event exposure notification.
	// includes custom unmarshaling for customized_data (QOS_MON).
	var smfNotification *smf_client.NsmfEventExposureNotification

	err = json.Unmarshal(smfNotificationJson, &smfNotification)
	if err != nil {
		return Response(http.StatusBadRequest, nil), err
	}

	// Get list of SMF event reports
	notifList, ok := smfNotification.GetEventNotifsOk()
	if !ok {
		return Response(http.StatusBadRequest, nil), err
	}

	// store reports one by one
	for _, notif := range notifList {
		oid := notif.GetSupi()
		if oid == "" {
			return Response(http.StatusBadRequest, nil), errors.New("supi not found in notification, cannot create object id")
		}

		update, err := getUpdateByNotif(notif)
		if err != nil {
			return Response(http.StatusBadRequest, nil), err
		}

		// Update/Insert the SMF notification report

		ctx, cancel = context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		res, err := smfCollection.UpdateByID(ctx, oid, update, opts)
		if err != nil {
			return Response(http.StatusBadRequest, nil), err
		}

		if res.MatchedCount != 0 {
			log.Println("matched and updated an existing notification report from SMF")
			return Response(http.StatusOK, nil), nil
		}
		if res.UpsertedCount != 0 {
			log.Printf("inserted a new notification report from SMF with ID %v\n", res.UpsertedID)
		}
	}

	return Response(http.StatusOK, nil), nil
}

//------------------------------------------------------------------------------
// getUpdateByNotif - Return update bson.D by notif
func getUpdateByNotif(notif smf_client.EventNotification) (bson.D, error) {
	var update bson.D
	var err error
	// TODO: implement other report types
	switch notif.GetEvent() {
	case smf_client.SMFEVENTANYOF_PDU_SES_EST:
		update, err = getUpdatePDU_SES_EST(notif)
	case smf_client.SMFEVENTANYOF_UE_IP_CH:
		update, err = getUpdateUE_IP_CH(notif)
	case smf_client.SMFEVENTANYOF_PLMN_CH:
		update, err = getUpdatePLMN_CH(notif)
	case smf_client.SMFEVENTANYOF_DDDS:
		update, err = getUpdateDDDS(notif)
	case smf_client.SMFEVENTANYOF_PDU_SES_REL:
		update, err = getUpdatePDU_SES_REL(notif)
	case smf_client.SMFEVENTANYOF_QOS_MON:
		update, err = getUpdateQOS_MON(notif)
	default:
		log.Printf("notif event %s is not supported currently", string(notif.GetEvent()))
		return nil, errors.New("invalid notif event")
	}
	if err != nil {
		return nil, err
	}

	return update, nil
}

// ----------------------------------------------------------------------------------------------------------------
// getUpdatePDU_SES_EST - Create update bson.D in case of PDU SESS EST
func getUpdatePDU_SES_EST(notif smf_client.EventNotification) (bson.D, error) {
	adIpv4Addr, ok := notif.GetAdIpv4AddrOk()
	if !ok {
		return nil, errors.New("failed to get AdIpv4Addr")
	}
	dnn, ok := notif.GetDnnOk()
	if !ok {
		return nil, errors.New("failed to get Dnn")
	}
	pduSeId, ok := notif.GetPduSeIdOk()
	if !ok {
		return nil, errors.New("failed to get PduSeId")
	}
	pduSessType, ok := notif.GetPduSessTypeOk()
	if !ok {
		return nil, errors.New("failed to get PduSessType")
	}
	snssai, ok := notif.GetSnssaiOk()
	if !ok {
		return nil, errors.New("failed to get Snssai")
	}
	timeStamp := time.Now().Unix()
	push := pduSesEst{AdIpv4Addr: adIpv4Addr, Dnn: dnn, PduSeId: pduSeId, PduSessType: pduSessType, Snssai: snssai, TimeStamp: timeStamp}
	update := bson.D{{"$set", bson.D{{"lastmodified", timeStamp}}}, {"$push", bson.M{"pdusesestlist": &push}}}
	return update, nil
}

// ----------------------------------------------------------------------------------------------------------------
// getUpdateUE_IP_CH - Create update bson.D in case of UE IP CH
func getUpdateUE_IP_CH(notif smf_client.EventNotification) (bson.D, error) {
	adIpv4Addr, ok := notif.GetAdIpv4AddrOk()
	if !ok {
		return nil, errors.New("failed to get AdIpv4Addr")
	}
	pduSeId, ok := notif.GetPduSeIdOk()
	if !ok {
		return nil, errors.New("failed to get PduSeId")
	}
	timeStamp := time.Now().Unix()
	push := ueIpCh{AdIpv4Addr: adIpv4Addr, PduSeId: pduSeId, TimeStamp: timeStamp}
	update := bson.D{{"$set", bson.D{{"lastmodified", timeStamp}}}, {"$push", bson.M{"ueipchlist": &push}}}
	return update, nil
}

// ----------------------------------------------------------------------------------------------------------------
// getUpdatePLMN_CH - Create update bson.D in case of PLMN CH
func getUpdatePLMN_CH(notif smf_client.EventNotification) (bson.D, error) {
	panic("unimplemented")
}

// ----------------------------------------------------------------------------------------------------------------
// getUpdateDDDS - Create update bson.D in case of DDDs
func getUpdateDDDS(notif smf_client.EventNotification) (bson.D, error) {
	dddStatus, ok := notif.GetDddStatusOk()
	if !ok {
		return nil, errors.New("failed to get DddStatus")
	}
	pduSeId, ok := notif.GetPduSeIdOk()
	if !ok {
		return nil, errors.New("failed to get PduSeId")
	}
	timeStamp := time.Now().Unix()
	push := ddds{DddStatus: dddStatus, PduSeId: pduSeId, TimeStamp: timeStamp}
	update := bson.D{{"$set", bson.D{{"lastmodified", timeStamp}}}, {"$push", bson.M{"dddslist": &push}}}
	return update, nil
}

// ----------------------------------------------------------------------------------------------------------------
// getUpdatePDU_SES_REL - Create update bson.D in case of PDU SES REL
func getUpdatePDU_SES_REL(notif smf_client.EventNotification) (bson.D, error) {
	panic("unimplemented")
}

// ----------------------------------------------------------------------------------------------------------------
// getUpdatePDU_SES_REL - Create update bson.D in case of QoS MON
func getUpdateQOS_MON(notif smf_client.EventNotification) (bson.D, error) {
	pduSeId, ok := notif.GetPduSeIdOk()
	if !ok {
		return nil, errors.New("failed to get PduSeId")
	}
	timeStamp := time.Now().Unix()
	// include "customized_data"
	push := qosMon{Customized_data: notif.CustomizedData, PduSeId: pduSeId, TimeStamp: timeStamp}
	update := bson.D{{"$set", bson.D{{"lastmodified", timeStamp}}}, {"$push", bson.M{"qosmonlist": &push}}}
	return update, nil
}
