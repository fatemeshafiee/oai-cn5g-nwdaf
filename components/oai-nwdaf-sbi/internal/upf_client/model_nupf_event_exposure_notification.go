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
/*
  - Author Fatemeh Shafiei Ardestani on 2025-04-06
  - Based on OpenAirInterface (OAI) 5G software
  - Changes: See GitHub repository for full diff
*/
package upf_client

import (
	"time"
)

type ThroughputStatisticsMeasurement struct {
	UlAverageThroughput string `json:"ulAverageThroughput"`
	DlAverageThroughput string `json:"dlAverageThroughput"`

	UlPeakThroughput          string `json:"ulPeakThroughput"`
	DlPeakThroughput          string `json:"dlPeakThroughput"`
	UlAveragePacketThroughput string `json:"ulAveragePacketThroughput"`
	DlAveragePacketThroughput string `json:"dlAveragePacketThroughput"`
	UlPeakPacketThroughput    string `json:"ulPeakPacketThroughput"`
	DlPeakPacketThroughput    string `json:"dlPeakPacketThroughput"`
}

type ThroughputMeasurement struct {
	UlThroughput       string `json:"ulThroughput"`
	DlThroughput       string `json:"dlThroughput"`
	UlPacketThroughput string `json:"ulPacketThroughput"`
	DlPacketThroughput string `json:"dlPacketThroughput"`
}

type DnProtocol string

const (
	DNS_QNAME DnProtocol = "DNS_QNAME"
	TLS_SNI   DnProtocol = "TLS_SNI"
	TLS_SAN   DnProtocol = "TLS_SAN"
	TLS_SCN   DnProtocol = "TLS_SCN"
)

type DomainInformation struct {
	DomainName         string     `json:"domainName"`
	DomainNameProtocol DnProtocol `json:"domainNameProtocol"`
}

type ApplicationRelatedInformation struct {
	Urls           []string            `json:"urls"`
	DomainInfoList []DomainInformation `json:"domainInfoList"`
}

type VolumeMeasurement struct {
	TotalVolume      string `json:"totalVolume"`
	UlVolume         string `json:"ulVolume"`
	DlVolume         string `json:"dlVolume"`
	TotalNbOfPackets uint64 `json:"totalNbOfPackets"`
	UlNbOfPackets    uint64 `json:"ulNbOfPackets"`
	DlNbOfPackets    uint64 `json:"dlNbOfPackets"`
}

type UserDataUsageMeasurements struct {
	AppID                           string                           `json:"appID"`
	FlowInfo                        *FlowInformation                 `json:"flowInfo"`
	VolumeMeasurement               *VolumeMeasurement               `json:"volumeMeasurement"`
	ThroughputMeasurement           *ThroughputMeasurement           `json:"throughputMeasurement"`
	ApplicationRelatedInformation   *ApplicationRelatedInformation   `json:"applicationRelatedInformation"`
	ThroughputStatisticsMeasurement *ThroughputStatisticsMeasurement `json:"throughputStatisticsMeasurement"`
}
type NotificationItem struct {
	Type                      EventType                   `json:"type"`
	UeIpv4Addr                string                      `json:"ueIpv4Addr"`
	UeIpv6Prefix              string                      `json:"ueIpv6Prefix"`
	UeMacAddr                 string                      `json:"ueMacAddr"`
	Dnn                       string                      `json:"dnn"`
	Snssai                    Snssai                      `json:"snssai"`
	Gpsi                      string                      `json:"gpsi"`
	Supi                      string                      `json:"supi"`
	TimeStamp                 time.Time                   `json:"timeStamp"`
	StartTime                 time.Time                   `json:"startTime"`
	UserDataUsageMeasurements []UserDataUsageMeasurements `json:"userDataUsageMeasurements"`
}

type Notification struct {
	NotificationItems []*NotificationItem `json:"notificationItems"`
	CorrelationId     string              `json:"correlationId"`
	AchievedSampRatio int                 `json:"achievedSampRatio"`
}

// UlAverageThroughput
func (t *ThroughputStatisticsMeasurement) GetUlAverageThroughput() string {
	return t.UlAverageThroughput
}

func (t *ThroughputStatisticsMeasurement) SetUlAverageThroughput(ulAverageThroughput string) {
	t.UlAverageThroughput = ulAverageThroughput
}

// DlAverageThroughput
func (t *ThroughputStatisticsMeasurement) GetDlAverageThroughput() string {
	return t.DlAverageThroughput
}

func (t *ThroughputStatisticsMeasurement) SetDlAverageThroughput(dlAverageThroughput string) {
	t.DlAverageThroughput = dlAverageThroughput
}

