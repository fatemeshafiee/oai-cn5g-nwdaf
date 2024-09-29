package upf_client

import (
	"time"
)

type UpfEventTrigger string

const (
	ONE_TIME UpfEventTrigger = "ONE_TIME"
	PERIODIC UpfEventTrigger = "PERIODIC"
)

type PartitioningCriteria string

const (
	TAC     PartitioningCriteria = "TAC"
	SUBPLMN PartitioningCriteria = "SUBPLMN"
	GEOAREA PartitioningCriteria = "GEOAREA"
	SNSSAI  PartitioningCriteria = "SNSSAI"
	DNN     PartitioningCriteria = "DNN"
)

type NotificationFlag string

const (
	ACTIVATE   NotificationFlag = "ACTIVATE"
	DEACTIVATE NotificationFlag = "DEACTIVATE"
	RETRIEVAL  NotificationFlag = "RETRIEVAL"
)

type BufferedNotificationsAction string

const (
	SEND_ALL    BufferedNotificationsAction = "SEND_ALL"
	DISCARD_ALL BufferedNotificationsAction = "DISCARD_ALL"
	DROP_OLD    BufferedNotificationsAction = "DROP_OLD"
)

type SubscriptionAction string

const (
	CLOSE                   SubscriptionAction = "CLOSE"
	CONTINUE_WITH_MUTING    SubscriptionAction = "CONTINUE_WITH_MUTING"
	CONTINUE_WITHOUT_MUTING SubscriptionAction = "CONTINUE_WITHOUT_MUTING"
)

type MutingExcInstructions struct {
	SubscriptionInstructions         SubscriptionAction          `json:"subscription"`
	BufferedNotificationInstructions BufferedNotificationsAction `json:"bufferedNotifs"`
}

type EventReportingMode struct {
	Trigger               UpfEventTrigger        `json:"trigger"`
	MaxReports            int                    `json:"maxReports"`
	SentReports           int                    `json:"-"`
	Expiry                string                 `json:"expiry"`
	RepPeriod             int                    `json:"repPeriod"`
	SampRatio             int                    `json:"sampRatio"`
	PartitioningCriteria  []PartitioningCriteria `json:"partitioningCriteria"`
	NotifFlag             NotificationFlag       `json:"notifFlag"`
	MutingExcInstructions MutingExcInstructions  `json:"mutingExcInstructions"`
	TimeOfLastReport      time.Time              `json:"-"`
	TimeOfSubscription    time.Time              `json:"-"`
}

type EventType string

const (
	QOS_MONITORING           EventType = "QOS_MONITORING"
	USER_DATA_USAGE_MEASURES EventType = "USER_DATA_USAGE_MEASURES"
	USER_DATA_USAGE_TRENDS   EventType = "USER_DATA_USAGE_TRENDS"
	TSC_MNGT_INFO            EventType = "TSC_MNGT_INFO"
)

type MeasurementType string

const (
	VOLUME_MEASUREMENT       MeasurementType = "VOLUME_MEASUREMENT"
	THROUGHPUT_MEASUREMENT   MeasurementType = "THROUGHPUT_MEASUREMENT"
	APPLICATION_RELATED_INFO MeasurementType = "APPLICATION_RELATED_INFO"
)

type FlowDirection string

const (
	DOWNLINK      FlowDirection = "DOWNLINK"
	UPLINK        FlowDirection = "UPLINK"
	BIDIRECTIONAL FlowDirection = "BIDIRECTIONAL"
	UNSPECIFIED   FlowDirection = "UNSPECIFIED"
)

type GranularityOfMeasurement string

const (
	PER_APPLICATION GranularityOfMeasurement = "PER_APPLICATION"
	PER_SESSION     GranularityOfMeasurement = "PER_SESSION"
	PER_FLOW        GranularityOfMeasurement = "PER_FLOW"
)

type ReportingUrgency string

const (
	DELAY_TOLERANT     ReportingUrgency = "DELAY_TOLERANT"
	NON_DELAY_TOLERANT ReportingUrgency = "NON_DELAY_TOLERANT"
)

type EthFlowDescription struct {
	DestMacAddr    string        `json:"destMacAddr"`
	EthType        string        `json:"ethType"`
	FDesc          string        `json:"fDesc"`
	FDir           FlowDirection `json:"fDir"`
	SourceMacAddr  string        `json:"sourceMacAddr"`
	VlanTags       []string      `json:"vlanTags"`
	SrcMacAddrEnd  string        `json:"srcMacAddrEnd"`
	DestMacAddrEnd string        `json:"destMacAddrEnd"`
}

