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
 * Description: This file contains functions to store the notifications from AMF in DB.
 */

package sbi

import (
	"context"
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"

	amf_client "gitlab.eurecom.fr/development/oai-nwdaf/components/oai-nwdaf-sbi/internal/amfclient"
)

// ------------------------------------------------------------------------------
// ApiAmfService is a service that implements the logic for the ApiAmfServicer
type ApiAmfService struct {
}

// ------------------------------------------------------------------------------
// ApiSbiService is a service that implements the logic for the ApiSbiServicer
type ApiSbiService struct {
}

type rmInfo struct {
	RmInfo    amf_client.RmInfo
	TimeStamp int64
}

type location struct {
	UserLocation amf_client.UserLocation
	TimeStamp    int64
}

type lossOfConnectReason struct {
	LossOfConnectReason amf_client.LossOfConnectivityReasonAnyOf
	TimeStamp           int64
}

// ------------------------------------------------------------------------------
// NewApiAmfService creates a default api service
func NewApiAmfService() ApiAmfServicer {
	return &ApiAmfService{}
}

// ------------------------------------------------------------------------------
// StoreAmfNotificationOnDB - Store event notification related to AMF in the Database.
func (s *ApiAmfService) StoreAmfNotificationOnDB(
	ctx context.Context,
	amfNotificationJson []byte,
) (ImplResponse, error) {
	// specify DB and collection names for AMF notifications
	databaseName := config.Database.DbName
	collectionName := config.Database.CollectionAmfName
	amfCollection := mongoClient.Database(databaseName).Collection(collectionName)
	opts := options.Update().SetUpsert(true)
	var amfNotification *amf_client.AmfEventNotification
	err := json.Unmarshal(amfNotificationJson, &amfNotification)
	if err != nil {
		return Response(http.StatusBadRequest, nil), err
	}
	reportList, ok := amfNotification.GetReportListOk()
	if !ok {
		return Response(http.StatusBadRequest, nil), err
	}
	for _, report := range reportList {
		oid := report.GetSupi()
		if oid == "" {
			return Response(http.StatusBadRequest, nil),
				errors.New("supi not found in report, cannot create object id")
		}
		update, err := getUpdateByReport(report)
		if err != nil {
			return Response(http.StatusBadRequest, nil), err
		}
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		res, err := amfCollection.UpdateByID(ctx, oid, update, opts)
		if err != nil {
			return Response(http.StatusBadRequest, nil), err
		}
		if res.MatchedCount != 0 {
			log.Println("matched and updated an existing notification report from Amf")
			return Response(http.StatusOK, nil), nil
		}
		if res.UpsertedCount != 0 {
			log.Printf("inserted a new notification report from Amf with ID %v\n",
				res.UpsertedID)
		}
	}
	return Response(http.StatusOK, nil), nil
}

// ------------------------------------------------------------------------------
// getUpdateByReport - Return update bson.D by report
func getUpdateByReport(report amf_client.AmfEventReport) (bson.D, error) {
	var update bson.D
	var err error
	switch report.GetType() {
	case amf_client.AMFEVENTTYPEANYOF_REGISTRATION_STATE_REPORT:
		update, err = getUpdateRegistration(report)
	case amf_client.AMFEVENTTYPEANYOF_LOCATION_REPORT:
		update, err = getUpdateLocation(report)
	case amf_client.AMFEVENTTYPEANYOF_LOSS_OF_CONNECTIVITY:
		update, err = getUpdateLossOfConnectivity(report)
	default:
		log.Printf("report type %s is not supported currently", string(report.GetType()))
		return nil, errors.New("invalid report type")
	}
	if err != nil {
		return nil, err
	}
	return update, nil
}

// ------------------------------------------------------------------------------
// getUpdateRegistration - Create update bson.D in case of registration
func getUpdateRegistration(report amf_client.AmfEventReport) (bson.D, error) {
	rmInfoList, ok := report.GetRmInfoListOk()
	if !ok {
		return nil, errors.New("failed to get RmInfoList")
	}
	timeStamp := time.Now().Unix()
	// TODO: fix (get rid of) the "RmStateAnyOf" field
	push := rmInfo{
		RmInfo:    rmInfoList[len(rmInfoList)-1],
		TimeStamp: timeStamp,
	}
	update := bson.D{
		{"$set", bson.D{
			{"lastmodified", timeStamp},
		}},
		{"$push", bson.M{
			"rminfolist": &push,
		}},
	}
	return update, nil
}

// ------------------------------------------------------------------------------
// getUpdateLocation - Create update bson.D in case of Location
func getUpdateLocation(report amf_client.AmfEventReport) (bson.D, error) {
	locationObj, ok := report.GetLocationOk()
	if !ok {
		return nil, errors.New("failed to get Location")
	}
	timeStamp := time.Now().Unix()
	push := location{UserLocation: *locationObj, TimeStamp: timeStamp}
	update := bson.D{
		{"$set", bson.D{
			{"lastmodified", timeStamp},
		}},
		{"$push", bson.M{
			"locationlist": &push,
		}},
	}
	return update, nil
}

// ------------------------------------------------------------------------------
// getUpdateLossOfConnectivity - Create update bson.D in case of Loss of connectivity
func getUpdateLossOfConnectivity(report amf_client.AmfEventReport) (bson.D, error) {
	lossOfConnectReasonObj, ok := report.GetLossOfConnectReasonOk()
	if !ok {
		return nil, errors.New("failed to get lossOfConnectReason")
	}
	timeStamp := time.Now().Unix()
	push := lossOfConnectReason{
		LossOfConnectReason: *lossOfConnectReasonObj.LossOfConnectivityReasonAnyOf,
		TimeStamp:           timeStamp,
	}
	update := bson.D{
		{"$set", bson.D{
			{"lastmodified", timeStamp},
		}},
		{"$push", bson.M{
			"lossofconnectreasonlist": &push,
		}},
	}
	return update, nil
}
