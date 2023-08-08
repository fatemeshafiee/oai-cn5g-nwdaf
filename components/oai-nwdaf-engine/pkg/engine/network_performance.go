package engine

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

// ------------------------------------------------------------------------------

func NwPerfNumOfUe(w http.ResponseWriter, r *http.Request, client *mongo.Client) {

	switch r.Method {

	case "GET":

		log.Printf("Getting Number of UE Info from DB")

		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			panic(err)
		}

		var engineReqData EngineReqData
		err = json.Unmarshal(body, &engineReqData)
		if err != nil {
			panic(err)
		}

		// get filter to calculate number of users in given network area
		filter := getFilterNwPerfNumUe(engineReqData)

		collection := client.Database(os.Getenv("MONGODB_DATABASE_NAME")).Collection(os.Getenv("MONGODB_COLLECTION_NAME_AMF"))

		log.Printf("Counting documents from mongo DB using filter ...")

		absoluteNum, err := collection.CountDocuments(context.Background(), filter)
		if err != nil {
			log.Printf("Error counting documents: %s", err)
		}

		//Implement relative ratio and confidence
		relativeRatio, confidence := int32(0), int32(0)

		// prepare http response body
		nwPerfResp := NwPerfResp{
			RelativeRatio: relativeRatio,
			AbsoluteNum:   int32(absoluteNum),
			Confidence:    confidence,
		}

		w.Header().Set("Content-Type", "application/json")

		jsonResp, err := json.Marshal(nwPerfResp)
		if err != nil {
			log.Fatalf("Error happened in JSON marshal. Err: %s", err)
		}
		w.Write(jsonResp)

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)

	}
}

// ------------------------------------------------------------------------------

func NwPerfNumOfPdu(w http.ResponseWriter, r *http.Request, client *mongo.Client) {

	switch r.Method {

	case "GET":

		log.Printf("Getting Number of Pdu Sessions from DB")

		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			panic(err)
		}

		var engineReqData EngineReqData
		err = json.Unmarshal(body, &engineReqData)
		if err != nil {
			panic(err)
		}

		// get filter to calculate number of users in given network area
		filter := getFilterNwPerfNumPdu(engineReqData)

		collection := client.Database(os.Getenv("MONGODB_DATABASE_NAME")).Collection(os.Getenv("MONGODB_COLLECTION_NAME_SMF"))

		log.Printf("Counting documents from mongo DB using filter ...")

		absoluteNum, err := collection.CountDocuments(context.Background(), filter)
		if err != nil {
			log.Printf("Error counting documents: %s", err)
		}

		//Implement relative ratio and confidence
		relativeRatio, confidence := int32(0), int32(0)

		// prepare http response body
		nwPerfResp := NwPerfResp{
			RelativeRatio: relativeRatio,
			AbsoluteNum:   int32(absoluteNum),
			Confidence:    confidence,
		}

		w.Header().Set("Content-Type", "application/json")

		jsonResp, err := json.Marshal(nwPerfResp)
		if err != nil {
			log.Fatalf("Error happened in JSON marshal. Err: %s", err)
		}
		w.Write(jsonResp)

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)

	}
}

// ------------------------------------------------------------------------------
// getFilterNumUe - Get request filter that will be used to calculates the number of UEs
// This function creates two filters, timestamps and networks area, and combine them.
func getFilterNwPerfNumUe(engineReqData EngineReqData) bson.D {

	log.Printf("Constructing filter for DB search ...")

	// get startTs and endTs
	startTs, endTs := getExtraReportReq(engineReqData)

	// get timeStamp condition to inject in mongo filter
	timeStampCondition := getTimeStampCondition(startTs, endTs)

	// get timestamps filter - UE that are registered at timestampCondition
	filterTimeReg := bson.D{
		{"rminfolist",
			bson.M{"$elemMatch": bson.M{"rminfo.rmstate.rmstateanyof": "REGISTERED",
				"timestamp": timeStampCondition}},
		}}

	// get Network Area filter
	filterLoc := bson.D{}

	if engineReqData.Tais != nil {

		tacs := make([]string, 0)
		plmnids := make([]PlmnId, 0)
		for _, t := range engineReqData.Tais {
			tacs = append(tacs, t.Tac)
			plmnids = append(plmnids, t.PlmnId)
		}

		// filter UE that are located in network area at timestampCondition
		filterLoc = bson.D{{"locationlist",
			bson.M{"$elemMatch": bson.M{
				"userlocation.nrlocation.tai.tac":    bson.D{{"$in", tacs}},
				"userlocation.nrlocation.tai.plmnid": bson.D{{"$in", plmnids}},
				"timestamp":                          timeStampCondition,
			}}},
		}
	}

	// combien the two filters
	filter := bson.D{{"$and", bson.A{filterTimeReg, filterLoc}}}

	return filter
}

// ------------------------------------------------------------------------------
// getFilterPduSesEstTime - Get filter that will be used to calculates the number PduSessionEst
// This function creates three filters, timestamps, Dnn and Snssai, and combine them.
func getFilterNwPerfNumPdu(engineReqData EngineReqData) bson.D {

	log.Printf("Constructing PDU session ratio filter for DB search ...")

	// get startTs and endTs
	startTs, endTs := getExtraReportReq(engineReqData)

	// get timeStamp condition to inject in mongo filter
	timeStampCondition := getTimeStampCondition(startTs, endTs)

	// get timestamps filter
	filterTimePdu := bson.D{{"pdusesestlist",
		bson.M{"$elemMatch": bson.M{
			"timestamp": timeStampCondition,
		}},
	},
	}

	// get Dnn filter
	filterDnn := bson.D{}

	if engineReqData.Dnns != nil {

		// filter UE that have dnn in dnns
		filterDnn = bson.D{{"pdusesestlist",
			bson.M{"$elemMatch": bson.M{
				"dnn": bson.D{{"$in", engineReqData.Dnns}},
			}},
		}}
	}

	// get Snssai filter
	filterSnssai := bson.D{}

	if engineReqData.Snssaia != nil {

		// filter UE that have Snssai in dSnssai
		filterSnssai = bson.D{{"pdusesestlist",
			bson.M{"$elemMatch": bson.M{
				"snssai": bson.D{{"$in", engineReqData.Snssaia}},
			}},
		}}
	}

	// combien the three filters
	filter := bson.D{{"$and", bson.A{filterTimePdu, filterDnn, filterSnssai}}}

	return filter
}
