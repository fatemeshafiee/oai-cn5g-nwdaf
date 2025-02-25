from enum import Enum
from pydantic import BaseModel, Field, root_validator, field_validator, model_validator,  UUID4, HttpUrl
from typing import Union, Optional, List
from datetime import datetime
from pydantic import RootModel

class NfInstanceId(BaseModel):
    nfInstanceId: UUID4

class FailureCodeEnum(str, Enum):
    UNAVAILABLE_ML_MODEL = "UNAVAILABLE_ML_MODEL"

class FailureCode(BaseModel):
    description: str = "Represents the failure code."
    failure_code: Union[FailureCodeEnum, str] = Field(
        ...,
        description="Enum for known failure codes, or a custom string for future extensions."
    )

class MLModelMetricEnum(str, Enum):
    ACCURACY = "ACCURACY"

class MLModelMetric(BaseModel):
    description: str = "Represents the metric of the ML model."
    failure_code: Union[MLModelMetricEnum, str] = Field(
        ...,
        description="Enum for known ML Model Metrics or a custom string for future extensions."
    )


class DataSetTag(BaseModel):

    dataSetId: str = Field(... )
    dataSetDesc: str = Field(None)

class InferenceDataForModelTrain(BaseModel):
    adrfId : Optional[str] = Field(None)
    adrfSetId: Optional[str] = Field(None)
    dataSetTag: Optional[DataSetTag] = Field(None)
    modelId: Optional[int] = Field(None)
    class Config:
        schema_extra = {
            "oneOf": [
                {"required": ["adrfId"]},
                {"required": ["adrfSetId"]}
            ]
        }


class NwdafEventEnum(str, Enum):
    SLICE_LOAD_LEVEL = "SLICE_LOAD_LEVEL"
    NETWORK_PERFORMANCE = "NETWORK_PERFORMANCE"
    NF_LOAD = "NF_LOAD"
    SERVICE_EXPERIENCE = "SERVICE_EXPERIENCE"
    UE_MOBILITY = "UE_MOBILITY"
    UE_COMMUNICATION = "UE_COMMUNICATION"
    QOS_SUSTAINABILITY = "QOS_SUSTAINABILITY"
    ABNORMAL_BEHAVIOUR = "ABNORMAL_BEHAVIOUR"
    USER_DATA_CONGESTION = "USER_DATA_CONGESTION"
    NSI_LOAD_LEVEL = "NSI_LOAD_LEVEL"
    DN_PERFORMANCE = "DN_PERFORMANCE"
    DISPERSION = "DISPERSION"
    RED_TRANS_EXP = "RED_TRANS_EXP"
    WLAN_PERFORMANCE = "WLAN_PERFORMANCE"
    SM_CONGESTION = "SM_CONGESTION"
    PFD_DETERMINATION = "PFD_DETERMINATION"
    PDU_SESSION_TRAFFIC = "PDU_SESSION_TRAFFIC"
    E2E_DATA_VOL_TRANS_TIME = "E2E_DATA_VOL_TRANS_TIME"
    MOVEMENT_BEHAVIOUR = "MOVEMENT_BEHAVIOUR"
    LOC_ACCURACY = "LOC_ACCURACY"
    RELATIVE_PROXIMITY = "RELATIVE_PROXIMITY"


class NwdafEvent(BaseModel):

    event: Union[NwdafEventEnum, str] = Field(
        ...,
        description="Enum for known NWDAF events, or a custom string for future extensions."
    )


class Snssai(BaseModel):


    sst: int = Field(
        ...,
        ge=0, le=255
    )

    sd: Optional[str] = Field(
        None,
        pattern="^[A-Fa-f0-9]{6}$"
    )



class PlmnIdNid(BaseModel):


    mcc: str = Field(
        ...,
        pattern="^\\d{3}$"
    )

    mnc: str = Field(
        ...,
        pattern="^\\d{2,3}$"
    )

    nid: Optional[str] = Field(
        None,
        pattern="^[A-Fa-f0-9]{11}$"
    )

class PlmnId(BaseModel):


    mcc: str = Field(
        ...,
        pattern="^\\d{3}$"
    )

    mnc: str = Field(
        ...,
        pattern="^\\d{2,3}$"
    )


class CivicAddress(BaseModel):

    country: Optional[str] = Field(None)
    A1: Optional[str] = Field(None)
    A2: Optional[str] = Field(None)
    A3: Optional[str] = Field(None)
    A4: Optional[str] = Field(None)
    A5: Optional[str] = Field(None)
    A6: Optional[str] = Field(None)
    PRD: Optional[str] = Field(None)
    POD: Optional[str] = Field(None)
    STS: Optional[str] = Field(None)
    HNO: Optional[str] = Field(None)
    HNS: Optional[str] = Field(None)
    LMK: Optional[str] = Field(None)
    LOC: Optional[str] = Field(None)
    NAM: Optional[str] = Field(None)
    PC: Optional[str] = Field(None)
    BLD: Optional[str] = Field(None)
    UNIT: Optional[str] = Field(None)
    FLR: Optional[str] = Field(None)
    ROOM: Optional[str] = Field(None)
    PLC: Optional[str] = Field(None)
    PCN: Optional[str] = Field(None)
    POBOX: Optional[str] = Field(None)
    ADDCODE: Optional[str] = Field(None)
    SEAT: Optional[str] = Field(None)
    RD: Optional[str] = Field(None)
    RDSEC: Optional[str] = Field(None)
    RDBR: Optional[str] = Field(None)
    RDSUBBR: Optional[str] = Field(None)
    PRM: Optional[str] = Field(None)
    POM: Optional[str] = Field(None)
    usageRules: Optional[str] = Field(None)
    method: Optional[str] = Field(None)
    providedBy: Optional[str] = Field(None)


class SupportedGADShapesEnum(str, Enum):
    POINT = "POINT"
    POINT_UNCERTAINTY_CIRCLE = "POINT_UNCERTAINTY_CIRCLE"
    POINT_UNCERTAINTY_ELLIPSE = "POINT_UNCERTAINTY_ELLIPSE"
    POLYGON = "POLYGON"
    POINT_ALTITUDE = "POINT_ALTITUDE"
    POINT_ALTITUDE_UNCERTAINTY = "POINT_ALTITUDE_UNCERTAINTY"
    ELLIPSOID_ARC = "ELLIPSOID_ARC"
    LOCAL_2D_POINT_UNCERTAINTY_ELLIPSE = "LOCAL_2D_POINT_UNCERTAINTY_ELLIPSE"
    LOCAL_3D_POINT_UNCERTAINTY_ELLIPSOID = "LOCAL_3D_POINT_UNCERTAINTY_ELLIPSOID"
    DISTANCE_DIRECTION = "DISTANCE_DIRECTION"
    RELATIVE_2D_LOCATION_UNCERTAINTY_ELLIPSE = "RELATIVE_2D_LOCATION_UNCERTAINTY_ELLIPSE"
    RELATIVE_3D_LOCATION_UNCERTAINTY_ELLIPSOID = "RELATIVE_3D_LOCATION_UNCERTAINTY_ELLIPSOID"

class SupportedGADShapes(BaseModel):

    shape: Union[SupportedGADShapesEnum, str] = Field(
        ...
    )



class GeographicalCoordinates(BaseModel):

    lon: float = Field(
        ...,
        ge=-180, le=180
    )

    lat: float = Field(
        ...,
        ge=-90, le=90
    )


class Point(BaseModel):

    shape: SupportedGADShapes = Field(...)
    point: GeographicalCoordinates = Field(...)


class PointUncertaintyCircle(BaseModel):

    shape: SupportedGADShapes = Field(...)

    point: GeographicalCoordinates = Field(...)

    uncertainty: float = Field(
        ...,
        ge=0
    )

class UncertaintyEllipse(BaseModel):

    semiMajor: float = Field(
        ...,
        ge=0
    )

    semiMinor: float = Field(
        ...,
        ge=0
    )

    orientationMajor: int = Field(
        ...,
        ge=0, le=180
    )


class PointUncertaintyEllipse(BaseModel):

    shape: SupportedGADShapes = Field(
        ...
    )

    point: GeographicalCoordinates = Field(
        ...
    )

    uncertaintyEllipse: UncertaintyEllipse = Field(
        ...
    )

    confidence: int = Field(
        ...,
        ge=0, le=100
    )


class Polygon(BaseModel):

    shape: SupportedGADShapes = Field(
        ...
    )

    pointList: List[GeographicalCoordinates] = Field(
        ...,
        min_items=3, max_items=15
    )


class PointAltitude(BaseModel):

    shape: SupportedGADShapes = Field(
        ...
    )

    point: GeographicalCoordinates = Field(
        ...
    )

    altitude: float = Field(
        ...,
        ge=-32767, le=32767
    )


class PointAltitudeUncertainty(BaseModel):


    shape: SupportedGADShapes = Field(
        ...
    )

    point: GeographicalCoordinates = Field(
        ...
    )

    altitude: float = Field(
        ...,
        ge=-32767, le=32767
    )

    uncertaintyEllipse: UncertaintyEllipse = Field(
        ...
    )

    uncertaintyAltitude: float = Field(
        ...,
        ge=0
    )

    confidence: int = Field(
        ...,
        ge=0, le=100
    )

    vConfidence: int = Field(
        ...,
        ge=0, le=100
    )



class EllipsoidArc(BaseModel):
    shape: SupportedGADShapes = Field(...)

    point: GeographicalCoordinates = Field(...)

    innerRadius: int = Field(
        ...,
        ge=0, le=327675
    )

    uncertaintyRadius: float = Field(
        ...,
        ge=0
    )

    offsetAngle: int = Field(
        ...,
        ge=0, le=360
    )

    includedAngle: int = Field(
        ...,
        ge=0, le=360
    )

    confidence: int = Field(
        ...,
        ge=0, le=100
    )

class GeographicArea(RootModel):
    root: Union[
        Point,
        PointUncertaintyCircle,
        PointUncertaintyEllipse,
        Polygon,
        PointAltitude,
        PointAltitudeUncertainty,
        EllipsoidArc
    ]


class RoamingInfo(BaseModel):
    plmnId: PlmnIdNid = Field(...)

    aois: List[GeographicArea] = Field(
        ...,
        min_items=1,
        description="Areas of Interest in the HPLMN or the VPLMN."
    )

    servingNfIds: List[NfInstanceId] = Field(
        ...,
        min_items=1,
        description="NF ID(s) of the NF(s) serving the roaming UE(s) in the VPLMN."
    )

    servingNfSetIds: List[str] = Field(
        ...,
        min_items=1,
        description="NF Set ID(s) of the NF Set(s) serving the roaming UE(s) in the VPLMN."
    )

