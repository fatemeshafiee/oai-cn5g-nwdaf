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
	"context"
	"net/http"
)

// ApiAmfRouter defines the required methods for binding the api requests to a responses for the ApiAmf
// The ApiAmfRouter implementation should parse necessary information from the http request,
// pass the data to a ApiAmfServicer to perform the required actions, then write the service results to the http response.
type ApiAmfRouter interface {
	PostAmfNotification(http.ResponseWriter, *http.Request)
}

// ApiSmfRouter defines the required methods for binding the api requests to a responses for the ApiSmf
// The ApiSmfRouter implementation should parse necessary information from the http request,
// pass the data to a ApiSmfServicer to perform the required actions, then write the service results to the http response.
type ApiSmfRouter interface {
	PostSmfNotification(http.ResponseWriter, *http.Request)
}

// ApiAmfServicer defines the api actions for the ApiAmf service
// This interface intended to stay up to date with the openapi yaml used to generate it,
// while the service implementation can be ignored with the .openapi-generator-ignore file
// and updated with the logic required for the API.
type ApiAmfServicer interface {
	StoreAmfNotificationOnDB(context.Context, []byte) (ImplResponse, error)
}

// ApiSmfServicer defines the api actions for the ApiSmf service
// This interface intended to stay up to date with the openapi yaml used to generate it,
// while the service implementation can be ignored with the .openapi-generator-ignore file
// and updated with the logic required for the API.
type ApiSmfServicer interface {
	StoreSmfNotificationOnDB(context.Context, []byte) (ImplResponse, error)
}
