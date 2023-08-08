package engine

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"log"
	"math"
	"net/http"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

// ------------------------------------------------------------------------------

func UeComm(w http.ResponseWriter, r *http.Request, client *mongo.Client) {

	switch r.Method {

	case "GET":

		log.Printf("Getting Ue Communication from DB")

		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			panic(err)
		}

		var engineReqData EngineReqData
		err = json.Unmarshal(body, &engineReqData)
		if err != nil {
			panic(err)
		}

		// get filter to retrieve documents according to startTs and endTs values
		filter := GetFilterUeComm(engineReqData)

		// get collection from database
		collection := client.Database(os.Getenv("MONGODB_DATABASE_NAME")).Collection(os.Getenv("MONGODB_COLLECTION_NAME_SMF"))

		// Retrieve Documents from DB
		cursor, err := collection.Find(context.Background(), filter)
		if err != nil {
			log.Printf("Error %s", err)
		}

		commDur := int32(0)
		ulVolSlice, dlVolSlice := make([]int64, 0), make([]int64, 0)
		ulVol, ulVolVariance := int64(0), float32(0)
		dlVol, dlVolVariance := int64(0), float32(0)
		startTs, endTs := getExtraReportReq(engineReqData)
		timeStamp := calculateTimeStamp(startTs, endTs)

		for cursor.Next(context.Background()) {

			var result bson.M
			err := cursor.Decode(&result)

			if err != nil {
				log.Printf("Error decoding document: %s", err)
				continue
			}

			qosMonList, ok := result["qosmonlist"].(primitive.A)
			if !ok {
				log.Printf("Invalid qosmonlist type in document")
				continue
			}

			for _, qosMonElem := range qosMonList {

				qosMonMap, ok := qosMonElem.(bson.M)
				if !ok {
					log.Printf("Invalid qosMonElem type in document")
					continue
				}

				qosTimestamp := qosMonMap["timestamp"].(int64)

				if matchTimeStamp(qosTimestamp, timeStamp, startTs, endTs) {
					ulVolSlice = append(ulVolSlice, qosMonMap["customized_data"].(bson.M)["usagereport"].(bson.M)["volume"].(bson.M)["uplink"].(int64))
					dlVolSlice = append(dlVolSlice, qosMonMap["customized_data"].(bson.M)["usagereport"].(bson.M)["volume"].(bson.M)["downlink"].(int64))
					commDur += qosMonMap["customized_data"].(bson.M)["usagereport"].(bson.M)["duration"].(int32)
				}
			}
		}

		// check if no data was matched
		if len(ulVolSlice) != 0 {
			ulVol, ulVolVariance = calculateSumAndVariance(ulVolSlice)
			dlVol, dlVolVariance = calculateSumAndVariance(dlVolSlice)
		}

		ueCommResp := UeCommResp{
			CommDur:       commDur,
			Ts:            engineReqData.StartTs,
			UlVol:         ulVol,
			UlVolVariance: ulVolVariance,
			DlVol:         dlVol,
			DlVolVariance: dlVolVariance,
		}

		w.Header().Set("Content-Type", "application/json")

		jsonResp, err := json.Marshal(ueCommResp)
		if err != nil {
			log.Fatalf("Error happened in JSON marshal. Err: %s", err)
		}
		w.Write(jsonResp)

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)

	}
}

// ------------------------------------------------------------------------------
// GetFilterQosMonTime - Get filter to retrieve documents according to startTs and endTs values
func GetFilterUeComm(engineReqData EngineReqData) bson.D {

	log.Printf("Constructing Ue Communication filter for DB search ...")

	// get startTs and endTs
	startTs, endTs := getExtraReportReq(engineReqData)

	// get timeStamp condition to inject in mongo filter
	timeStampCondition := getTimeStampCondition(startTs, endTs)

	return bson.D{{"qosmonlist",
		bson.M{"$elemMatch": bson.M{
			// "dnn":       kvEvFilters["dnn"], // if no filter, matching only empty list (BAD)
			// "snssai":    kvEvFilters["snssai"], // if no filter, matching only empty list (BAD)
			"timestamp": timeStampCondition,
		}},
	}}

}

// -----------------------------------------------------------------------------
// GetSumAndVariance - Calculates sum and variance
func calculateSumAndVariance(volSlice []int64) (int64, float32) {

	volSum := int64(0)
	volVariance := float64(0)

	for _, vol := range volSlice {
		volSum += vol
	}

	// sum the square of the mean subtracted from each element
	volMean := float64(volSum) / float64(len(volSlice))

	for _, vol := range volSlice {
		volVariance += (float64(vol) - volMean) * (float64(vol) - volMean)
	}

	// divide variance by the slice length and take square root
	volVarianceResult := float32(math.Sqrt(volVariance / float64(len(volSlice))))
	return volSum, volVarianceResult
}