type FlowInformation struct {
	FlowDescription    string              `json:"flowDescription"`
	EthFlowDescription *EthFlowDescription `json:"ethFlowDescription"`
	PackFiltId         string              `json:"packFiltId"`
	PacketFilterUsage  bool                `json:"packetFilterUsage"`
	TosTrafficClass    string              `json:"tosTrafficClass"`
	Spi                string              `json:"spi"`
	FlowLabel          string              `json:"flowLabel"`
	FDir               FlowDirection       `json:"flowDirection"`
}

type ReportingSuggestionInformation struct {
	ReportingUrgency  ReportingUrgency `json:"reportingUrgency"`
	ReportingTimeInfo int              `json:"reportingTimeInfo"`
}

type UpfEvent struct {
	Type                     EventType                      `json:"type"`
	ImmediateFlag            bool                           `json:"immediateFlag"`
	MeasurementTypes         []MeasurementType              `json:"measurementTypes"`
	AppIds                   []string                       `json:"appIds"`
	TrafficFilters           []FlowInformation              `json:"trafficFilters"`
	GranularityOfMeasurement GranularityOfMeasurement       `json:"granularityOfMeasurement"`
	ReportingSuggestionInfo  ReportingSuggestionInformation `json:"reportingSuggestionInfo"`
}

type Snssai struct {
	Sst uint32 `json:"sst"`
	Sd  string `json:"sd"`
}

type UeIpAddressVersion string

const (
	V4       UeIpAddressVersion = "V4"
	V6       UeIpAddressVersion = "V6"
	V6Prefix UeIpAddressVersion = "V6Prefix"
)

type UeIpAddress struct {
	Ipv4Addr   string `json:"ipv4Addr"`
	Ipv6Addr   string `json:"ipv6Addr"`
	Ipv6Prefix string `json:"ipv6Prefix"`
}

type UpfEventSubscription struct {
	EventList           []UpfEvent         `json:"eventList"`
	EventNotifyUri      string             `json:"eventNotifyUri"`
	NotifyCorrelationId string             `json:"notifyCorrelationId"`
	EventReportingMode  EventReportingMode `json:"eventReportingMode"`
	NfId                string             `json:"nfId"`
	UeIpAddressVersion  UeIpAddressVersion `json:"ueIpAddressVersion"`
	UeIpAddress         UeIpAddress        `json:"ueIpAddress"`
	Supi                string             `json:"supi"`
	Gpsi                string             `json:"gpsi"`
	Pei                 string             `json:"pei"`
	AnyUe               bool               `json:"anyUe"`
	Dnn                 string             `json:"dnn"`
	Snssai              Snssai             `json:"snssai"`
}
type SubscriptionRequest struct {
	Subscription      UpfEventSubscription `json:"subscription"`
	SupportedFeatures string               `json:"supportedFeatures"`
}

func NewNupfEventExposure(NfId string, EventNotifyUri string, Triger UpfEventTrigger, NotifyCorrelationId string, RequestedEventTypes []EventType) *SubscriptionRequest {
	this := SubscriptionRequest{}
	this.Subscription.EventNotifyUri = EventNotifyUri
	this.Subscription.NfId = NfId
	this.Subscription.NotifyCorrelationId = NotifyCorrelationId
	this.Subscription.EventReportingMode.Trigger = Triger
	//this.Subscription.EventReportingMode.RepPeriod = 3

	for i := 0; i < len(RequestedEventTypes); i++ {
		Upfevent := UpfEvent{Type: RequestedEventTypes[i], ImmediateFlag: false}
		this.Subscription.EventList = append(this.Subscription.EventList, Upfevent)
	}
	return &this
}

// EventList
func (u *UpfEventSubscription) GetEventList() []UpfEvent {
	return u.EventList
}

func (u *UpfEventSubscription) SetEventList(eventList []UpfEvent) {
	u.EventList = eventList
}

// EventNotifyUri
func (u *UpfEventSubscription) GetEventNotifyUri() string {
	return u.EventNotifyUri
}

func (u *UpfEventSubscription) SetEventNotifyUri(eventNotifyUri string) {
	u.EventNotifyUri = eventNotifyUri
}

