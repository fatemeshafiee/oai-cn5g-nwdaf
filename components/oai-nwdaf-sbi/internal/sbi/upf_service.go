package sbi

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"log"
	"net/http"
	upf_client"github.com/fatemeshafiee/oai-cn5g-nwdaf/components/oai-nwdaf-sbi/internal/upf_client"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func storeUpfotificationOnDB(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		log.Printf("[UPF_Notification] Storing UPF notification in Database")
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			log.Println(err)
			http.Error(w, "[UPF_Notification] Error reading request body from UPF", http.StatusInternalServerError)
			return
		}
		log.Println(string(body[:])
		var upfNotification Notification *upf_client.Notification
		err = json.Unmarshal(body, &upfNotification)
		if err != nil {
			log.Println(err)
			http.Error(w, "[UPF_Notification] Error unmarshaling JSON received a UPF Notification", http.StatusBadRequest)
			return
		}
		notifList, ok:= upfNotification.GetEventNotifsOk()
		if !ok {
			http.Error(w, "[UPF_Notification] Error in getting EventNotifs from UPF notification", http.StatusBadRequest)
			return
		}
		databaseName := config.Database.DbName
		collectionName := config.Database.CollectionUpfName
		upfCollection := mongoClient.Database(databaseName).Collection(collectionName)
		opts := options.Update().SetUpsert(true)
		for _, notif := range notifList {
			oid, ok := notif.GetEventNotifKey()
			if !ok {
				http.Error(w, oid, http.StatusBadRequest)
				return
			}
			jsonBytes, err := notif.MarshalJSON()
			if err != nil {
				http.Error(w, "[UPF_Notification] error in marshal json UPF Notification", http.StatusBadRequest)
				return
			}
			jsonString := string(jsonBytes)
			log.Printf("[UPF_Notification] found a new event: %s\n", jsonString)
			update, err := getUpdateByNotif(notif)




		}




	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)

	}

}
func getUpdateByNotif(notif upf_client.NotificationItem) (bson.D, error) {
	var update bson.D
	var err error
	// TODO: implement other report types
	// TODO: implement other parts of userDataUsageMeasurements, now it is just for volume measurements
	switch notif.GetType() {
	case upf_client.USER_DATA_USAGE_MEASURES:
		update, err = getUpdateUE_USAGE_MEASURES(notif)

	default:
		log.Printf("notif event %s is not supported currently",
			string(notif.GetType()))
		return nil, errors.New("invalid notif event")
	}
	if err != nil {
		return nil, err
	}
	return update, nil
}
func getUpdateUE_USAGE_MEASURES(notif upf_client.NotificationItem) (bson.D, error) {


}