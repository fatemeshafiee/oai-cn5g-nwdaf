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
	"context"
)

//------------------------------------------------------------------------------
// NWDAFContextDocumentApiService is a service that implements the logic for the NWDAFContextDocumentApiServicer
type NWDAFContextDocumentApiService struct {
}

//------------------------------------------------------------------------------
// NewNWDAFContextDocumentApiService creates a default api service
func NewNWDAFContextDocumentApiService() NWDAFContextDocumentApiServicer {
	return &NWDAFContextDocumentApiService{}
}

//------------------------------------------------------------------------------
// GetNwdafContext - Get context information related to analytics subscriptions.
func (s *NWDAFContextDocumentApiService) GetNwdafContext(ctx context.Context, contextIds ContextIdList, reqContext RequestedContext) (ImplResponse, error) {
	// TODO - update GetNwdafContext with the required logic for this service method.
	// Add api_nwdaf_context_document_service.go to the .openapi-generator-ignore to avoid overwriting this service implementation when updating open api generation.

	//TODO: Uncomment the next line to return response Response(200, ContextData{}) or use other options such as http.Ok ...
	return Response(200, ContextData{}), nil

	//TODO: Uncomment the next line to return response Response(204, {}) or use other options such as http.Ok ...
	//return Response(204, nil),nil

	//TODO: Uncomment the next line to return response Response(400, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(400, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(401, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(401, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(403, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(403, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(404, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(404, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(406, {}) or use other options such as http.Ok ...
	//return Response(406, nil),nil

	//TODO: Uncomment the next line to return response Response(414, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(414, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(429, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(429, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(500, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(500, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(503, ProblemDetails{}) or use other options such as http.Ok ...
	//return Response(503, ProblemDetails{}), nil

	//TODO: Uncomment the next line to return response Response(0, {}) or use other options such as http.Ok ...
	//return Response(0, nil),nil

	// return Response(http.StatusNotImplemented, nil), errors.New("GetNwdafContext method not implemented")
}