// NotifyCorrelationId
func (u *UpfEventSubscription) GetNotifyCorrelationId() string {
	return u.NotifyCorrelationId
}

func (u *UpfEventSubscription) SetNotifyCorrelationId(notifyCorrelationId string) {
	u.NotifyCorrelationId = notifyCorrelationId
}

// EventReportingMode
func (u *UpfEventSubscription) GetEventReportingMode() EventReportingMode {
	return u.EventReportingMode
}

func (u *UpfEventSubscription) SetEventReportingMode(eventReportingMode EventReportingMode) {
	u.EventReportingMode = eventReportingMode
}

// NfId
func (u *UpfEventSubscription) GetNfId() string {
	return u.NfId
}

func (u *UpfEventSubscription) SetNfId(nfId string) {
	u.NfId = nfId
}

// UeIpAddressVersion
func (u *UpfEventSubscription) GetUeIpAddressVersion() UeIpAddressVersion {
	return u.UeIpAddressVersion
}

func (u *UpfEventSubscription) SetUeIpAddressVersion(ueIpAddressVersion UeIpAddressVersion) {
	u.UeIpAddressVersion = ueIpAddressVersion
}

// UeIpAddress
func (u *UpfEventSubscription) GetUeIpAddress() UeIpAddress {
	return u.UeIpAddress
}

func (u *UpfEventSubscription) SetUeIpAddress(ueIpAddress UeIpAddress) {
	u.UeIpAddress = ueIpAddress
}

// Supi
func (u *UpfEventSubscription) GetSupi() string {
	return u.Supi
}

func (u *UpfEventSubscription) SetSupi(supi string) {
	u.Supi = supi
}

// Gpsi
func (u *UpfEventSubscription) GetGpsi() string {
	return u.Gpsi
}

func (u *UpfEventSubscription) SetGpsi(gpsi string) {
	u.Gpsi = gpsi
}

// Pei
func (u *UpfEventSubscription) GetPei() string {
	return u.Pei
}

func (u *UpfEventSubscription) SetPei(pei string) {
	u.Pei = pei
}

// AnyUe
func (u *UpfEventSubscription) GetAnyUe() bool {
	return u.AnyUe
}

func (u *UpfEventSubscription) SetAnyUe(anyUe bool) {
	u.AnyUe = anyUe
}

// Dnn
func (u *UpfEventSubscription) GetDnn() string {
	return u.Dnn
}

func (u *UpfEventSubscription) SetDnn(dnn string) {
	u.Dnn = dnn
}

// Snssai
func (u *UpfEventSubscription) GetSnssai() Snssai {
	return u.Snssai
}

func (u *UpfEventSubscription) SetSnssai(snssai Snssai) {
	u.Snssai = snssai
}

func (s *Snssai) GetSst() uint32 {
	return s.Sst
}

func (s *Snssai) SetSst(sst uint32) {
	s.Sst = sst
}

// Sd
func (s *Snssai) GetSd() string {
	return s.Sd
}

func (s *Snssai) SetSd(sd string) {
	s.Sd = sd
}

// Type
func (u *UpfEvent) GetType() EventType {
	return u.Type
}

func (u *UpfEvent) SetType(t EventType) {
	u.Type = t
}

// ImmediateFlag
func (u *UpfEvent) GetImmediateFlag() bool {
	return u.ImmediateFlag
}

func (u *UpfEvent) SetImmediateFlag(flag bool) {
	u.ImmediateFlag = flag
}

// MeasurementTypes
func (u *UpfEvent) GetMeasurementTypes() []MeasurementType {
	return u.MeasurementTypes
}

func (u *UpfEvent) SetMeasurementTypes(measurementTypes []MeasurementType) {
	u.MeasurementTypes = measurementTypes
}

// AppIds
func (u *UpfEvent) GetAppIds() []string {
	return u.AppIds
}

func (u *UpfEvent) SetAppIds(appIds []string) {
	u.AppIds = appIds
}

// TrafficFilters
func (u *UpfEvent) GetTrafficFilters() []FlowInformation {
	return u.TrafficFilters
}

func (u *UpfEvent) SetTrafficFilters(trafficFilters []FlowInformation) {
	u.TrafficFilters = trafficFilters
}