class LocalOrigin(BaseModel):
    coordinateId: Optional[str] = Field(None)
    point: Optional[GeographicalCoordinates] = Field(None)


class RelativeCartesianLocation(BaseModel):
    x: float = Field(..., description="Float number representing the x-coordinate.")
    y: float = Field(..., description="Float number representing the y-coordinate.")
    z: Optional[float] = Field(None, description="Float number representing the z-coordinate.")

class GeoLocation(BaseModel):
    point: Optional[Point] = Field(None)
    pointAlt: Optional[PointAltitude] = Field(None)
    refPoint: Optional[LocalOrigin] = Field(None)
    localCoords: Optional[RelativeCartesianLocation] = Field(None)

    @model_validator(mode="before")
    @classmethod
    def validate_geo_location(cls, values):
        point = values.get("point")
        pointAlt = values.get("pointAlt")
        refPoint = values.get("refPoint")
        localCoords = values.get("localCoords")

        # ✅ Ensure at least one valid combination exists
        if not any([point, pointAlt, (refPoint and localCoords)]):
            raise ValueError("GeoLocation must include either 'point', 'pointAlt', or both 'refPoint' and 'localCoords'.")

        # ✅ Ensure 'refPoint' and 'localCoords' are provided together
        if (refPoint and not localCoords) or (localCoords and not refPoint):
            raise ValueError("Both 'refPoint' and 'localCoords' must be provided together.")

        return values


class Ecgi(BaseModel):
    plmnId: PlmnId = Field(...)
    eutraCellId: str = Field(..., pattern="^[A-Fa-f0-9]{7}$")
    nid: Optional[str] = Field(None, pattern="^[A-Fa-f0-9]{11}$")

class Ncgi(BaseModel):
    plmnId: PlmnId = Field(...)
    nrCellId: str = Field(..., pattern="^[A-Fa-f0-9]{9}$")
    nid: Optional[str] = Field(None, pattern="^[A-Fa-f0-9]{11}$")

class GNbId(BaseModel):
    bitLength: int = Field(..., ge=22, le=32)
    gNBValue: str = Field(..., pattern="^[A-Fa-f0-9]{6,8}$")

class GlobalRanNodeId(BaseModel):
    plmnId: PlmnId = Field(...)

    n3IwfId: Optional[str] = Field(
        None, pattern="^[A-Fa-f0-9]+$"
    )

    gNbId: Optional[GNbId] = None

    ngeNbId: Optional[str] = Field(
        None, pattern="^(MacroNGeNB-[A-Fa-f0-9]{5}|LMacroNGeNB-[A-Fa-f0-9]{6}|SMacroNGeNB-[A-Fa-f0-9]{5})$"
    )

    wagfId: Optional[str] = Field(
        None, pattern="^[A-Fa-f0-9]+$"
    )

    tngfId: Optional[str] = Field(
        None, pattern="^[A-Fa-f0-9]+$"
    )

    nid: Optional[str] = Field(
        None, pattern="^[A-Fa-f0-9]{11}$"
    )

    eNbId: Optional[str] = Field(
        None, pattern="^(MacroeNB-[A-Fa-f0-9]{5}|LMacroeNB-[A-Fa-f0-9]{6}|SMacroeNB-[A-Fa-f0-9]{5}|HomeeNB-[A-Fa-f0-9]{7})$"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_one_of_fields(cls, values):
        fields = ["n3IwfId", "gNbId", "ngeNbId", "wagfId", "tngfId", "eNbId"]
        present_fields = [field for field in fields if values.get(field) is not None]

        if len(present_fields) != 1:
            raise ValueError(f"Exactly one of {fields} must be present. Found: {present_fields}")

        return values


class Tai(BaseModel):
    plmnId: PlmnId = Field(...)
    tac: str = Field(..., pattern="(^[A-Fa-f0-9]{4}$)|(^[A-Fa-f0-9]{6}$)")
    nid: Optional[str] = Field(None, pattern="^[A-Fa-f0-9]{11}$")


class NetworkAreaInfo(BaseModel):
    ecgis: Optional[List[Ecgi]] = Field( None, min_items=1)
    ncgis: Optional[List[Ncgi]] = Field(None, min_items=1)
    gRanNodeIds: Optional[List[GlobalRanNodeId]] = Field(None, min_items=1)
    tais: Optional[List[Tai]] = Field(None, min_items=1)

class GeographicalArea(BaseModel):
    civicAddress: Optional[CivicAddress] = None
    shapes: Optional[GeographicArea] = None


class NFTypeEnum(str, Enum):
    NRF = "NRF"
    UDM = "UDM"
    AMF = "AMF"
    SMF = "SMF"
    AUSF = "AUSF"
    NEF = "NEF"
    PCF = "PCF"
    SMSF = "SMSF"
    NSSF = "NSSF"
    UDR = "UDR"
    LMF = "LMF"
    GMLC = "GMLC"
    _5G_EIR = "5G_EIR"
    SEPP = "SEPP"
    UPF = "UPF"
    N3IWF = "N3IWF"
    AF = "AF"
    UDSF = "UDSF"
    BSF = "BSF"
    CHF = "CHF"
    NWDAF = "NWDAF"
    PCSCF = "PCSCF"
    CBCF = "CBCF"
    HSS = "HSS"
    UCMF = "UCMF"
    SOR_AF = "SOR_AF"
    SPAF = "SPAF"
    MME = "MME"
    SCSAS = "SCSAS"
    SCEF = "SCEF"
    SCP = "SCP"
    NSSAAF = "NSSAAF"
    ICSCF = "ICSCF"
    SCSCF = "SCSCF"
    DRA = "DRA"
    IMS_AS = "IMS_AS"
    AANF = "AANF"
    _5G_DDNMF = "5G_DDNMF"
    NSACF = "NSACF"
    MFAF = "MFAF"
    EASDF = "EASDF"
    DCCF = "DCCF"
    MB_SMF = "MB_SMF"
    TSCTSF = "TSCTSF"
    ADRF = "ADRF"
    GBA_BSF = "GBA_BSF"
    CEF = "CEF"
    MB_UPF = "MB_UPF"
    NSWOF = "NSWOF"
    PKMF = "PKMF"
    MNPF = "MNPF"
    SMS_GMSC = "SMS_GMSC"
    SMS_IWMSC = "SMS_IWMSC"
    MBSF = "MBSF"
    MBSTF = "MBSTF"
    PANF = "PANF"
    IP_SM_GW = "IP_SM_GW"
    SMS_ROUTER = "SMS_ROUTER"
    DCSF = "DCSF"
    MRF = "MRF"
    MRFP = "MRFP"
    MF = "MF"
    SLPKMF = "SLPKMF"
    RH = "RH"

class NFType(BaseModel):
    nfType: Union[NFTypeEnum, str] = Field(
        ..., description="Enum for known NF types or a custom string for future extensions."
    )

class DeviceTypeEnum(str, Enum):
    MOBILE_PHONE = "MOBILE_PHONE"
    SMART_PHONE = "SMART_PHONE"
    TABLET = "TABLET"
    DONGLE = "DONGLE"
    MODEM = "MODEM"
    WLAN_ROUTER = "WLAN_ROUTER"
    IOT_DEVICE = "IOT_DEVICE"
    WEARABLE = "WEARABLE"
    MOBILE_TEST_PLATFORM = "MOBILE_TEST_PLATFORM"
    UNDEFINED = "UNDEFINED"


class NsiIdInfo(BaseModel):
    snssai: Snssai = Field(...)

    nsiIds: Optional[List[str]] = Field(None, min_items=1)

class QosResourceTypeEnum(str, Enum):
    NON_GBR = "NON_GBR"
    NON_CRITICAL_GBR = "NON_CRITICAL_GBR"
    CRITICAL_GBR = "CRITICAL_GBR"

class QosResourceType(BaseModel):
    qosResourceType: Union[QosResourceTypeEnum, str] = Field(
        ..., description="Enum for known QoS resource types or a custom string for future extensions."
    )

class HorizontalVelocity(BaseModel):
    hSpeed: float = Field(
        ..., ge=0, le=2047
    )

    bearing: int = Field(
        ..., ge=0, le=360
    )

class VerticalDirectionEnum(str, Enum):
    UPWARD = "UPWARD"
    DOWNWARD = "DOWNWARD"

class VerticalDirection(BaseModel):
    verticalDirection: Union[VerticalDirectionEnum, str] = Field(
        ..., description="Enum for known vertical directions or a custom string for future extensions."
    )

class HorizontalWithVerticalVelocity(BaseModel):
    hSpeed: float = Field(
        ..., ge=0, le=2047
    )

    bearing: int = Field(
        ..., ge=0, le=360
    )

    vSpeed: float = Field(
        ..., ge=0, le=255
    )

    vDirection: VerticalDirectionEnum = Field(...)


class HorizontalVelocityWithUncertainty(BaseModel):
    hSpeed: float = Field(
        ..., ge=0, le=2047
    )

    bearing: int = Field(
        ..., ge=0, le=360
    )

    hUncertainty: float = Field(
        ..., ge=0, le=255
    )


class HorizontalWithVerticalVelocityAndUncertainty(BaseModel):
    hSpeed: float = Field(
        ..., ge=0, le=2047
    )

    bearing: int = Field(
        ..., ge=0, le=360
    )

    vSpeed: float = Field(
        ..., ge=0, le=255
    )

    vDirection: VerticalDirectionEnum = Field(...)

    hUncertainty: float = Field(
        ..., ge=0, le=255
    )

    vUncertainty: float = Field(
        ..., ge=0, le=255
    )

class VelocityEstimate(RootModel):
    root: Union[
        HorizontalVelocity,
        HorizontalWithVerticalVelocity,
        HorizontalVelocityWithUncertainty,
        HorizontalWithVerticalVelocityAndUncertainty
    ]

class QosRequirement(BaseModel):
    five_qi: Optional[int] = Field(
        None, ge=0, le=255
    )

    gfbrUl: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

    gfbrDl: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

    resType: Optional[QosResourceTypeEnum] = None

    pdb: Optional[int] = Field(
        None, ge=1
    )

    per: Optional[str] = Field(
        None, pattern=r"^([0-9]E-[0-9])$"
    )

    deviceSpeed: Optional[VelocityEstimate] = None

    deviceType: Optional[DeviceTypeEnum] = None

    @classmethod
    def validate(cls, values):
        if "_5qi" not in values and "resType" not in values:
            raise ValueError("One of '5qi' or 'resType' must be present.")
        return values


class NetworkPerfOrderCriterionEnum(str, Enum):
    NUMBER_OF_UES = "NUMBER_OF_UES"
    COMMUNICATION_PERF = "COMMUNICATION_PERF"
    MOBILITY_PERF = "MOBILITY_PERF"

class NetworkPerfOrderCriterion(BaseModel):
    orderCriterion: Union[NetworkPerfOrderCriterionEnum, str] = Field(
        ..., description="Enum for known network performance order criteria or a custom string for future extensions."
    )

class MatchingDirectionEnum(str, Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
    CROSSED = "CROSSED"

class MatchingDirection(BaseModel):
    matchingDirection: Union[MatchingDirectionEnum, str] = Field(
        ..., description="Enum for known matching directions or a custom string for future extensions."
    )



class NetworkPerfReq(BaseModel):
    orderCriterion: Optional[NetworkPerfOrderCriterion] = Field(...)
    orderDirection: Optional[MatchingDirection] = Field(...)

class NetworkPerfTypeEnum(str, Enum):
    GNB_ACTIVE_RATIO = "GNB_ACTIVE_RATIO"
    GNB_COMPUTING_USAGE = "GNB_COMPUTING_USAGE"
    GNB_MEMORY_USAGE = "GNB_MEMORY_USAGE"
    GNB_DISK_USAGE = "GNB_DISK_USAGE"
    GNB_RSC_USAGE_OVERALL_TRAFFIC = "GNB_RSC_USAGE_OVERALL_TRAFFIC"
    GNB_RSC_USAGE_GBR_TRAFFIC = "GNB_RSC_USAGE_GBR_TRAFFIC"
    GNB_RSC_USAGE_DELAY_CRIT_GBR_TRAFFIC = "GNB_RSC_USAGE_DELAY_CRIT_GBR_TRAFFIC"
    NUM_OF_UE = "NUM_OF_UE"
    SESS_SUCC_RATIO = "SESS_SUCC_RATIO"
    HO_SUCC_RATIO = "HO_SUCC_RATIO"

class NetworkPerfType(BaseModel):
    networkPerfType: Union[NetworkPerfTypeEnum, str] = Field(
        ..., description="Enum for known network performance types or a custom string for future extensions."
    )

class TrafficDirectionEnum(str, Enum):
    UL_AND_DL = "UL_AND_DL"
    UL = "UL"
    DL = "DL"

class TrafficDirection(BaseModel):
    trafficDirection: Union[TrafficDirectionEnum, str] = Field(
        ..., description="Enum for known traffic directions or a custom string for future extensions."
    )

class ValueExpressionEnum(str, Enum):
    AVERAGE = "AVERAGE"
    PEAK = "PEAK"

class ValueExpression(BaseModel):
    valueExpression: Union[ValueExpressionEnum, str] = Field(
        ..., description="Enum for known value expressions or a custom string for future extensions."
    )

class ResourceUsageRequirement(BaseModel):
    tfcDirc: Optional[TrafficDirection] = None
    valExp: Optional[ValueExpression] = None

class ResourceUsageRequPerNwPerfType(BaseModel):
    nwPerfType: NetworkPerfType = Field(...)
    rscUsgReq: Optional[ResourceUsageRequirement] = None

class UserDataConOrderCritEnum(str, Enum):
    APPLICABLE_TIME_WINDOW = "APPLICABLE_TIME_WINDOW"
    NETWORK_STATUS_INDICATION = "NETWORK_STATUS_INDICATION"

class UserDataConOrderCrit(BaseModel):
    orderCriterion: Union[UserDataConOrderCritEnum, str] = Field(
        ..., description="Enum for known user data congestion order criteria or a custom string for future extensions."
    )

class UserDataCongestReq(BaseModel):
    orderCriterion: Optional[UserDataConOrderCrit] = None
    orderDirection: Optional[MatchingDirection] = None

class BwRequirement(BaseModel):
    appId: str = Field(
        ..., description="String providing an application identifier."
    )

    marBwDl: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

    marBwUl: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

    mirBwDl: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

    mirBwUl: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

class ExceptionIdEnum(str, Enum):
    UNEXPECTED_UE_LOCATION = "UNEXPECTED_UE_LOCATION"
    UNEXPECTED_LONG_LIVE_FLOW = "UNEXPECTED_LONG_LIVE_FLOW"
    UNEXPECTED_LARGE_RATE_FLOW = "UNEXPECTED_LARGE_RATE_FLOW"
    UNEXPECTED_WAKEUP = "UNEXPECTED_WAKEUP"
    SUSPICION_OF_DDOS_ATTACK = "SUSPICION_OF_DDOS_ATTACK"
    WRONG_DESTINATION_ADDRESS = "WRONG_DESTINATION_ADDRESS"
    TOO_FREQUENT_SERVICE_ACCESS = "TOO_FREQUENT_SERVICE_ACCESS"
    UNEXPECTED_RADIO_LINK_FAILURES = "UNEXPECTED_RADIO_LINK_FAILURES"
    PING_PONG_ACROSS_CELLS = "PING_PONG_ACROSS_CELLS"

class ExceptionId(BaseModel):
    exceptionId: Union[ExceptionIdEnum, str] = Field(
        ..., description="Enum for known exception IDs or a custom string for future extensions."
    )

class ExpectedAnalyticsTypeEnum(str, Enum):
    MOBILITY = "MOBILITY"
    COMMUN = "COMMUN"
    MOBILITY_AND_COMMUN = "MOBILITY_AND_COMMUN"

class ExpectedAnalyticsType(BaseModel):
    expectedAnalyticsType: Union[ExpectedAnalyticsTypeEnum, str] = Field(
        ..., description="Enum for known expected UE analytics types or a custom string for future extensions."
    )

class StationaryIndicationEnum(str, Enum):
    STATIONARY = "STATIONARY"
    MOBILE = "MOBILE"

class StationaryIndication(BaseModel):
    stationaryIndication: Union[StationaryIndicationEnum, str] = Field(
        ..., description="Enum for known stationary indications or a custom string for future extensions."
    )

class ScheduledCommunicationTime(BaseModel):
    daysOfWeek: Optional[List[int]] = Field(
        None, min_items=1, max_items=6, ge=1, le=7
    )

    timeOfDayStart: Optional[str] = Field(
        None, pattern=r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)?$"
    )

    timeOfDayEnd: Optional[str] = Field(
        None, pattern=r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)?$"
    )

