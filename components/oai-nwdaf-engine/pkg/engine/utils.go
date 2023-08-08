package engine

import (
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// ------------------------------------------------------------------------------
// Type of network_performance data to request engine
type EngineReqData struct {
	StartTs time.Time `json:"startTs,omitempty"`
	EndTs   time.Time `json:"endTs,omitempty"`
	Tais    []Tai     `json:"tais,omitempty"`
	Dnns    []string  `json:"dnns,omitempty"`
	Snssaia []Snssai  `json:"snssaia,omitempty"`
	Supi    string    `json:"supi,omitempty"`
}

type Tai struct {
	PlmnId PlmnId `json:"plmnId"`
	Tac    string `json:"tac"`
	Nid    string `json:"nid,omitempty"`
}

type PlmnId struct {
	Mcc string `json:"mcc"`
	Mnc string `json:"mnc"`
}

type Snssai struct {
	Sst int32  `json:"sst"`
	Sd  string `json:"sd,omitempty"`
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
// Connect to mongo
func ConnectMongo(uri string) *mongo.Client {
	log.Printf("Connecting to Mongo DB ...")

	// Set up MongoDB client options
	ctx := context.Background()
	clientOptions := options.Client().ApplyURI(uri)

	// Connect to the MongoDB server
	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("Connected to Mongo DB")

	return client
}

// ------------------------------------------------------------------------------
// getAnaReqValues - Get Anal-request start-ts and ent-ts values
func getExtraReportReq(engineReqData EngineReqData) (int64, int64) {

	startTs, endTs := int64(0), int64(0)

	// get Start TimeStamp
	if !engineReqData.StartTs.IsZero() {
		startTs = engineReqData.StartTs.Unix()
	}

	// get End TimeStamp
	if !engineReqData.EndTs.IsZero() {
		endTs = engineReqData.EndTs.Unix()
	}

	return startTs, endTs
}

// ------------------------------------------------------------------------------
// getTimeStampCondition - Get timestamp confition to be used by filters
func getTimeStampCondition(startTs int64, endTs int64) bson.D {

	timeStamp := calculateTimeStamp(startTs, endTs)

	switch timeStamp {
	case 0:
		// case 3. Both startTs and endTs present -> number of attached UEs during period
		// timestamp between startTs and endTs
		return bson.D{{"$gt", startTs}, {"$lt", endTs}}
	default:
		// case 1/2. number of attached UEs before NOW/startTs/endTs (set in timeStamp)
		return bson.D{{"$lt", timeStamp}}
	}
}

// ------------------------------------------------------------------------------
// calculateTimeStamp - Set timestamp according to cases 1-2-3 presented below
func calculateTimeStamp(startTs int64, endTs int64) int64 {

	// case 1. No startTs or endTs -> number of documents before NOW
	// case 2A. startTs present, no endTs -> number of documents before startTs
	// case 2B. endTs present, no startTs -> number of documents before endTs
	// case 3. Both startTs and endTs present -> number of documents during period

	timeStamp := int64(0)

	// print log and set timestamp.
	if endTs == 0 {
		if startTs == 0 {
			log.Printf("Case 1. No startTs or endTs-> documents before NOW")
			timeStamp = time.Now().Unix()
		} else {
			log.Printf("Case 2A. startTs present, no endTs -> documents before startTs")
			timeStamp = startTs
		}
	} else {
		if startTs == 0 {
			log.Printf("Case 2B. no startTs, endTs present -> documents before endTs")
			timeStamp = endTs
		} else {
			log.Printf("Case 3. Both startTs and endTs present -> documents during period")
		}
	}

	return timeStamp
}

// ------------------------------------------------------------------------------
// MatchTimeStamp - Returns true if notifTimeStamp corresponds to what we are searching for.
func matchTimeStamp(notifTimeStamp int64, timeStamp int64, startTs int64, endTs int64) bool {

	if timeStamp == 0 {
		return (notifTimeStamp > startTs && notifTimeStamp < endTs)
	} else {
		return notifTimeStamp < timeStamp
	}
}