// GranularityOfMeasurement
func (u *UpfEvent) GetGranularityOfMeasurement() GranularityOfMeasurement {
	return u.GranularityOfMeasurement
}

func (u *UpfEvent) SetGranularityOfMeasurement(granularity GranularityOfMeasurement) {
	u.GranularityOfMeasurement = granularity
}

// ReportingSuggestionInfo
func (u *UpfEvent) GetReportingSuggestionInfo() ReportingSuggestionInformation {
	return u.ReportingSuggestionInfo
}

func (u *UpfEvent) SetReportingSuggestionInfo(info ReportingSuggestionInformation) {
	u.ReportingSuggestionInfo = info
}

// ReportingUrgency
func (r *ReportingSuggestionInformation) GetReportingUrgency() ReportingUrgency {
	return r.ReportingUrgency
}

func (r *ReportingSuggestionInformation) SetReportingUrgency(urgency ReportingUrgency) {
	r.ReportingUrgency = urgency
}

// ReportingTimeInfo
func (r *ReportingSuggestionInformation) GetReportingTimeInfo() int {
	return r.ReportingTimeInfo
}

func (r *ReportingSuggestionInformation) SetReportingTimeInfo(timeInfo int) {
	r.ReportingTimeInfo = timeInfo
}

// FlowDescription
func (f *FlowInformation) GetFlowDescription() string {
	return f.FlowDescription
}

func (f *FlowInformation) SetFlowDescription(flowDescription string) {
	f.FlowDescription = flowDescription
}

// EthFlowDescription
func (f *FlowInformation) GetEthFlowDescription() *EthFlowDescription {
	return f.EthFlowDescription
}

func (f *FlowInformation) SetEthFlowDescription(ethFlowDescription *EthFlowDescription) {
	f.EthFlowDescription = ethFlowDescription
}

// PackFiltId
func (f *FlowInformation) GetPackFiltId() string {
	return f.PackFiltId
}

func (f *FlowInformation) SetPackFiltId(packFiltId string) {
	f.PackFiltId = packFiltId
}

// PacketFilterUsage
func (f *FlowInformation) GetPacketFilterUsage() bool {
	return f.PacketFilterUsage
}

func (f *FlowInformation) SetPacketFilterUsage(packetFilterUsage bool) {
	f.PacketFilterUsage = packetFilterUsage
}

// TosTrafficClass
func (f *FlowInformation) GetTosTrafficClass() string {
	return f.TosTrafficClass
}

func (f *FlowInformation) SetTosTrafficClass(tosTrafficClass string) {
	f.TosTrafficClass = tosTrafficClass
}

// Spi
func (f *FlowInformation) GetSpi() string {
	return f.Spi
}

func (f *FlowInformation) SetSpi(spi string) {
	f.Spi = spi
}

// FlowLabel
func (f *FlowInformation) GetFlowLabel() string {
	return f.FlowLabel
}

func (f *FlowInformation) SetFlowLabel(flowLabel string) {
	f.FlowLabel = flowLabel
}

// FDir (FlowDirection)
func (f *FlowInformation) GetFDir() FlowDirection {
	return f.FDir
}

func (f *FlowInformation) SetFDir(fDir FlowDirection) {
	f.FDir = fDir
}

// DestMacAddr
func (e *EthFlowDescription) GetDestMacAddr() string {
	return e.DestMacAddr
}

func (e *EthFlowDescription) SetDestMacAddr(destMacAddr string) {
	e.DestMacAddr = destMacAddr
}

// EthType
func (e *EthFlowDescription) GetEthType() string {
	return e.EthType
}

func (e *EthFlowDescription) SetEthType(ethType string) {
	e.EthType = ethType
}

// FDesc
func (e *EthFlowDescription) GetFDesc() string {
	return e.FDesc
}

func (e *EthFlowDescription) SetFDesc(fDesc string) {
	e.FDesc = fDesc
}

// FDir (FlowDirection)
func (e *EthFlowDescription) GetFDir() FlowDirection {
	return e.FDir
}

func (e *EthFlowDescription) SetFDir(fDir FlowDirection) {
	e.FDir = fDir
}

// SourceMacAddr
func (e *EthFlowDescription) GetSourceMacAddr() string {
	return e.SourceMacAddr
}

func (e *EthFlowDescription) SetSourceMacAddr(sourceMacAddr string) {
	e.SourceMacAddr = sourceMacAddr
}

