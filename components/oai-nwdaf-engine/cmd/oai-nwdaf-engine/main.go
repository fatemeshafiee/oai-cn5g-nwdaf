package main

import (
	"log"
	"net/http"
	"os"
	"time"

	"gitlab.eurecom.fr/mekrache/oai-nwdaf/components/oai-nwdaf-engine/pkg/engine"
)

// ------------------------------------------------------------------------------

func main() {

	log.Printf("Server started")

	// Connect to Mongo DB
	client := engine.ConnectMongo(os.Getenv("MONGODB_URI"))

	// create a new ServeMux (router)
	mux := http.NewServeMux()

	// register routes
	mux.HandleFunc(os.Getenv("ENGINE_NUM_OF_UE_ROUTE"), func(w http.ResponseWriter, r *http.Request) {
		engine.NwPerfNumOfUe(w, r, client)
	})

	mux.HandleFunc(os.Getenv("ENGINE_SESS_SUCC_RATIO_ROUTE"), func(w http.ResponseWriter, r *http.Request) {
		engine.NwPerfNumOfPdu(w, r, client)
	})

	mux.HandleFunc(os.Getenv("ENGINE_UE_COMMUNICATION_ROUTE"), func(w http.ResponseWriter, r *http.Request) {
		engine.UeComm(w, r, client)
	})

	mux.HandleFunc(os.Getenv("ENGINE_UE_MOBILITY_ROUTE"), func(w http.ResponseWriter, r *http.Request) {
		engine.UeMob(w, r, client)
	})

	server := &http.Server{
		Addr:         ":8080",
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	log.Fatal(server.ListenAndServe())

}
