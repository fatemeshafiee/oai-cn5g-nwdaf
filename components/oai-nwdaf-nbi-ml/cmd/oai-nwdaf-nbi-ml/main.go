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
 * Description: This is main file of the oai-nwdaf-nbi-ml HTTP server.
 */

package main

import (
	"log"
	"net/http"
	"time"

	"github.com/joho/godotenv"
	"github.com/kelseyhightower/envconfig"
	nbi_ml "gitlab.eurecom.fr/oai/cn5g/oai-cn5g-nwdaf/components/oai-nwdaf-nbi-ml/internal/nbiml"
)

type MainConfig struct {
	Server struct {
		Addr string `envconfig:"SERVER_ADDR"`
	}
}

func main() {
	// load the environment variables from the file .env
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	var config MainConfig
	err = envconfig.Process("", &config)
	if err != nil {
		log.Fatal(err.Error())
	}
	IndividualNWDAFMLModelProvisionSubscriptionDocumentApiService := nbi_ml.NewIndividualNWDAFMLModelProvisionSubscriptionDocumentApiService()
	IndividualNWDAFMLModelProvisionSubscriptionDocumentApiController := nbi_ml.NewIndividualNWDAFMLModelProvisionSubscriptionDocumentApiController(
		IndividualNWDAFMLModelProvisionSubscriptionDocumentApiService,
	)
	SubscriptionsCollectionApiService := nbi_ml.NewSubscriptionsCollectionApiService()
	SubscriptionsCollectionApiController := nbi_ml.NewSubscriptionsCollectionApiController(
		SubscriptionsCollectionApiService,
	)
	router := nbi_ml.NewRouter(
		IndividualNWDAFMLModelProvisionSubscriptionDocumentApiController,
		SubscriptionsCollectionApiController,
	)
	server := &http.Server{
		Addr:         config.Server.Addr,
		Handler:      router,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}
	log.Printf("Server listening at %s", config.Server.Addr)
	log.Fatal(server.ListenAndServe())
}
