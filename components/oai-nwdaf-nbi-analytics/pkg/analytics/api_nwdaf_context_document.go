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

package analytics

import (
	"encoding/json"
	"net/http"
	"strings"
)

//------------------------------------------------------------------------------
// NWDAFContextDocumentApiController binds http requests to an api service and writes the service results to the http response
type NWDAFContextDocumentApiController struct {
	service      NWDAFContextDocumentApiServicer
	errorHandler ErrorHandler
}

// NWDAFContextDocumentApiOption for how the controller is set up.
type NWDAFContextDocumentApiOption func(*NWDAFContextDocumentApiController)

//------------------------------------------------------------------------------
// WithNWDAFContextDocumentApiErrorHandler inject ErrorHandler into controller
func WithNWDAFContextDocumentApiErrorHandler(h ErrorHandler) NWDAFContextDocumentApiOption {
	return func(c *NWDAFContextDocumentApiController) {
		c.errorHandler = h
	}
}

//------------------------------------------------------------------------------
// NewNWDAFContextDocumentApiController creates a default api controller
func NewNWDAFContextDocumentApiController(s NWDAFContextDocumentApiServicer, opts ...NWDAFContextDocumentApiOption) Router {
	controller := &NWDAFContextDocumentApiController{
		service:      s,
		errorHandler: DefaultErrorHandler,
	}

	for _, opt := range opts {
		opt(controller)
	}

	return controller
}

//------------------------------------------------------------------------------
// Routes returns all the api routes for the NWDAFContextDocumentApiController
func (c *NWDAFContextDocumentApiController) Routes() Routes {
	return Routes{
		{
			"GetNwdafContext",
			strings.ToUpper("Get"),
			"/nnwdaf-analyticsinfo/v1/context",
			c.GetNwdafContext,
		},
	}
}

//------------------------------------------------------------------------------
// GetNwdafContext - Get context information related to analytics subscriptions.
func (c *NWDAFContextDocumentApiController) GetNwdafContext(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query()

	contextIdsParam := query.Get("context-ids")
	var contextIdList ContextIdList
	json.Unmarshal([]byte(contextIdsParam), &contextIdList)

	reqContextParam := query.Get("req-context")
	var reqContext RequestedContext
	json.Unmarshal([]byte(reqContextParam), &reqContext)

	result, err := c.service.GetNwdafContext(r.Context(), contextIdList, reqContext)
	// If an error occurred, encode the error with the status code
	if err != nil {
		c.errorHandler(w, r, err, &result)
		return
	}
	// If no error, encode the body and the result code
	EncodeJSONResponse(result.Body, &result.Code, w)

}