// UlPeakThroughput
func (t *ThroughputStatisticsMeasurement) GetUlPeakThroughput() string {
	return t.UlPeakThroughput
}

func (t *ThroughputStatisticsMeasurement) SetUlPeakThroughput(ulPeakThroughput string) {
	t.UlPeakThroughput = ulPeakThroughput
}

// DlPeakThroughput
func (t *ThroughputStatisticsMeasurement) GetDlPeakThroughput() string {
	return t.DlPeakThroughput
}

func (t *ThroughputStatisticsMeasurement) SetDlPeakThroughput(dlPeakThroughput string) {
	t.DlPeakThroughput = dlPeakThroughput
}

// UlAveragePacketThroughput
func (t *ThroughputStatisticsMeasurement) GetUlAveragePacketThroughput() string {
	return t.UlAveragePacketThroughput
}

func (t *ThroughputStatisticsMeasurement) SetUlAveragePacketThroughput(ulAveragePacketThroughput string) {
	t.UlAveragePacketThroughput = ulAveragePacketThroughput
}

// DlAveragePacketThroughput
func (t *ThroughputStatisticsMeasurement) GetDlAveragePacketThroughput() string {
	return t.DlAveragePacketThroughput
}

func (t *ThroughputStatisticsMeasurement) SetDlAveragePacketThroughput(dlAveragePacketThroughput string) {
	t.DlAveragePacketThroughput = dlAveragePacketThroughput
}

// UlPeakPacketThroughput
func (t *ThroughputStatisticsMeasurement) GetUlPeakPacketThroughput() string {
	return t.UlPeakPacketThroughput
}

func (t *ThroughputStatisticsMeasurement) SetUlPeakPacketThroughput(ulPeakPacketThroughput string) {
	t.UlPeakPacketThroughput = ulPeakPacketThroughput
}

// DlPeakPacketThroughput
func (t *ThroughputStatisticsMeasurement) GetDlPeakPacketThroughput() string {
	return t.DlPeakPacketThroughput
}

func (t *ThroughputStatisticsMeasurement) SetDlPeakPacketThroughput(dlPeakPacketThroughput string) {
	t.DlPeakPacketThroughput = dlPeakPacketThroughput
}

// UlThroughput
func (t *ThroughputMeasurement) GetUlThroughput() string {
	return t.UlThroughput
}

func (t *ThroughputMeasurement) SetUlThroughput(ulThroughput string) {
	t.UlThroughput = ulThroughput
}

// DlThroughput
func (t *ThroughputMeasurement) GetDlThroughput() string {
	return t.DlThroughput
}

func (t *ThroughputMeasurement) SetDlThroughput(dlThroughput string) {
	t.DlThroughput = dlThroughput
}

// UlPacketThroughput
func (t *ThroughputMeasurement) GetUlPacketThroughput() string {
	return t.UlPacketThroughput
}

func (t *ThroughputMeasurement) SetUlPacketThroughput(ulPacketThroughput string) {
	t.UlPacketThroughput = ulPacketThroughput
}

// DlPacketThroughput
func (t *ThroughputMeasurement) GetDlPacketThroughput() string {
	return t.DlPacketThroughput
}

func (t *ThroughputMeasurement) SetDlPacketThroughput(dlPacketThroughput string) {
	t.DlPacketThroughput = dlPacketThroughput
}

// DomainName
func (d *DomainInformation) GetDomainName() string {
	return d.DomainName
}

func (d *DomainInformation) SetDomainName(domainName string) {
	d.DomainName = domainName
}

// DomainNameProtocol
func (d *DomainInformation) GetDomainNameProtocol() DnProtocol {
	return d.DomainNameProtocol
}

func (d *DomainInformation) SetDomainNameProtocol(domainNameProtocol DnProtocol) {
	d.DomainNameProtocol = domainNameProtocol
}

// Urls
func (a *ApplicationRelatedInformation) GetUrls() []string {
	return a.Urls
}

func (a *ApplicationRelatedInformation) SetUrls(urls []string) {
	a.Urls = urls
}

// DomainInfoList
func (a *ApplicationRelatedInformation) GetDomainInfoList() []DomainInformation {
	return a.DomainInfoList
}

func (a *ApplicationRelatedInformation) SetDomainInfoList(domainInfoList []DomainInformation) {
	a.DomainInfoList = domainInfoList
}

// TotalVolume
func (v *VolumeMeasurement) GetTotalVolume() string {
	return v.TotalVolume
}