class ScheduledCommunicationTypeEnum(str, Enum):
    DOWNLINK_ONLY = "DOWNLINK_ONLY"
    UPLINK_ONLY = "UPLINK_ONLY"
    BIDIRECTIONAL = "BIDIRECTIONAL"

class ScheduledCommunicationType(BaseModel):
    scheduledCommunicationType: Union[ScheduledCommunicationTypeEnum, str] = Field(
        ..., description="Enum for known scheduled communication types or a custom string for future extensions."
    )

class UmtTime(BaseModel):
    timeOfDay: str = Field(
        ...,
        pattern=r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)?$"
    )

    dayOfWeek: int = Field(
        ..., ge=1, le=7
    )

class LocationArea(BaseModel):
    geographicAreas: Optional[List[GeographicalArea]] = Field(None, min_items=0)
    civicAddresses: Optional[List[CivicAddress]] = Field(None, min_items=0)
    nwAreaInfo: Optional[NetworkAreaInfo] = None
    umtTime: Optional[UmtTime] = None

class TrafficProfileEnum(str, Enum):
    SINGLE_TRANS_UL = "SINGLE_TRANS_UL"
    SINGLE_TRANS_DL = "SINGLE_TRANS_DL"
    DUAL_TRANS_UL_FIRST = "DUAL_TRANS_UL_FIRST"
    DUAL_TRANS_DL_FIRST = "DUAL_TRANS_DL_FIRST"
    MULTI_TRANS = "MULTI_TRANS"

class TrafficProfile(BaseModel):
    trafficProfile: Union[TrafficProfileEnum, str] = Field(
        ..., description="Enum for known traffic profiles or a custom string for future extensions."
    )

class BatteryIndication(BaseModel):
    batteryInd: bool = Field(..., description="Indicates whether the UE is battery powered.")
    replaceableInd: Optional[bool] = Field(
        None, description="Indicates whether the battery of the UE is replaceable."
    )
    rechargeableInd: Optional[bool] = Field(
        None, description="Indicates whether the battery of the UE is rechargeable."
    )

    @staticmethod
    def validate(cls, values):
        if not values.get("batteryInd"):
            values["replaceableInd"] = None
            values["rechargeableInd"] = None
        return values



class ExpectedUeBehaviourData(BaseModel):
    stationaryIndication: Optional[StationaryIndication] = None
    communicationDurationTime: Optional[int] = Field(None, ge=0, description="Time in seconds.")
    periodicTime: Optional[int] = Field(None, ge=0, description="Time in seconds.")
    scheduledCommunicationTime: Optional[ScheduledCommunicationTime] = None
    scheduledCommunicationType: Optional[ScheduledCommunicationType] = None
    expectedUmts: Optional[List[UmtTime]] = None
    trafficProfile: Optional[TrafficProfile] = None
    batteryIndication: Optional[BatteryIndication] = None
    validityTime: Optional[datetime] = None
    confidenceLevel: Optional[str] = Field(
        None, pattern=r"^[0]\.[0-9]{2}$|^1\.00$", description="A floating value between 0.00 and 1.00."
    )
    accuracyLevel: Optional[str] = Field(
        None, pattern=r"^[0]\.[0-9]{2}$|^1\.00$", description="A floating value between 0.00 and 1.00."
    )

class RatTypeEnum(str, Enum):
    NR = "NR"
    EUTRA = "EUTRA"
    WLAN = "WLAN"
    VIRTUAL = "VIRTUAL"
    NBIOT = "NBIOT"
    WIRELINE = "WIRELINE"
    WIRELINE_CABLE = "WIRELINE_CABLE"
    WIRELINE_BBF = "WIRELINE_BBF"
    LTE_M = "LTE-M"
    NR_U = "NR_U"
    EUTRA_U = "EUTRA_U"
    TRUSTED_N3GA = "TRUSTED_N3GA"
    TRUSTED_WLAN = "TRUSTED_WLAN"
    UTRA = "UTRA"
    GERA = "GERA"
    NR_LEO = "NR_LEO"
    NR_MEO = "NR_MEO"
    NR_GEO = "NR_GEO"
    NR_OTHER_SAT = "NR_OTHER_SAT"
    NR_REDCAP = "NR_REDCAP"
    WB_E_UTRAN_LEO = "WB_E_UTRAN_LEO"
    WB_E_UTRAN_MEO = "WB_E_UTRAN_MEO"
    WB_E_UTRAN_GEO = "WB_E_UTRAN_GEO"
    WB_E_UTRAN_OTHERSAT = "WB_E_UTRAN_OTHERSAT"
    NB_IOT_LEO = "NB_IOT_LEO"
    NB_IOT_MEO = "NB_IOT_MEO"
    NB_IOT_GEO = "NB_IOT_GEO"
    NB_IOT_OTHERSAT = "NB_IOT_OTHERSAT"
    LTE_M_LEO = "LTE_M_LEO"
    LTE_M_MEO = "LTE_M_MEO"
    LTE_M_GEO = "LTE_M_GEO"
    LTE_M_OTHERSAT = "LTE_M_OTHERSAT"
    NR_EREDCAP = "NR_EREDCAP"

