package sbi

import (
	"io/ioutil"
	"log"
	"net/http"
	upf_client""
)

func storeUpfotificationOnDB(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		log.Printf("Storing UPF notification in Database")
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			log.Println(err)
			http.Error(w, "Error reading request body from UPF", http.StatusInternalServerError)
			return
		}
		log.Println(string(body[:])
		var Notif Notification *upf_client.Notification
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)

	}

}