func (v *VolumeMeasurement) SetTotalVolume(totalVolume string) {
	v.TotalVolume = totalVolume
}

// UlVolume
func (v *VolumeMeasurement) GetUlVolume() string {
	return v.UlVolume
}

func (v *VolumeMeasurement) SetUlVolume(ulVolume string) {
	v.UlVolume = ulVolume
}

// DlVolume
func (v *VolumeMeasurement) GetDlVolume() string {
	return v.DlVolume
}

func (v *VolumeMeasurement) SetDlVolume(dlVolume string) {
	v.DlVolume = dlVolume
}

// TotalNbOfPackets
func (v *VolumeMeasurement) GetTotalNbOfPackets() uint64 {
	return v.TotalNbOfPackets
}

func (v *VolumeMeasurement) SetTotalNbOfPackets(totalNbOfPackets uint64) {
	v.TotalNbOfPackets = totalNbOfPackets
}

// UlNbOfPackets
func (v *VolumeMeasurement) GetUlNbOfPackets() uint64 {
	return v.UlNbOfPackets
}

func (v *VolumeMeasurement) SetUlNbOfPackets(ulNbOfPackets uint64) {
	v.UlNbOfPackets = ulNbOfPackets
}

// DlNbOfPackets
func (v *VolumeMeasurement) GetDlNbOfPackets() uint64 {
	return v.DlNbOfPackets
}

func (v *VolumeMeasurement) SetDlNbOfPackets(dlNbOfPackets uint64) {
	v.DlNbOfPackets = dlNbOfPackets
}

// AppID
func (u *UserDataUsageMeasurements) GetAppID() string {
	return u.AppID
}

func (u *UserDataUsageMeasurements) SetAppID(appID string) {
	u.AppID = appID
}

// FlowInfo
func (u *UserDataUsageMeasurements) GetFlowInfo() *FlowInformation {
	return u.FlowInfo
}

func (u *UserDataUsageMeasurements) SetFlowInfo(flowInfo *FlowInformation) {
	u.FlowInfo = flowInfo
}

// VolumeMeasurement
func (u *UserDataUsageMeasurements) GetVolumeMeasurement() *VolumeMeasurement {
	return u.VolumeMeasurement
}

func (u *UserDataUsageMeasurements) SetVolumeMeasurement(volumeMeasurement *VolumeMeasurement) {
	u.VolumeMeasurement = volumeMeasurement
}

// ThroughputMeasurement
func (u *UserDataUsageMeasurements) GetThroughputMeasurement() *ThroughputMeasurement {
	return u.ThroughputMeasurement
}

func (u *UserDataUsageMeasurements) SetThroughputMeasurement(throughputMeasurement *ThroughputMeasurement) {
	u.ThroughputMeasurement = throughputMeasurement
}

// ApplicationRelatedInformation
func (u *UserDataUsageMeasurements) GetApplicationRelatedInformation() *ApplicationRelatedInformation {
	return u.ApplicationRelatedInformation
}

func (u *UserDataUsageMeasurements) SetApplicationRelatedInformation(applicationRelatedInformation *ApplicationRelatedInformation) {
	u.ApplicationRelatedInformation = applicationRelatedInformation
}

// ThroughputStatisticsMeasurement
func (u *UserDataUsageMeasurements) GetThroughputStatisticsMeasurement() *ThroughputStatisticsMeasurement {
	return u.ThroughputStatisticsMeasurement
}

func (u *UserDataUsageMeasurements) SetThroughputStatisticsMeasurement(throughputStatisticsMeasurement *ThroughputStatisticsMeasurement) {
	u.ThroughputStatisticsMeasurement = throughputStatisticsMeasurement
}

// Type
func (n *NotificationItem) GetType() EventType {
	return n.Type
}

func (n *NotificationItem) SetType(eventType EventType) {
	n.Type = eventType
}

// UeIpv4Addr
func (n *NotificationItem) GetUeIpv4Addr() string {
	return n.UeIpv4Addr
}

func (n *NotificationItem) SetUeIpv4Addr(ueIpv4Addr string) {
	n.UeIpv4Addr = ueIpv4Addr
}

// UeIpv6Prefix
func (n *NotificationItem) GetUeIpv6Prefix() string {
	return n.UeIpv6Prefix
}

func (n *NotificationItem) SetUeIpv6Prefix(ueIpv6Prefix string) {
	n.UeIpv6Prefix = ueIpv6Prefix
}

// UeMacAddr
func (n *NotificationItem) GetUeMacAddr() string {
	return n.UeMacAddr
}

func (n *NotificationItem) SetUeMacAddr(ueMacAddr string) {
	n.UeMacAddr = ueMacAddr
}

