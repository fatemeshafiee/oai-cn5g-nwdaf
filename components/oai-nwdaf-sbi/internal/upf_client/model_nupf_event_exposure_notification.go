package upf_client

import "time"

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
	AppID                           string                          `json:"appID"`
	FlowInfo                        FlowInformation                 `json:"flowInfo"`
	VolumeMeasurement               VolumeMeasurement               `json:"volumeMeasurement"`
	ThroughputMeasurement           ThroughputMeasurement           `json:"throughputMeasurement"`
	ApplicationRelatedInformation   ApplicationRelatedInformation   `json:"applicationRelatedInformation"`
	ThroughputStatisticsMeasurement ThroughputStatisticsMeasurement `json:"throughputStatisticsMeasurement"`
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
	NotificationItems []NotificationItem `json:"notificationItems"`
	CorrelationId     string             `json:"correlationId"`
	AchievedSampRatio int                `json:"achievedSampRatio"`
}
