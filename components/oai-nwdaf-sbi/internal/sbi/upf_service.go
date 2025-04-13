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
package sbi

import (
	"context"
	"encoding/json"
	"gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf/components/oai-nwdaf-sbi/internal/upf_client"
	"go.mongodb.org/mongo-driver/bson"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

func storeUpfotificationOnDB(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		customHeader := r.Header.Get("Report_number")
		currentTime := time.Now()
		formattedTime := currentTime.Format("2006-01-02 15:04:05.000")
		log.Printf("[DSN_Latency] Storing UPF notification in Database, the report number and time %s, %s", customHeader, formattedTime)
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			log.Println(err)
			http.Error(w, "[UPF_Notification] Error reading request body", http.StatusInternalServerError)
			return
		}
		//log.Println(string(body[:]))

		upfNotification := new(upf_client.Notification)
		err = json.Unmarshal(body, upfNotification)
		if err != nil {
			log.Println(err)
			http.Error(w, "[UPF_Notification] Error unmarshaling JSON", http.StatusBadRequest)
			return
		}
		notifList, ok := upfNotification.GetEventNotifsOk()
		if !ok {
			http.Error(w, "[UPF_Notification] Error getting EventNotifs", http.StatusBadRequest)
			return
		}

		databaseName := config.Database.DbName
		collectionName := config.Database.CollectionUpfName
		upfCollection := mongoClient.Database(databaseName).Collection(collectionName)

		for _, notif := range notifList {
			//log.Println("parsing each notif")
			notifTimestamp := notif.TimeStamp
			ueIpv4Addr := notif.UeIpv4Addr
			//log.Println("the ue ip is")
			//log.Println(ueIpv4Addr)
			for _, measurement := range notif.UserDataUsageMeasurements {

				var flowInfo struct {
					SeId    int    `json:"SeId"`
					SrcIp   string `json:"SrcIp"`
					DstIp   string `json:"DstIp"`
					SrcPort int    `json:"SrcPort"`
					DstPort int    `json:"DstPort"`
				}
				if measurement.FlowInfo != nil && measurement.FlowInfo.PackFiltId != "" {
					err := json.Unmarshal([]byte(measurement.FlowInfo.PackFiltId), &flowInfo)
					if err != nil {
						log.Println("[UPF_Notification] Error parsing FlowInfo PackFiltId:", err)
					}
				} else {
					log.Println("[UPF_Notification] FlowInfo is nil or empty, skipping parsing.")
				}
				//log.Println("parsing each flow info")
				volumeMeasurement := bson.M{}
				if measurement.VolumeMeasurement != nil {
					volumeMeasurement["totalVolume"] = measurement.VolumeMeasurement.TotalVolume
					volumeMeasurement["ulVolume"] = measurement.VolumeMeasurement.UlVolume
					volumeMeasurement["dlVolume"] = measurement.VolumeMeasurement.DlVolume
					volumeMeasurement["totalPackets"] = measurement.VolumeMeasurement.TotalNbOfPackets
					volumeMeasurement["ulPackets"] = measurement.VolumeMeasurement.UlNbOfPackets
					volumeMeasurement["dlPackets"] = measurement.VolumeMeasurement.DlNbOfPackets
				}

				throughputMeasurement := bson.M{}
				if measurement.ThroughputMeasurement != nil {
					throughputMeasurement["ulThroughput"] = measurement.ThroughputMeasurement.UlThroughput
					throughputMeasurement["dlThroughput"] = measurement.ThroughputMeasurement.DlThroughput
					throughputMeasurement["ulPacketThroughput"] = measurement.ThroughputMeasurement.UlPacketThroughput
					throughputMeasurement["dlPacketThroughput"] = measurement.ThroughputMeasurement.DlPacketThroughput
				}
				applicationRelatedInformation := bson.M{}
				if measurement.ApplicationRelatedInformation != nil {
					applicationRelatedInformation["urls"] = measurement.ApplicationRelatedInformation.Urls
					applicationRelatedInformation["domainInfoList"] = measurement.ApplicationRelatedInformation.DomainInfoList
				}
				throughputStatisticsMeasurement := bson.M{}
				if measurement.ThroughputStatisticsMeasurement != nil {
					throughputStatisticsMeasurement["ulAverageThroughput"] = measurement.ThroughputStatisticsMeasurement.UlAverageThroughput
					throughputStatisticsMeasurement["dlAverageThroughput"] = measurement.ThroughputStatisticsMeasurement.DlAverageThroughput
					throughputStatisticsMeasurement["ulPeakThroughput"] = measurement.ThroughputStatisticsMeasurement.UlPeakThroughput
					throughputStatisticsMeasurement["dlPeakThroughput"] = measurement.ThroughputStatisticsMeasurement.DlPeakThroughput
					throughputStatisticsMeasurement["ulAveragePacketThroughput"] = measurement.ThroughputStatisticsMeasurement.UlAveragePacketThroughput
					throughputStatisticsMeasurement["dlAveragePacketThroughput"] = measurement.ThroughputStatisticsMeasurement.DlAveragePacketThroughput
					throughputStatisticsMeasurement["ulPeakPacketThroughput"] = measurement.ThroughputStatisticsMeasurement.UlPeakPacketThroughput
					throughputStatisticsMeasurement["dlPeakPacketThroughput"] = measurement.ThroughputStatisticsMeasurement.DlPeakPacketThroughput
				}
				report := bson.M{
					"reportType":                      "userdata_usage",
					"timestamp":                       notifTimestamp,
					"ueIpv4Addr":                      ueIpv4Addr,
					"volumeMeasurement":               volumeMeasurement,
					"throughputMeasurement":           throughputMeasurement,
					"applicationRelatedInformation":   applicationRelatedInformation,
					"throughputStatisticsMeasurement": throughputStatisticsMeasurement,
				}
				if measurement.FlowInfo != nil {
					report["seID"] = flowInfo.SeId
					report["SrcIp"] = flowInfo.SrcIp
					report["DstIp"] = flowInfo.DstIp
					report["SrcPort"] = flowInfo.SrcPort
					report["DstPort"] = flowInfo.DstPort
				}
				if measurement.AppID != "" {
					report["appID"] = measurement.AppID
				}

				//log.Printf("[UPF_Notification] Report being inserted: %+v\n", report)

				res, err := upfCollection.InsertOne(context.Background(), report)
				if err != nil {
					log.Println("[UPF_Notification] Error inserting into MongoDB:", err)
				} else {
					log.Println("Inserted document ID:", res.InsertedID)
				}

				//log.Println("inserted the report")
			}

		}

		w.WriteHeader(http.StatusOK)

	default:
		http.Error(w, "[UPF_Notification] Method not allowed", http.StatusMethodNotAllowed)
	}
}