// Dnn
func (n *NotificationItem) GetDnn() string {
	return n.Dnn
}

func (n *NotificationItem) SetDnn(dnn string) {
	n.Dnn = dnn
}

// Snssai
func (n *NotificationItem) GetSnssai() Snssai {
	return n.Snssai
}

func (n *NotificationItem) SetSnssai(snssai Snssai) {
	n.Snssai = snssai
}

// Gpsi
func (n *NotificationItem) GetGpsi() string {
	return n.Gpsi
}

func (n *NotificationItem) SetGpsi(gpsi string) {
	n.Gpsi = gpsi
}

// Supi
func (n *NotificationItem) GetSupi() string {
	return n.Supi
}

func (n *NotificationItem) SetSupi(supi string) {
	n.Supi = supi
}

// TimeStamp
func (n *NotificationItem) GetTimeStamp() time.Time {
	return n.TimeStamp
}

func (n *NotificationItem) SetTimeStamp(timeStamp time.Time) {
	n.TimeStamp = timeStamp
}

// StartTime
func (n *NotificationItem) GetStartTime() time.Time {
	return n.StartTime
}

func (n *NotificationItem) SetStartTime(startTime time.Time) {
	n.StartTime = startTime
}

// UserDataUsageMeasurements
func (n *NotificationItem) GetUserDataUsageMeasurements() []UserDataUsageMeasurements {
	return n.UserDataUsageMeasurements
}

func (n *NotificationItem) SetUserDataUsageMeasurements(userDataUsageMeasurements []UserDataUsageMeasurements) {
	n.UserDataUsageMeasurements = userDataUsageMeasurements
}

// NotificationItems
func (n *Notification) GetNotificationItems() []*NotificationItem {
	return n.NotificationItems
}

func (n *Notification) SetNotificationItems(notificationItems []*NotificationItem) {
	n.NotificationItems = notificationItems
}

// CorrelationId
func (n *Notification) GetCorrelationId() string {
	return n.CorrelationId
}

func (n *Notification) SetCorrelationId(correlationId string) {
	n.CorrelationId = correlationId
}

// AchievedSampRatio
func (n *Notification) GetAchievedSampRatio() int {
	return n.AchievedSampRatio
}

func (n *Notification) SetAchievedSampRatio(achievedSampRatio int) {
	n.AchievedSampRatio = achievedSampRatio
}

func (n *Notification) GetEventNotifsOk() ([]*NotificationItem, bool) {
	if n == nil {
		return nil, false
	}
	return n.NotificationItems, true
}
func (n *NotificationItem) GetEventNotifKey() (string, bool) {
	if n.UeIpv4Addr != "" {
		return n.UeIpv4Addr, true
	}
	if n.UeIpv6Prefix != "" {
		return n.UeIpv6Prefix, true
	}
	if n.UeMacAddr != "" {
		return n.UeMacAddr, true
	}
	return "[UPF_Notification] The UE Identifier is not set", false
}

//
//func (n *NotificationItem) MarshalJSON() ([]byte, error) {
//	return json.Marshal(n)
//}

func (u *UserDataUsageMeasurements) GetAppIdOk() (string, bool) {
	if u == nil || u.AppID == "" {
		return "", false
	}
	return u.AppID, true
}
func (u *UserDataUsageMeasurements) GetFlowInfoOk() (*FlowInformation, bool) {
	if u == nil || u.FlowInfo == nil {
		return nil, false
	}
	return u.FlowInfo, true
}
func (u *UserDataUsageMeasurements) GetVolumeMeasurementOk() (*VolumeMeasurement, bool) {
	if u == nil || u.VolumeMeasurement == nil {
		return nil, false
	}
	return u.VolumeMeasurement, true
}
func (u *UserDataUsageMeasurements) GetThroughputMeasurementOk() (*ThroughputMeasurement, bool) {
	if u == nil || u.ThroughputMeasurement == nil {
		return nil, false
	}
	return u.ThroughputMeasurement, true
}
func (u *UserDataUsageMeasurements) GetApplicationInformationk() (*ApplicationRelatedInformation, bool) {
	if u == nil || u.ApplicationRelatedInformation == nil {
		return nil, false
	}
	return u.ApplicationRelatedInformation, true
}
func (u *UserDataUsageMeasurements) GetThroughputStatisticsMeasurementOk() (*ThroughputStatisticsMeasurement, bool) {
	if u == nil || u.ThroughputStatisticsMeasurement == nil {
		return nil, false
	}
	return u.ThroughputStatisticsMeasurement, true
}