class RatType(BaseModel):
    ratType: Union[RatTypeEnum, str] = Field(
        ..., description="Enum for known RAT types or a custom string for future extensions."
    )


class ThresholdLevel(BaseModel):
    congLevel: Optional[int] = None
    nfLoadLevel: Optional[int] = None
    nfCpuUsage: Optional[int] = None
    nfMemoryUsage: Optional[int] = None
    nfStorageUsage: Optional[int] = None

    avgTrafficRate: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )
    maxTrafficRate: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )
    minTrafficRate: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )
    aggTrafficRate: Optional[str] = Field(
        None, pattern=r"^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
    )

    varTrafficRate: Optional[float] = None

    avgPacketDelay: Optional[int] = Field(None, ge=1)
    maxPacketDelay: Optional[int] = Field(None, ge=1)

    varPacketDelay: Optional[float] = None

    avgPacketLossRate: Optional[int] = Field(None, ge=0, le=1000)
    maxPacketLossRate: Optional[int] = Field(None, ge=0, le=1000)

    varPacketLossRate: Optional[float] = None
    svcExpLevel: Optional[float] = None
    speed: Optional[float] = None


class RatFreqInformation(BaseModel):
    allFreq: Optional[bool] = None
    allRat: Optional[bool] = None
    freq: Optional[int] = Field(None, ge=0, le=3279165)
    ratType: Optional[RatType] = None
    svcExpThreshold: Optional[ThresholdLevel] = None
    matchingDir: Optional[MatchingDirection] = None

    @staticmethod
    def validate(cls, values):
        if values.get("allFreq") and values.get("freq") is not None:
            raise ValueError("The 'allFreq' and 'freq' attributes are mutually exclusive.")

        if values.get("allRat") and values.get("ratType") is not None:
            raise ValueError("The 'allRat' and 'ratType' attributes are mutually exclusive.")

        return values

class DispersionOrderingCriterionEnum(str, Enum):
    TIME_SLOT_START = "TIME_SLOT_START"
    DISPERSION = "DISPERSION"
    CLASSIFICATION = "CLASSIFICATION"
    RANKING = "RANKING"
    PERCENTILE_RANKING = "PERCENTILE_RANKING"

class DispersionOrderingCriterion(BaseModel):
    dispersionOrderingCriterion: Union[DispersionOrderingCriterionEnum, str] = Field(
        ..., description="Enum for known dispersion ordering criteria or a custom string for future extensions."
    )

class RankingCriterion(BaseModel):
    highBase: int = Field(
        ..., ge=1, le=100, description="Unsigned integer indicating Sampling Ratio, expressed in percent."
    )

    lowBase: int = Field(
        ..., ge=1, le=100, description="Unsigned integer indicating Sampling Ratio, expressed in percent."
    )

class DispersionClassEnum(str, Enum):
    FIXED = "FIXED"
    CAMPER = "CAMPER"
    TRAVELLER = "TRAVELLER"
    TOP_HEAVY = "TOP_HEAVY"

class DispersionClass(BaseModel):
    dispersionClass: Union[DispersionClassEnum, str] = Field(
        ..., description="Enum for known dispersion classes or a custom string for future extensions."
    )

class ClassCriterion(BaseModel):
    disperClass: DispersionClass = Field(...)
    classThreshold: int = Field(
        ..., ge=1, le=100, description="Unsigned integer indicating Sampling Ratio, expressed in percent."
    )
    thresMatch: MatchingDirection = Field(...)

class DispersionTypeEnum(str, Enum):
    DVDA = "DVDA"
    TDA = "TDA"
    DVDA_AND_TDA = "DVDA_AND_TDA"

class DispersionType(BaseModel):
    dispersionType: Union[DispersionTypeEnum, str] = Field(
        ..., description="Enum for known dispersion types or a custom string for future extensions."
    )

class DispersionRequirement(BaseModel):
    disperType: DispersionType = Field(...)  # Required field

    classCriters: Optional[List[ClassCriterion]] = Field(
        None, min_items=1
    )

    rankCriters: Optional[List[RankingCriterion]] = Field(
        None, min_items=1
    )

    dispOrderCriter: Optional[DispersionOrderingCriterion] = None
    order: Optional[MatchingDirection] = None

class RedTransExpOrderingCriterionEnum(str, Enum):
    TIME_SLOT_START = "TIME_SLOT_START"
    RED_TRANS_EXP = "RED_TRANS_EXP"

class RedTransExpOrderingCriterion(BaseModel):
    redTransExpOrderingCriterion: Union[RedTransExpOrderingCriterionEnum, str] = Field(
        ..., description="Enum for known Redundant Transmission Experience ordering criteria or a custom string for future extensions."
    )
class RedundantTransmissionExpReq(BaseModel):
    redTOrderCriter: Optional[RedTransExpOrderingCriterion] = None
    order: Optional[MatchingDirection] = None

class WlanOrderingCriterionEnum(str, Enum):
    TIME_SLOT_START = "TIME_SLOT_START"
    NUMBER_OF_UES = "NUMBER_OF_UES"
    RSSI = "RSSI"
    RTT = "RTT"
    TRAFFIC_INFO = "TRAFFIC_INFO"

class WlanOrderingCriterion(BaseModel):
    wlanOrderingCriterion: Union[WlanOrderingCriterionEnum, str] = Field(
        ..., description="Enum for known WLAN ordering criteria or a custom string for future extensions."
    )

class WlanPerformanceReq(BaseModel):
    ssIds: Optional[List[str]] = Field(None, min_items=1)
    bssIds: Optional[List[str]] = Field(None, min_items=1)
    wlanOrderCriter: Optional[WlanOrderingCriterion] = None
    order: Optional[MatchingDirection] = None


class AnalyticsSubsetEnum(str, Enum):
    NUM_OF_UE_REG = "NUM_OF_UE_REG"
    NUM_OF_PDU_SESS_ESTBL = "NUM_OF_PDU_SESS_ESTBL"
    RES_USAGE = "RES_USAGE"
    NUM_OF_EXCEED_RES_USAGE_LOAD_LEVEL_THR = "NUM_OF_EXCEED_RES_USAGE_LOAD_LEVEL_THR"
    PERIOD_OF_EXCEED_RES_USAGE_LOAD_LEVEL_THR = "PERIOD_OF_EXCEED_RES_USAGE_LOAD_LEVEL_THR"
    EXCEED_LOAD_LEVEL_THR_IND = "EXCEED_LOAD_LEVEL_THR_IND"
    LIST_OF_TOP_APP_UL = "LIST_OF_TOP_APP_UL"
    LIST_OF_TOP_APP_DL = "LIST_OF_TOP_APP_DL"
    NF_STATUS = "NF_STATUS"
    NF_RESOURCE_USAGE = "NF_RESOURCE_USAGE"
    NF_LOAD = "NF_LOAD"
    NF_PEAK_LOAD = "NF_PEAK_LOAD"
    NF_LOAD_AVG_IN_AOI = "NF_LOAD_AVG_IN_AOI"
    DISPER_AMOUNT = "DISPER_AMOUNT"
    DISPER_CLASS = "DISPER_CLASS"
    RANKING = "RANKING"
    PERCENTILE_RANKING = "PERCENTILE_RANKING"
    RSSI = "RSSI"
    RTT = "RTT"
    TRAFFIC_INFO = "TRAFFIC_INFO"
    NUMBER_OF_UES = "NUMBER_OF_UES"
    APP_LIST_FOR_UE_COMM = "APP_LIST_FOR_UE_COMM"
    N4_SESS_INACT_TIMER_FOR_UE_COMM = "N4_SESS_INACT_TIMER_FOR_UE_COMM"
    AVG_TRAFFIC_RATE = "AVG_TRAFFIC_RATE"
    MAX_TRAFFIC_RATE = "MAX_TRAFFIC_RATE"
    AGG_TRAFFIC_RATE = "AGG_TRAFFIC_RATE"
    VAR_TRAFFIC_RATE = "VAR_TRAFFIC_RATE"
    AVG_PACKET_DELAY = "AVG_PACKET_DELAY"
    MAX_PACKET_DELAY = "MAX_PACKET_DELAY"
    VAR_PACKET_DELAY = "VAR_PACKET_DELAY"
    AVG_PACKET_LOSS_RATE = "AVG_PACKET_LOSS_RATE"
    MAX_PACKET_LOSS_RATE = "MAX_PACKET_LOSS_RATE"
    VAR_PACKET_LOSS_RATE = "VAR_PACKET_LOSS_RATE"
    UE_LOCATION = "UE_LOCATION"
    LIST_OF_HIGH_EXP_UE = "LIST_OF_HIGH_EXP_UE"
    LIST_OF_MEDIUM_EXP_UE = "LIST_OF_MEDIUM_EXP_UE"
    LIST_OF_LOW_EXP_UE = "LIST_OF_LOW_EXP_UE"
    AVG_UL_PKT_DROP_RATE = "AVG_UL_PKT_DROP_RATE"
    VAR_UL_PKT_DROP_RATE = "VAR_UL_PKT_DROP_RATE"
    AVG_DL_PKT_DROP_RATE = "AVG_DL_PKT_DROP_RATE"
    VAR_DL_PKT_DROP_RATE = "VAR_DL_PKT_DROP_RATE"
    AVG_UL_PKT_DELAY = "AVG_UL_PKT_DELAY"
    VAR_UL_PKT_DELAY = "VAR_UL_PKT_DELAY"
    AVG_DL_PKT_DELAY = "AVG_DL_PKT_DELAY"
    VAR_DL_PKT_DELAY = "VAR_DL_PKT_DELAY"
    TRAFFIC_MATCH_TD = "TRAFFIC_MATCH_TD"
    TRAFFIC_UNMATCH_TD = "TRAFFIC_UNMATCH_TD"
    NUMBER_OF_UE = "NUMBER_OF_UE"
    UE_GEOG_DIST = "UE_GEOG_DIST"
    UE_DIRECTION = "UE_DIRECTION"
    AVG_E2E_UL_PKT_DELAY = "AVG_E2E_UL_PKT_DELAY"
    VAR_E2E_UL_PKT_DELAY = "VAR_E2E_UL_PKT_DELAY"
    AVG_E2E_DL_PKT_DELAY = "AVG_E2E_DL_PKT_DELAY"
    VAR_E2E_DL_PKT_DELAY = "VAR_E2E_DL_PKT_DELAY"
    AVG_E2E_UL_PKT_LOSS_RATE = "AVG_E2E_UL_PKT_LOSS_RATE"
    VAR_E2E_UL_PKT_LOSS_RATE = "VAR_E2E_UL_PKT_LOSS_RATE"
    AVG_E2E_DL_PKT_LOSS_RATE = "AVG_E2E_DL_PKT_LOSS_RATE"
    VAR_E2E_DL_PKT_LOSS_RATE = "VAR_E2E_DL_PKT_LOSS_RATE"
    E2E_DATA_VOL_TRANS_TIME_FOR_UE_LIST = "E2E_DATA_VOL_TRANS_TIME_FOR_UE_LIST"
    IN_OUT_PERCENT = "IN_OUT_PERCENT"
    TIME_TO_COLLISION = "TIME_TO_COLLISION"

