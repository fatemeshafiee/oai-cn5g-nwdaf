package engine

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

// ------------------------------------------------------------------------------

func UeMob(w http.ResponseWriter, r *http.Request, client *mongo.Client) {

	switch r.Method {

	case "GET":

		log.Printf("Getting Ue Mobility from DB")

		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			panic(err)
		}

		var engineReqData EngineReqData
		err = json.Unmarshal(body, &engineReqData)
		if err != nil {
			panic(err)
		}

		// Construct the filter based on SUPI and timestamp interval
		filter := GetFilterUeMob(engineReqData)

		// Retrieve the documents matching the filter
		collection := client.Database(os.Getenv("MONGODB_DATABASE_NAME")).Collection(os.Getenv("MONGODB_COLLECTION_NAME_AMF"))

		// Find the IMSI document
		var result bson.M
		var loc []bson.M

		err = collection.FindOne(context.Background(), filter).Decode(&result)
		if err == nil {

			// Extract the location list from the result
			locationList := result["locationlist"].(primitive.A)

			// Variables to store the last user location and its timestamp
			var lastUserLocation bson.M
			var lastTimestamp int64
			// get startTs and endTs
			startTs, endTs := getExtraReportReq(engineReqData)

			// Iterate over the location list and extract the nrlocation
			for _, location := range locationList {
				locationMap := location.(primitive.M)
				userLocation := locationMap["userlocation"].(bson.M)
				timestamp := locationMap["timestamp"].(int64)

				// Check if either startTs or endTs is 0
				if startTs == 0 || endTs == 0 {
					// Update the last user location and its timestamp
					if timestamp > lastTimestamp {
						lastUserLocation = userLocation
						lastTimestamp = timestamp
					}
				} else {
					// Check if the timestamp falls within the desired range
					if timestamp > startTs && timestamp < endTs {
						loc = append(loc, userLocation)
					}
				}
			}
			// If either startTs or endTs is 0, append the last user location
			if startTs == 0 || endTs == 0 {
				loc = append(loc, lastUserLocation)
			}

		}

		response := bson.M{
			"loc": loc,
		}

		w.Header().Set("Content-Type", "application/json")

		jsonResp, err := json.Marshal(response)
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
func GetFilterUeMob(engineReqData EngineReqData) bson.M {

	log.Printf("Constructing Ue Mobility filter for DB search ...")

	// get startTs and endTs
	//startTs, endTs := getExtraReportReq(engineReqData)

	return bson.M{"_id": engineReqData.Supi}

	/*
		return bson.M{
			"_id": engineReqData.Supi,
			"locationlist": bson.M{
				"$elemMatch": bson.M{
					"timestamp": bson.M{
						"$gte": startTs,
						"$lt":  endTs,
					},
				},
			},
		}*/
}
