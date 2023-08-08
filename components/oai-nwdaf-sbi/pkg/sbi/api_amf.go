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

package sbi

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

//------------------------------------------------------------------------------
// ApiAmfController binds http requests to an api service and writes the service results to the http response
type ApiAmfController struct {
	service      ApiAmfServicer
	errorHandler ErrorHandler
}

// ApiAmfOption for how the controller is set up.
type ApiAmfOption func(*ApiAmfController)

//------------------------------------------------------------------------------
// WithApiAmfErrorHandler inject ErrorHandler into controller
func WithApiAmfErrorHandler(h ErrorHandler) ApiAmfOption {
	return func(c *ApiAmfController) {
		c.errorHandler = h
	}
}

//------------------------------------------------------------------------------
// NewApiAmfController creates a default api controller
func NewApiAmfController(s ApiAmfServicer, opts ...ApiAmfOption) Router {
	controller := &ApiAmfController{
		service:      s,
		errorHandler: DefaultErrorHandler,
	}

	for _, opt := range opts {
		opt(controller)
	}

	return controller
}

//------------------------------------------------------------------------------
// Routes returns all the api routes for the ApiAmfController
func (c *ApiAmfController) Routes() Routes {
	return Routes{
		{
			"PostAmfNotification",
			strings.ToUpper("Post"),
			os.Getenv("AMF_API_ROUTE"),
			c.PostAmfNotification,
		},
	}
}

//------------------------------------------------------------------------------
// PostAmfNotification - Post Amf Notification
func (c *ApiAmfController) PostAmfNotification(w http.ResponseWriter, r *http.Request) {
	log.Printf("Received notification from Amf")

	// Read the JSON Body of the AMF Notification
	jsonBody, err := ioutil.ReadAll(r.Body)
	r.Body.Close()
	if err != nil {
		c.errorHandler(w, r, &ParsingError{Err: err}, nil)
		return
	}

	result, err := c.service.StoreAmfNotificationOnDB(r.Context(), jsonBody)
	// If an error occurred, encode the error with the status code
	if err != nil {
		c.errorHandler(w, r, err, &result)
		return
	}
	// If no error, encode the body and the result code
	EncodeJSONResponse(result.Body, &result.Code, w)
}