// VlanTags
func (e *EthFlowDescription) GetVlanTags() []string {
	return e.VlanTags
}

func (e *EthFlowDescription) SetVlanTags(vlanTags []string) {
	e.VlanTags = vlanTags
}

// SrcMacAddrEnd
func (e *EthFlowDescription) GetSrcMacAddrEnd() string {
	return e.SrcMacAddrEnd
}

func (e *EthFlowDescription) SetSrcMacAddrEnd(srcMacAddrEnd string) {
	e.SrcMacAddrEnd = srcMacAddrEnd
}

// DestMacAddrEnd
func (e *EthFlowDescription) GetDestMacAddrEnd() string {
	return e.DestMacAddrEnd
}

func (e *EthFlowDescription) SetDestMacAddrEnd(destMacAddrEnd string) {
	e.DestMacAddrEnd = destMacAddrEnd
}

// Trigger
func (e *EventReportingMode) GetTrigger() UpfEventTrigger {
	return e.Trigger
}

func (e *EventReportingMode) SetTrigger(trigger UpfEventTrigger) {
	e.Trigger = trigger
}

// MaxReports
func (e *EventReportingMode) GetMaxReports() int {
	return e.MaxReports
}

func (e *EventReportingMode) SetMaxReports(maxReports int) {
	e.MaxReports = maxReports
}

// SentReports
func (e *EventReportingMode) GetSentReports() int {
	return e.SentReports
}

func (e *EventReportingMode) SetSentReports(sentReports int) {
	e.SentReports = sentReports
}

// Expiry
func (e *EventReportingMode) GetExpiry() string {
	return e.Expiry
}

func (e *EventReportingMode) SetExpiry(expiry string) {
	e.Expiry = expiry
}

// RepPeriod
func (e *EventReportingMode) GetRepPeriod() int {
	return e.RepPeriod
}

func (e *EventReportingMode) SetRepPeriod(repPeriod int) {
	e.RepPeriod = repPeriod
}

// SampRatio
func (e *EventReportingMode) GetSampRatio() int {
	return e.SampRatio
}

func (e *EventReportingMode) SetSampRatio(sampRatio int) {
	e.SampRatio = sampRatio
}

// PartitioningCriteria
func (e *EventReportingMode) GetPartitioningCriteria() []PartitioningCriteria {
	return e.PartitioningCriteria
}

func (e *EventReportingMode) SetPartitioningCriteria(criteria []PartitioningCriteria) {
	e.PartitioningCriteria = criteria
}

// NotifFlag
func (e *EventReportingMode) GetNotifFlag() NotificationFlag {
	return e.NotifFlag
}

func (e *EventReportingMode) SetNotifFlag(notifFlag NotificationFlag) {
	e.NotifFlag = notifFlag
}

// MutingExcInstructions
func (e *EventReportingMode) GetMutingExcInstructions() MutingExcInstructions {
	return e.MutingExcInstructions
}

func (e *EventReportingMode) SetMutingExcInstructions(instructions MutingExcInstructions) {
	e.MutingExcInstructions = instructions
}

// TimeOfLastReport
func (e *EventReportingMode) GetTimeOfLastReport() time.Time {
	return e.TimeOfLastReport
}

func (e *EventReportingMode) SetTimeOfLastReport(lastReport time.Time) {
	e.TimeOfLastReport = lastReport
}

// TimeOfSubscription
func (e *EventReportingMode) GetTimeOfSubscription() time.Time {
	return e.TimeOfSubscription
}

func (e *EventReportingMode) SetTimeOfSubscription(subscriptionTime time.Time) {
	e.TimeOfSubscription = subscriptionTime
}

// SubscriptionInstructions
func (m *MutingExcInstructions) GetSubscriptionInstructions() SubscriptionAction {
	return m.SubscriptionInstructions
}

func (m *MutingExcInstructions) SetSubscriptionInstructions(subscriptionInstructions SubscriptionAction) {
	m.SubscriptionInstructions = subscriptionInstructions
}

// BufferedNotificationInstructions
func (m *MutingExcInstructions) GetBufferedNotificationInstructions() BufferedNotificationsAction {
	return m.BufferedNotificationInstructions
}

func (m *MutingExcInstructions) SetBufferedNotificationInstructions(bufferedNotifs BufferedNotificationsAction) {
	m.BufferedNotificationInstructions = bufferedNotifs
}