class AnalyticsSubset(BaseModel):
    analyticsSubset: Union[AnalyticsSubsetEnum, str] = Field(
        ..., description="Enum for known analytics subsets or a custom string for future extensions."
    )


class IpAddr(BaseModel):
    ipv4Addr: Optional[str] = Field(
        None,
        pattern=r"^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
    )

    ipv6Addr: Optional[str] = Field(
        None,
        pattern=r"^((([^:]+:){7}([^:]+))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?))$"
    )

    ipv6Prefix: Optional[str] = Field(
        None,
        pattern=r"^((([^:]+:){7}([^:]+))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?))(\/.+)$"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        provided_fields = [field for field in ["ipv4Addr", "ipv6Addr", "ipv6Prefix"] if values.get(field) is not None]

        if len(provided_fields) != 1:
            raise ValueError(f"Exactly one of 'ipv4Addr', 'ipv6Addr', or 'ipv6Prefix' must be provided. Found: {provided_fields}")

        return values


class AddrFqdn(BaseModel):
    ipAddr: Optional[IpAddr] = None
    fqdn: Optional[str] = None

class UpfInformation(BaseModel):
    upfId: Optional[str] = None
    upfAddr: Optional[AddrFqdn] = None

class DnPerfOrderingCriterionEnum(str, Enum):
    AVERAGE_TRAFFIC_RATE = "AVERAGE_TRAFFIC_RATE"
    MAXIMUM_TRAFFIC_RATE = "MAXIMUM_TRAFFIC_RATE"
    AVERAGE_PACKET_DELAY = "AVERAGE_PACKET_DELAY"
    MAXIMUM_PACKET_DELAY = "MAXIMUM_PACKET_DELAY"
    AVERAGE_PACKET_LOSS_RATE = "AVERAGE_PACKET_LOSS_RATE"

class DnPerfOrderingCriterion(BaseModel):
    dnPerfOrderingCriterion: Union[DnPerfOrderingCriterionEnum, str] = Field(
        ..., description="Enum for known DN performance ordering criteria or a custom string for future extensions."
    )

class DnPerformanceReq(BaseModel):
    dnPerfOrderCriter: Optional[DnPerfOrderingCriterion] = None
    order: Optional[MatchingDirection] = None
    reportThresholds: Optional[List[ThresholdLevel]] = Field(None, min_items=1)

class UeMobilityOrderCriterionEnum(str, Enum):
    TIME_SLOT = "TIME_SLOT"

class UeMobilityOrderCriterion(BaseModel):
    ueMobilityOrderCriterion: Union[UeMobilityOrderCriterionEnum, str] = Field(
        ..., description="Enum for known UE mobility ordering criteria or a custom string for future extensions."
    )

class UeCommOrderCriterionEnum(str, Enum):
    START_TIME = "START_TIME"
    DURATION = "DURATION"

class UeCommOrderCriterion(BaseModel):
    ueCommOrderCriterion: Union[UeCommOrderCriterionEnum, str] = Field(
        ..., description="Enum for known UE communication ordering criteria or a custom string for future extensions."
    )
class UeMobilityReq(BaseModel):
    orderCriterion: Optional[UeMobilityOrderCriterion] = None
    orderDirection: Optional[MatchingDirection] = None
    ueLocOrderInd: Optional[bool] = None

    distThresholds: Optional[List[int]] = Field(
        None, min_items=1, description="List of linear distance thresholds, must be 0 or greater."
    )
class UeCommReq(BaseModel):
    orderCriterion: Optional[UeCommOrderCriterion] = None
    orderDirection: Optional[MatchingDirection] = None

class PduSessionTypeEnum(str, Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    IPV4V6 = "IPV4V6"
    UNSTRUCTURED = "UNSTRUCTURED"
    ETHERNET = "ETHERNET"

class PduSessionType(BaseModel):
    pduSessionType: Union[PduSessionTypeEnum, str] = Field(
        ..., description="Enum for known PDU session types or a custom string for future extensions."
    )

class SscModeEnum(str, Enum):
    SSC_MODE_1 = "SSC_MODE_1"
    SSC_MODE_2 = "SSC_MODE_2"
    SSC_MODE_3 = "SSC_MODE_3"

class SscMode(BaseModel):
    sscMode: Union[SscModeEnum, str] = Field(
        ..., description="Enum for known SSC modes or a custom string for future extensions."
    )

class AccessTypeEnum(str, Enum):
    _3GPP_ACCESS = "3GPP_ACCESS"
    NON_3GPP_ACCESS = "NON_3GPP_ACCESS"

class AccessType(BaseModel):
    accessType: Union[AccessTypeEnum, str] = Field(
        ..., description="Enum for known access types or a custom string for future extensions."
    )
class PduSessionInfo(BaseModel):
    pduSessType: Optional[PduSessionType] = None
    sscMode: Optional[SscMode] = None
    accessTypes: Optional[List[AccessType]] = Field(None, min_items=1)

class PduSesTrafficReq(BaseModel):
    flowDescs: Optional[List[str]] = Field(None, min_items=1, description="Indicates traffic flow filtering description(s) for IP flow(s).")
    appId: Optional[str] = None
    domainDescs: Optional[List[str]] = Field(None, min_items=1, description="FQDN(s) or a regular expression used as domain name matching criteria.")

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        provided_fields = [
            field for field in ["flowDescs", "appId", "domainDescs"] if values.get(field) is not None
        ]

        if len(provided_fields) != 1:
            raise ValueError(f"Exactly one of 'flowDescs', 'appId', or 'domainDescs' must be provided. Found: {provided_fields}")

        return values

class PositioningMethodEnum(str, Enum):
    CELLID = "CELLID"
    ECID = "ECID"
    OTDOA = "OTDOA"
    BAROMETRIC_PRESSURE = "BAROMETRIC_PRESSURE"
    WLAN = "WLAN"
    BLUETOOTH = "BLUETOOTH"
    MBS = "MBS"
    MOTION_SENSOR = "MOTION_SENSOR"
    DL_TDOA = "DL_TDOA"
    DL_AOD = "DL_AOD"
    MULTI_RTT = "MULTI-RTT"
    NR_ECID = "NR_ECID"
    UL_TDOA = "UL_TDOA"
    UL_AOA = "UL_AOA"
    NETWORK_SPECIFIC = "NETWORK_SPECIFIC"
    SL_TDOA = "SL_TDOA"
    SL_TOA = "SL_TOA"
    SL_AOA = "SL_AoA"
    SL_RT = "SL_RT"

class PositioningMethod(BaseModel):
    positioningMethod: Union[PositioningMethodEnum, str] = Field(
        ..., description="Enum for known positioning methods or a custom string for future extensions."
    )


class LocAccuracyReq(BaseModel):
    accThres: Optional[int] = Field(None, ge=0, description="Unsigned integer indicating accuracy threshold.")
    accThresMatchDir: Optional[MatchingDirection] = None
    inOutThres: Optional[int] = Field(None, ge=0, description="Unsigned integer indicating in/out threshold.")
    inOutThresMatchDir: Optional[MatchingDirection] = None
    posMethod: Optional[PositioningMethod] = None

class LocInfoGranularityEnum(str, Enum):
    TA_LEVEL = "TA_LEVEL"
    CELL_LEVEL = "CELL_LEVEL"
    LON_AND_LAT_LEVEL = "LON_AND_LAT_LEVEL"

class LocInfoGranularity(BaseModel):
    locInfoGranularity: Union[LocInfoGranularityEnum, str] = Field(
        ..., description="Enum for known location information granularities or a custom string for future extensions."
    )
class LocationOrientationEnum(str, Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"
    HOR_AND_VER = "HOR_AND_VER"

class LocationOrientation(BaseModel):
    locationOrientation: Union[LocationOrientationEnum, str] = Field(
        ..., description="Enum for known location orientations or a custom string for future extensions."
    )

class E2eDataVolTransTimeCriterionEnum(str, Enum):
    TIME_SLOT_START = "TIME_SLOT_START"
    E2E_DATA_VOL_TRANS_TIME = "E2E_DATA_VOL_TRANS_TIME"

class E2eDataVolTransTimeCriterion(BaseModel):
    e2eDataVolTransTimeCriterion: Union[E2eDataVolTransTimeCriterionEnum, str] = Field(
        ..., description="Enum for known E2E data volume transfer time criteria or a custom string for future extensions."
    )

class E2eDataVolTransTimeReq(BaseModel):
    criterion: Optional[E2eDataVolTransTimeCriterion] = None
    order: Optional[MatchingDirection] = None
    highTransTmThr: Optional[int] = Field(None, ge=0, description="Unsigned integer for high transmission time threshold.")
    lowTransTmThr: Optional[int] = Field(None, ge=0, description="Unsigned integer for low transmission time threshold.")
    repeatDataTrans: Optional[int] = Field(None, ge=0, description="Unsigned integer for repeated data transmissions.")
    tsIntervalDataTrans: Optional[datetime] = None
    dataVolume: Optional[int] = Field(None, ge=0, description="Unsigned integer for data volume.")
    maxNumberUes: Optional[int] = Field(None, ge=0, description="Unsigned integer for the maximum number of UEs.")

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        provided_fields = [
            field for field in ["repeatDataTrans", "tsIntervalDataTrans"] if values.get(field) is not None
        ]

        if len(provided_fields) != 1:
            raise ValueError(f"Exactly one of 'repeatDataTrans' or 'tsIntervalDataTrans' must be provided. Found: {provided_fields}")

        return values

class TimeWindow(BaseModel):
    startTime: datetime = Field(..., description="Start time of the time window in 'date-time' format as defined in OpenAPI.")
    stopTime: datetime = Field(..., description="Stop time of the time window in 'date-time' format as defined in OpenAPI.")

class AccuracyReq(BaseModel):
    accuTimeWin: Optional[TimeWindow] = None
    accuPeriod: Optional[int] = Field(None, ge=0, description="Time period in seconds.")
    accuDevThr: Optional[int] = Field(None, ge=0, description="Unsigned integer, representing deviation threshold.")
    minNum: Optional[int] = Field(None, ge=0, description="Unsigned integer, representing minimum number required.")
    updatedAnaFlg: Optional[bool] = Field(
        None, description="Indicates if NWDAF can provide updated analytics within the specified accuracy time window."
    )
    correctionInterval: Optional[int] = Field(None, ge=0, description="Time period in seconds for correction interval.")

class MovBehavReq(BaseModel):
    locationGranReq: Optional[LocInfoGranularity] = None
    reportThresholds: Optional[ThresholdLevel] = None

class DirectionEnum(str, Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"
    NORTHWEST = "NORTHWEST"
    NORTHEAST = "NORTHEAST"
    SOUTHWEST = "SOUTHWEST"
    SOUTHEAST = "SOUTHEAST"

class Direction(BaseModel):
    direction: Union[DirectionEnum, str] = Field(
        ..., description="Enum for known directions or a custom string for future extensions."
    )
class ProximityCriterionEnum(str, Enum):
    VELOCITY = "VELOCITY"
    AVG_SPD = "AVG_SPD"
    ORIENTATION = "ORIENTATION"
    TRAJECTORY = "TRAJECTORY"

class ProximityCriterion(BaseModel):
    proximityCriterion: Union[ProximityCriterionEnum, str] = Field(
        ..., description="Enum for known proximity criteria or a custom string for future extensions."
    )

class RelProxReq(BaseModel):
    direction: Optional[List[Direction]] = Field(None, min_items=1, description="List of directions.")
    numOfUe: Optional[int] = Field(None, ge=0, description="Unsigned integer representing the number of UEs.")
    proximityCrits: Optional[List[ProximityCriterion]] = Field(None, min_items=1, description="List of proximity criteria.")


class EventFilter(BaseModel):
    anySlice: Optional[bool] = None
    snssais: Optional[List[Snssai]] = Field(None, min_items=1)
    roamingInfo: Optional[RoamingInfo] = None
    appIds: Optional[List[str]] = Field(None, min_items=1)
    dnns: Optional[List[str]] = Field(None, min_items=1)
    dnais: Optional[List[str]] = Field(None, min_items=1)
    ladnDnns: Optional[List[str]] = Field(None, min_items=1)
    location: Optional[GeoLocation] = None
    networkArea: Optional[NetworkAreaInfo] = None
    temporalGranSize: Optional[int] = Field(None, ge=0)
    spatialGranSizeTa: Optional[int] = Field(None, ge=0)
    spatialGranSizeCell: Optional[int] = Field(None, ge=0)
    fineGranAreas: Optional[List[GeographicalArea]] = Field(None, min_items=1)
    visitedAreas: Optional[List[NetworkAreaInfo]] = Field(None, min_items=1)
    maxTopAppUlNbr: Optional[int] = Field(None, ge=0)
    maxTopAppDlNbr: Optional[int] = Field(None, ge=0)
    nfInstanceIds: Optional[List[str]] = Field(None, min_items=1)
    nfSetIds: Optional[List[str]] = Field(None, min_items=1)
    nfTypes: Optional[List[NFType]] = Field(None, min_items=1)
    nsiIdInfos: Optional[List[NsiIdInfo]] = Field(None, min_items=1)
    qosRequ: Optional[QosRequirement] = None
    nwPerfReqs: Optional[List[NetworkPerfReq]] = Field(None, min_items=1)
    nwPerfTypes: Optional[List[NetworkPerfType]] = Field(None, min_items=1)
    addNwPerfReqs: Optional[List[ResourceUsageRequPerNwPerfType]] = Field(None, min_items=1)
    userDataConReqs: Optional[List[UserDataCongestReq]] = Field(None, min_items=1)
    bwRequs: Optional[List[BwRequirement]] = Field(None, min_items=1)
    excepIds: Optional[List[ExceptionId]] = Field(None, min_items=1)
    exptAnaType: Optional[ExpectedAnalyticsType] = None
    exptUeBehav: Optional[ExpectedUeBehaviourData] = None
    ratFreqs: Optional[List[RatFreqInformation]] = Field(None, min_items=1)
    disperReqs: Optional[List[DispersionRequirement]] = Field(None, min_items=1)
    redTransReqs: Optional[List[RedundantTransmissionExpReq]] = Field(None, min_items=1)
    wlanReqs: Optional[List[WlanPerformanceReq]] = Field(None, min_items=1)
    listOfAnaSubsets: Optional[List[AnalyticsSubset]] = Field(None, min_items=1)
    upfInfo: Optional[UpfInformation] = None
    appServerAddrs: Optional[List[AddrFqdn]] = Field(None, min_items=1)
    dnPerfReqs: Optional[List[DnPerformanceReq]] = Field(None, min_items=1)
    ueMobilityReqs: Optional[List[UeMobilityReq]] = Field(None, min_items=1)
    ueCommReqs: Optional[List[UeCommReq]] = Field(None, min_items=1)
    pduSesInfos: Optional[List[PduSessionInfo]] = Field(None, min_items=1)
    pduSesTrafReqs: Optional[List[PduSesTrafficReq]] = Field(None, min_items=1)
    locAccReqs: Optional[List[LocAccuracyReq]] = Field(None, min_items=1)
    locGranularity: Optional[LocInfoGranularity] = None
    locOrientation: Optional[LocationOrientation] = None
    useCaseCxt: Optional[str] = None
    dataVlTrnsTmRqs: Optional[List[E2eDataVolTransTimeReq]] = Field(None, min_items=1)
    accuReq: Optional[AccuracyReq] = None
    movBehavReqs: Optional[List[MovBehavReq]] = Field(None, min_items=1)
    relProxReqs: Optional[List[RelProxReq]] = Field(None, min_items=1)
    @model_validator(mode="before")
    @classmethod
    def validate_not_anySlice_and_snssais(cls, values):
        if values.get("anySlice") is not None and values.get("snssais") is not None:
            raise ValueError("Cannot provide both 'anySlice' and 'snssais' together.")
        return values
class TargetUeInformation(BaseModel):
    anyUe: Optional[bool] = Field(
        None
    )

    supis: Optional[List[str]] = Field(
        None,
        min_items=1,
        pattern=r"^(imsi-[0-9]{5,15}|nai-.+|gci-.+|gli-.+|.+)$"
    )

    gpsis: Optional[List[str]] = Field(
        None,
        min_items=1,
        pattern=r"^(msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|.+)$"
    )

    intGroupIds: Optional[List[str]] = Field(
        None,
        min_items=1,
        pattern=r"^[A-Fa-f0-9]{8}-[0-9]{3}-[0-9]{2,3}-([A-Fa-f0-9][A-Fa-f0-9]){1,10}$"
    )


class MLRepEventCondition(BaseModel):
    mlTrainRound: Optional[int] = Field(
        None, ge=0, description="Unsigned integer indicating the number of ML training rounds (0 or greater)."
    )

    mlTrainRepTime: Optional[TimeWindow] = None

    mlAccuracyThreshold: Optional[int] = Field(
        None, ge=0, description="Unsigned integer indicating the ML accuracy threshold (0 or greater)."
    )

    modelMetric: Optional[MLModelMetric] = None

class NwdafEventEnum(str, Enum):
    SLICE_LOAD_LEVEL = "SLICE_LOAD_LEVEL"
    NETWORK_PERFORMANCE = "NETWORK_PERFORMANCE"
    NF_LOAD = "NF_LOAD"
    SERVICE_EXPERIENCE = "SERVICE_EXPERIENCE"
    UE_MOBILITY = "UE_MOBILITY"
    UE_COMMUNICATION = "UE_COMMUNICATION"
    QOS_SUSTAINABILITY = "QOS_SUSTAINABILITY"
    ABNORMAL_BEHAVIOUR = "ABNORMAL_BEHAVIOUR"
    USER_DATA_CONGESTION = "USER_DATA_CONGESTION"
    NSI_LOAD_LEVEL = "NSI_LOAD_LEVEL"
    DN_PERFORMANCE = "DN_PERFORMANCE"
    DISPERSION = "DISPERSION"
    RED_TRANS_EXP = "RED_TRANS_EXP"
    WLAN_PERFORMANCE = "WLAN_PERFORMANCE"
    SM_CONGESTION = "SM_CONGESTION"
    PFD_DETERMINATION = "PFD_DETERMINATION"
    PDU_SESSION_TRAFFIC = "PDU_SESSION_TRAFFIC"
    E2E_DATA_VOL_TRANS_TIME = "E2E_DATA_VOL_TRANS_TIME"
    MOVEMENT_BEHAVIOUR = "MOVEMENT_BEHAVIOUR"
    NUM_OF_UE = "NUM_OF_UE"
    MOV_UE_RATIO = "MOV_UE_RATIO"
    AVR_SPEED = "AVR_SPEED"
    SPEED_THRESHOLD = "SPEED_THRESHOLD"
    MOV_UE_DIRECTION = "MOV_UE_DIRECTION"
    LOC_ACCURACY = "LOC_ACCURACY"
    RELATIVE_PROXIMITY = "RELATIVE_PROXIMITY"

class NwdafEvent(BaseModel):
    nwdafEvent: Union[NwdafEventEnum, str] = Field(...)

class SmfEventEnum(str, Enum):
    AC_TY_CH = "AC_TY_CH"
    UP_PATH_CH = "UP_PATH_CH"
    PDU_SES_REL = "PDU_SES_REL"
    PLMN_CH = "PLMN_CH"
    UE_IP_CH = "UE_IP_CH"
    RAT_TY_CH = "RAT_TY_CH"
    DDDS = "DDDS"
    COMM_FAIL = "COMM_FAIL"
    PDU_SES_EST = "PDU_SES_EST"
    QFI_ALLOC = "QFI_ALLOC"
    QOS_MON = "QOS_MON"
    SMCC_EXP = "SMCC_EXP"
    DISPERSION = "DISPERSION"
    RED_TRANS_EXP = "RED_TRANS_EXP"
    WLAN_INFO = "WLAN_INFO"
    UPF_INFO = "UPF_INFO"
    UP_STATUS_INFO = "UP_STATUS_INFO"
    SATB_CH = "SATB_CH"
    TRAFFIC_CORRELATION = "TRAFFIC_CORRELATION"

class SmfEvent(BaseModel):
    smfEvent: Union[SmfEventEnum, str] = Field(...)

class AmfEventTypeEnum(str, Enum):
    LOCATION_REPORT = "LOCATION_REPORT"
    PRESENCE_IN_AOI_REPORT = "PRESENCE_IN_AOI_REPORT"
    TIMEZONE_REPORT = "TIMEZONE_REPORT"
    ACCESS_TYPE_REPORT = "ACCESS_TYPE_REPORT"
    REGISTRATION_STATE_REPORT = "REGISTRATION_STATE_REPORT"
    CONNECTIVITY_STATE_REPORT = "CONNECTIVITY_STATE_REPORT"
    REACHABILITY_REPORT = "REACHABILITY_REPORT"
    COMMUNICATION_FAILURE_REPORT = "COMMUNICATION_FAILURE_REPORT"
    UES_IN_AREA_REPORT = "UES_IN_AREA_REPORT"
    SUBSCRIPTION_ID_CHANGE = "SUBSCRIPTION_ID_CHANGE"
    SUBSCRIPTION_ID_ADDITION = "SUBSCRIPTION_ID_ADDITION"
    SUBSCRIPTION_TERMINATION = "SUBSCRIPTION_TERMINATION"
    LOSS_OF_CONNECTIVITY = "LOSS_OF_CONNECTIVITY"
    _5GS_USER_STATE_REPORT = "5GS_USER_STATE_REPORT"
    AVAILABILITY_AFTER_DDN_FAILURE = "AVAILABILITY_AFTER_DDN_FAILURE"
    TYPE_ALLOCATION_CODE_REPORT = "TYPE_ALLOCATION_CODE_REPORT"
    FREQUENT_MOBILITY_REGISTRATION_REPORT = "FREQUENT_MOBILITY_REGISTRATION_REPORT"
    SNSSAI_TA_MAPPING_REPORT = "SNSSAI_TA_MAPPING_REPORT"
    UE_LOCATION_TRENDS = "UE_LOCATION_TRENDS"
    UE_ACCESS_BEHAVIOR_TRENDS = "UE_ACCESS_BEHAVIOR_TRENDS"
    UE_MM_TRANSACTION_REPORT = "UE_MM_TRANSACTION_REPORT"

class AmfEventType(BaseModel):
    amfEventType: Union[AmfEventTypeEnum, str] = Field(...)

class NefEventEnum(str, Enum):
    SVC_EXPERIENCE = "SVC_EXPERIENCE"
    UE_MOBILITY = "UE_MOBILITY"
    UE_COMM = "UE_COMM"
    EXCEPTIONS = "EXCEPTIONS"
    USER_DATA_CONGESTION = "USER_DATA_CONGESTION"
    PERF_DATA = "PERF_DATA"
    DISPERSION = "DISPERSION"
    COLLECTIVE_BEHAVIOUR = "COLLECTIVE_BEHAVIOUR"
    MS_QOE_METRICS = "MS_QOE_METRICS"
    MS_CONSUMPTION = "MS_CONSUMPTION"
    MS_NET_ASSIST_INVOCATION = "MS_NET_ASSIST_INVOCATION"
    MS_DYN_POLICY_INVOCATION = "MS_DYN_POLICY_INVOCATION"
    MS_ACCESS_ACTIVITY = "MS_ACCESS_ACTIVITY"
    GNSS_ASSISTANCE_DATA = "GNSS_ASSISTANCE_DATA"
    DATA_VOLUME_TRANSFER_TIME = "DATA_VOLUME_TRANSFER_TIME"

class NefEvent(BaseModel):
    nefEvent: Union[NefEventEnum, str] = Field(...)

class UdmEventEnum(str, Enum):
    LOSS_OF_CONNECTIVITY = "LOSS_OF_CONNECTIVITY"
    UE_REACHABILITY_FOR_DATA = "UE_REACHABILITY_FOR_DATA"
    UE_REACHABILITY_FOR_SMS = "UE_REACHABILITY_FOR_SMS"
    LOCATION_REPORTING = "LOCATION_REPORTING"
    CHANGE_OF_SUPI_PEI_ASSOCIATION = "CHANGE_OF_SUPI_PEI_ASSOCIATION"
    ROAMING_STATUS = "ROAMING_STATUS"
    COMMUNICATION_FAILURE = "COMMUNICATION_FAILURE"
    AVAILABILITY_AFTER_DDN_FAILURE = "AVAILABILITY_AFTER_DDN_FAILURE"
    CN_TYPE_CHANGE = "CN_TYPE_CHANGE"
    DL_DATA_DELIVERY_STATUS = "DL_DATA_DELIVERY_STATUS"
    PDN_CONNECTIVITY_STATUS = "PDN_CONNECTIVITY_STATUS"
    UE_CONNECTION_MANAGEMENT_STATE = "UE_CONNECTION_MANAGEMENT_STATE"
    ACCESS_TYPE_REPORT = "ACCESS_TYPE_REPORT"
    REGISTRATION_STATE_REPORT = "REGISTRATION_STATE_REPORT"
    CONNECTIVITY_STATE_REPORT = "CONNECTIVITY_STATE_REPORT"
    TYPE_ALLOCATION_CODE_REPORT = "TYPE_ALLOCATION_CODE_REPORT"
    FREQUENT_MOBILITY_REGISTRATION_REPORT = "FREQUENT_MOBILITY_REGISTRATION_REPORT"
    PDU_SES_REL = "PDU_SES_REL"
    PDU_SES_EST = "PDU_SES_EST"
    UE_MEMORY_AVAILABLE_FOR_SMS = "UE_MEMORY_AVAILABLE_FOR_SMS"
    GROUP_MEMBER_LIST_CHANGE = "GROUP_MEMBER_LIST_CHANGE"
    QOS_MON = "QOS_MON"

class UdmEvent(BaseModel):
    udmEvent: Union[UdmEventEnum, str] = Field(...)

class AfEventEnum(str, Enum):
    SVC_EXPERIENCE = "SVC_EXPERIENCE"
    UE_MOBILITY = "UE_MOBILITY"
    UE_COMM = "UE_COMM"
    EXCEPTIONS = "EXCEPTIONS"
    USER_DATA_CONGESTION = "USER_DATA_CONGESTION"
    PERF_DATA = "PERF_DATA"
    DISPERSION = "DISPERSION"
    COLLECTIVE_BEHAVIOUR = "COLLECTIVE_BEHAVIOUR"
    MS_QOE_METRICS = "MS_QOE_METRICS"
    MS_CONSUMPTION = "MS_CONSUMPTION"
    MS_NET_ASSIST_INVOCATION = "MS_NET_ASSIST_INVOCATION"
    MS_DYN_POLICY_INVOCATION = "MS_DYN_POLICY_INVOCATION"
    MS_ACCESS_ACTIVITY = "MS_ACCESS_ACTIVITY"
    GNSS_ASSISTANCE_DATA = "GNSS_ASSISTANCE_DATA"
    DATA_VOLUME_TRANSFER_TIME = "DATA_VOLUME_TRANSFER_TIME"

class AfEvent(BaseModel):
    afEvent: Union[AfEventEnum, str] = Field(...)

class UpfEventEnum(str, Enum):
    QOS_MONITORING = "QOS_MONITORING"
    USER_DATA_USAGE_MEASURES = "USER_DATA_USAGE_MEASURES"
    USER_DATA_USAGE_TRENDS = "USER_DATA_USAGE_TRENDS"
    TSC_MNGT_INFO = "TSC_MNGT_INFO"

class UpfEvent(BaseModel):
    upfEvent: Union[UpfEventEnum, str] = Field(
        ..., description="Enum for known UPF event types or a custom string for future extensions."
    )


class EventNotifyDataTypeEnum(str, Enum):
    UE_AVAILABLE = "UE_AVAILABLE"
    PERIODIC = "PERIODIC"
    ENTERING_INTO_AREA = "ENTERING_INTO_AREA"
    LEAVING_FROM_AREA = "LEAVING_FROM_AREA"
    BEING_INSIDE_AREA = "BEING_INSIDE_AREA"
    MOTION = "MOTION"
    MAXIMUM_INTERVAL_EXPIRATION_EVENT = "MAXIMUM_INTERVAL_EXPIRATION_EVENT"
    LOCATION_CANCELLATION_EVENT = "LOCATION_CANCELLATION_EVENT"
    ACTIVATION_OF_DEFERRED_LOCATION = "ACTIVATION_OF_DEFERRED_LOCATION"
    UE_MOBILITY_FOR_DEFERRED_LOCATION = "UE_MOBILITY_FOR_DEFERRED_LOCATION"
    _5GC_MT_LR = "5GC_MT_LR"
    DIRECT_REPORT_EVENT = "DIRECT_REPORT_EVENT"
    CUMULATIVE_EVENT_REPORT = "CUMULATIVE_EVENT_REPORT"

class EventNotifyDataType(BaseModel):
    eventNotifyDataType: Union[EventNotifyDataTypeEnum, str] = Field(
        ..., description="Enum for known event notification types or a custom string for future extensions."
    )
class NotificationEventTypeEnum(str, Enum):
    NF_REGISTERED = "NF_REGISTERED"
    NF_DEREGISTERED = "NF_DEREGISTERED"
    NF_PROFILE_CHANGED = "NF_PROFILE_CHANGED"
    SHARED_DATA_CHANGED = "SHARED_DATA_CHANGED"

class NotificationEventType(BaseModel):
    notificationEventType: Union[NotificationEventTypeEnum, str] = Field(
        ..., description="Enum for known notification event types or a custom string for future extensions."
    )



class SACEventTypeEnum(str, Enum):
    NUM_OF_REGD_UES = "NUM_OF_REGD_UES"
    NUM_OF_ESTD_PDU_SESSIONS = "NUM_OF_ESTD_PDU_SESSIONS"


class SACEventType(BaseModel):
    sacEventType: Union[SACEventTypeEnum, str]


class SACEventTriggerEnum(str, Enum):
    THRESHOLD = "THRESHOLD"
    PERIODIC = "PERIODIC"


class SACEventTrigger(BaseModel):
    sacEventTrigger: Union[SACEventTriggerEnum, str]


class SACInfo(BaseModel):
    numericValNumUes: Optional[int] = None
    numericValNumPduSess: Optional[int] = None
    percValueNumUes: Optional[int] = Field(None, ge=0, le=100)
    percValueNumPduSess: Optional[int] = Field(None, ge=0, le=100)
    uesWithPduSessionInd: Optional[bool] = False

class VarRepPeriod(BaseModel):
    repPeriod: int = Field(..., description="Duration in seconds.")
    percValueNfLoad: Optional[int] = Field(None, ge=0, le=100)

class SACEvent(BaseModel):
    eventType: SACEventType
    eventTrigger: Optional[SACEventTrigger] = None
    eventFilter: List[Snssai] = Field(..., min_items=1)
    notificationPeriod: Optional[int] = None
    notifThreshold: Optional[SACInfo] = None
    immediateFlag: Optional[bool] = False
    varRepPeriodInfo: Optional[List[VarRepPeriod]] = Field(None, min_items=1)


class DccfEvent(BaseModel):
    nwdafEvent: Optional[NwdafEvent] = None
    smfEvent: Optional[SmfEvent] = None
    amfEvent: Optional[AmfEventType] = None
    nefEvent: Optional[NefEvent] = None
    udmEvent: Optional[UdmEvent] = None
    afEvent: Optional[AfEvent] = None
    sacEvent: Optional[SACEvent] = None
    nrfEvent: Optional[NotificationEventType] = None
    gmlcEvent: Optional[EventNotifyDataType] = None
    upfEvent: Optional[UpfEvent] = None

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        # Count how many fields are provided
        provided_fields = [key for key, value in values.items() if value is not None]

        if len(provided_fields) != 1:
            raise ValueError(f"Exactly one of {', '.join(cls.__annotations__.keys())} must be provided, but got {len(provided_fields)}.")

        return values
class InputDataInfo(BaseModel):
    ratio: Optional[int] = Field(None, ge=0)
    maxNumSamples: Optional[int] = Field(None, ge=0)
    maxTimeInterval: Optional[int] = Field(None, ge=0)
    inpEvent: DccfEvent
    nfInstanceIds: Optional[List[NfInstanceId]] = Field(None, min_items=1)
    nfSetIds: Optional[List[str]] = Field(None, min_items=1)

class AccuracyEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    HIGHEST = "HIGHEST"

class Accuracy(BaseModel):
    accuracy: Union[AccuracyEnum, str]
class ModelProvisionParamsExt(BaseModel):
    reqRepRatio: Optional[int] = Field(None, ge=0)
    inferInpDataInfos: Optional[List[InputDataInfo]] = Field(None, min_items=1)
    multModelsInd: Optional[bool] = None
    numModels: Optional[int] = Field(None, ge=0)
    accuLevels: Optional[List[Accuracy]] = Field(None, min_items=1)

class InferenceDataForModelTrain(BaseModel):
    adrfId: Optional[NfInstanceId] = None
    adrfSetId: Optional[str] = None
    dataSetTag: Optional[DataSetTag] = None
    modelId: Optional[int] = Field(None, ge=0)

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        # Check that at least one of 'adrfId' or 'adrfSetId' is provided
        if not any([values.get("adrfId"), values.get("adrfSetId")]):
            raise ValueError("Exactly one of 'adrfId' or 'adrfSetId' must be provided.")

        return values

class MLEventSubscription(BaseModel):
    mLEvent: NwdafEvent
    mLEventFilter: EventFilter
    tgtUe: Optional[TargetUeInformation] = None
    mLTargetPeriod: Optional[TimeWindow] = None
    expiryTime: Optional[datetime] = None
    timeModelNeeded: Optional[datetime] = None
    mlEvRepCon: Optional[MLRepEventCondition] = None
    modelInterInfo: Optional[str] = None
    nfConsumerInfo: Optional[str] = Field(None, pattern=r"^[0-9]{6}$")
    modelProvExt: Optional[ModelProvisionParamsExt] = None
    useCaseCxt: Optional[str] = None
    inferDataForModel: Optional[InferenceDataForModelTrain] = None
    modelId: Optional[int] = Field(None, ge=0)

class MLModelAddr(BaseModel):
    mLModelUrl: Optional[HttpUrl] = None
    mlFileFqdn: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        # Ensure exactly one of 'mLModelUrl' or 'mlFileFqdn' is provided
        if not any([values.get("mLModelUrl"), values.get("mlFileFqdn")]):
            raise ValueError("Exactly one of 'mLModelUrl' or 'mlFileFqdn' must be provided.")

        return values

class MLModelAdrf(BaseModel):
    adrfId: Optional[NfInstanceId] = None
    adrfSetId: Optional[str] = None
    storTransId: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        # Ensure exactly one of 'adrfId' or 'adrfSetId' is provided
        if not any([values.get("adrfId"), values.get("adrfSetId")]):
            raise ValueError("Exactly one of 'adrfId' or 'adrfSetId' must be provided.")

        return values

class TrainInputDataInfo(BaseModel):
    dataInfo: InputDataInfo
    time: Optional[TimeWindow] = None
    dataStatisticsInfos: Optional[str] = None

class AdditionalMLModelInformation(BaseModel):
    mLFileAddr: Optional[MLModelAddr] = None
    mLModelAdrf: Optional[MLModelAdrf] = None
    validityPeriod: Optional[TimeWindow] = None
    spatialValidity: Optional[NetworkAreaInfo] = None
    modelUniqueId: int = Field(..., ge=0)
    modelRepRatio: Optional[int] = Field(None, ge=0)
    mlDegradInd: Optional[bool] = False
    trainInpInfos: Optional[List[TrainInputDataInfo]] = Field(None, min_items=1)
    modelMetric: Optional[MLModelMetric] = None
    accMLModel: Optional[int] = Field(None, ge=0)

    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        # Ensure exactly one of 'mLFileAddr' or 'mLModelAdrf' is provided
        if not any([values.get("mLFileAddr"), values.get("mLModelAdrf")]):
            raise ValueError("Exactly one of 'mLFileAddr' or 'mLModelAdrf' must be provided.")

        return values


class MLEventNotif(BaseModel):
    event: NwdafEvent
    notifCorreId: Optional[str] = None
    mlFile: Optional[str] = None
    mLFileAddr: Optional[MLModelAddr] = None
    mLModelAdrf: Optional[MLModelAdrf] = None
    validityPeriod: Optional[TimeWindow] = None
    spatialValidity: Optional[NetworkAreaInfo] = None
    addModelInfo: Optional[List[AdditionalMLModelInformation]] = Field(None, min_items=1)
    modelUniqueId: int = Field(..., ge=0)
    @model_validator(mode="before")
    @classmethod
    def validate_one_of(cls, values):
        # Ensure exactly one of 'mLFileAddr' or 'mLModelAdrf' is provided
        if not any([values.get("mLFileAddr"), values.get("mLModelAdrf")]):
            raise ValueError("Exactly one of 'mLFileAddr' or 'mLModelAdrf' must be provided.")

        return values
class NotificationMethodEnum(str, Enum):
    PERIODIC = "PERIODIC"
    ONE_TIME = "ONE_TIME"
    ON_EVENT_DETECTION = "ON_EVENT_DETECTION"


class NotificationMethod(BaseModel):
    notificationMethod: Union[NotificationMethodEnum, str]

class PartitioningCriteriaEnum(str, Enum):
    TAC = "TAC"
    SUBPLMN = "SUBPLMN"
    GEOAREA = "GEOAREA"
    SNSSAI = "SNSSAI"
    DNN = "DNN"


class PartitioningCriteria(BaseModel):
    partitioningCriteria: Union[PartitioningCriteriaEnum, str]

class NotificationFlagEnum(str, Enum):
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"
    RETRIEVAL = "RETRIEVAL"


class NotificationFlag(BaseModel):
    notificationFlag: Union[NotificationFlagEnum, str]

class BufferedNotificationsActionEnum(str, Enum):
    SEND_ALL = "SEND_ALL"
    DISCARD_ALL = "DISCARD_ALL"
    DROP_OLD = "DROP_OLD"

class BufferedNotificationsAction(BaseModel):
    notificationFlag: Union[BufferedNotificationsActionEnum, str]

class SubscriptionActionEnum(str, Enum):
    CLOSE = "CLOSE"
    CONTINUE_WITH_MUTING = "CONTINUE_WITH_MUTING"
    CONTINUE_WITHOUT_MUTING = "CONTINUE_WITHOUT_MUTING"


class SubscriptionAction(BaseModel):
    notificationFlag: Union[SubscriptionActionEnum, str]


class MutingExceptionInstructions(BaseModel):
    bufferedNotifs: Optional[BufferedNotificationsAction] = None
    subscription: Optional[SubscriptionActionEnum] = None

class MutingNotificationsSettings(BaseModel):
    maxNoOfNotif: Optional[int] = None
    durationBufferedNotif: Optional[int] = Field(None, ge=0)


class ReportingInformation(BaseModel):
    immRep: Optional[bool] = None
    notifMethod: Optional[NotificationMethod] = None
    maxReportNbr: Optional[int] = Field(None, ge=0)
    monDur: Optional[datetime] = None
    repPeriod: Optional[int] = Field(None, ge=0)
    sampRatio: Optional[int] = Field(None, ge=1, le=100)
    partitionCriteria: Optional[List[PartitioningCriteria]] = Field(None, min_items=1)
    grpRepTime: Optional[int] = Field(None, ge=0)
    notifFlag: Optional[NotificationFlag] = None
    notifFlagInstruct: Optional[MutingExceptionInstructions] = None
    mutingSetting: Optional[MutingNotificationsSettings] = None

class FailureEventInfoForMLModel(BaseModel):
    event: NwdafEvent
    failureCode: FailureCode


class NwdafMLModelProvSubsc(BaseModel):
    mLEventSubscs: List[MLEventSubscription] = Field(..., min_items=1)
    notifUri: HttpUrl
    mLEventNotifs: Optional[List[MLEventNotif]] = Field(None, min_items=1)
    suppFeats: Optional[str] = Field(None, pattern=r"^[A-Fa-f0-9]*$")
    notifCorreId: Optional[str] = None
    eventReq: Optional[ReportingInformation] = None
    failEventReports: Optional[List[FailureEventInfoForMLModel]] = Field(None, min_items=1)

class NwdafMLModelProvNotif(BaseModel):
    eventNotifs: List[MLEventNotif] = Field(..., min_items=1)
    subscriptionId: str