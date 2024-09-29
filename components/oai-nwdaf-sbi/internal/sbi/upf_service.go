package sbi

import (
	"context"
	"encoding/json"
	"gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf/components/oai-nwdaf-sbi/internal/upf_client"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
	"io/ioutil"
	"log"
	"net/http"
	"time"
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
		log.Println(string(body[:]))
		upfNotification := new(upf_client.Notification)
		//upfNotification := upf_client.Notification{}
		err = json.Unmarshal(body, upfNotification)
		if err != nil {
			log.Println(err)
			http.Error(w, "[UPF_Notification] Error unmarshaling JSON received a UPF Notification", http.StatusBadRequest)
			return
		}
		notifList, ok := upfNotification.GetEventNotifsOk()
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
			jsonBytes, err := json.Marshal(notif)
			if err != nil {
				http.Error(w, "[UPF_Notification] error in marshal json UPF Notification", http.StatusBadRequest)
				return
			}
			jsonString := string(jsonBytes)
			log.Printf("[UPF_Notification] found a new event: %s\n", jsonString)

			ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer cancel()

			//r := upfCollection.FindOne(ctx, &bson.M{"_id": oid})
			//if r.Err() != nil {

			//c, err := getUPFCreateByNotif(notif)
			//if err != nil {
			//	http.Error(w, "[UPF_Notification] error in getUPFCreateByNotif", http.StatusBadRequest)
			//	return
			//}
			//
			//res, err := upfCollection.InsertOne(ctx, c)
			//if err != nil {
			//	http.Error(w, "[UPF_Notification] error in updating the SMF collection", http.StatusBadRequest)
			//	return
			//}
			//if res.MatchedCount != 0 {
			//	log.Printf("[UPF_Notification] matched and updated an existing notification report from UPF")
			//}
			//if res.UpsertedCount != 0 {
			//	log.Printf("[UPF_Notification] inserted a new notification report from UPF with ID %v\n", res.UpsertedID)
			//}
			//} else {
			//
			update, err := getUPFUpdateByNotif(notif)
			if err != nil {
				http.Error(w, "[UPF_Notification] error in getUpdateByNotif", http.StatusBadRequest)
				return
			}

			res, err := upfCollection.UpdateByID(ctx, oid, update, opts)
			if err != nil {
				http.Error(w, "[UPF_Notification] error in updating the SMF collection", http.StatusBadRequest)
				return
			}
			if res.MatchedCount != 0 {
				log.Printf("[UPF_Notification] matched and updated an existing notification report from UPF")
			}
			if res.UpsertedCount != 0 {
				log.Printf("[UPF_Notification] inserted a new notification report from UPF with ID %v\n", res.UpsertedID)
			}

			//}

		}
		w.WriteHeader(http.StatusOK)

	default:
		http.Error(w, "[UPF_Notification] Method not allowed", http.StatusMethodNotAllowed)

	}

}

//
//func getUPFCreateByNotif(notif *upf_client.NotificationItem) (bson.M, error) {
//	timeStamp := time.Now().Unix()
//	create := bson.M{
//		"_id":              notif.GetEventNotifKey(),
//		"upfeventexposure": bson.A{notif},
//		"lastmodified":     timeStamp,
//	}
//	return create, nil
//}

func getUPFUpdateByNotif(notif *upf_client.NotificationItem) (bson.D, error) {
	timeStamp := time.Now().Unix()
	update := bson.D{
		{"$set", bson.D{
			{"lastmodified", timeStamp},
		}},
		{"$push", bson.M{
			"upf_volume": notif,
		}},
	}
	return update, nil
}
