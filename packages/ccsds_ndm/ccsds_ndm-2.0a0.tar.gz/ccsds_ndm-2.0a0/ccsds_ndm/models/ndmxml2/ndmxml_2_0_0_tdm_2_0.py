from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from ccsds_ndm.models.ndmxml2.ndmxml_2_0_0_common_2_0 import (
    AngleType,
    TimeSystemType,
    YesNoType,
)

__NAMESPACE__ = "urn:ccsds:schema:ndmxml"


class AngleTypeType(Enum):
    AZEL = "AZEL"
    AZEL_1 = "azel"
    RADEC = "RADEC"
    RADEC_1 = "radec"
    XEYN = "XEYN"
    XEYN_1 = "xeyn"
    XSYE = "XSYE"
    XSYE_1 = "xsye"


class DataQualityType(Enum):
    RAW = "raw"
    RAW_1 = "RAW"
    VALIDATED = "validated"
    VALIDATED_1 = "VALIDATED"
    DEGRADED = "degraded"
    DEGRADED_1 = "DEGRADED"


class IntegrationRefType(Enum):
    START = "START"
    START_1 = "start"
    MIDDLE = "MIDDLE"
    MIDDLE_1 = "middle"
    END = "END"
    END_1 = "end"


class ModeType(Enum):
    SEQUENTIAL = "SEQUENTIAL"
    SEQUENTIAL_1 = "sequential"
    SINGLE_DIFF = "SINGLE_DIFF"
    SINGLE_DIFF_1 = "single_diff"


class RangeUnitsType(Enum):
    KM = "km"
    KM_1 = "KM"
    RU = "ru"
    RU_1 = "RU"
    S = "s"
    S_1 = "S"


class RangemodeType(Enum):
    COHERENT = "coherent"
    COHERENT_1 = "COHERENT"
    CONSTANT = "constant"
    CONSTANT_1 = "CONSTANT"
    ONE_WAY = "one_way"
    ONE_WAY_1 = "ONE_WAY"


class RefFrameType(Enum):
    EME2000 = "EME2000"
    EME2000_1 = "eme2000"
    ICRF = "ICRF"
    ICRF_1 = "icrf"
    ITRF2000 = "ITRF2000"
    ITRF2000_1 = "itrf2000"
    ITRF_93 = "ITRF-93"
    ITRF_93_1 = "itrf-93"
    ITRF_97 = "ITRF-97"
    ITRF_97_1 = "itrf-97"
    TOD = "TOD"
    TOD_1 = "tod"


@dataclass
class TdmHeader:
    class Meta:
        name = "tdmHeader"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    creation_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "CREATION_DATE",
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    originator: Optional[str] = field(
        default=None,
        metadata={
            "name": "ORIGINATOR",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    message_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MESSAGE_ID",
            "type": "Element",
            "namespace": "",
        },
    )


class TimetagRefType(Enum):
    TRANSMIT = "TRANSMIT"
    TRANSMIT_1 = "transmit"
    RECEIVE = "RECEIVE"
    RECEIVE_1 = "receive"


@dataclass
class TdmMetadata:
    class Meta:
        name = "tdmMetadata"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    track_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TRACK_ID",
            "type": "Element",
            "namespace": "",
        },
    )
    data_types: Optional[str] = field(
        default=None,
        metadata={
            "name": "DATA_TYPES",
            "type": "Element",
            "namespace": "",
        },
    )
    time_system: Optional[TimeSystemType] = field(
        default=None,
        metadata={
            "name": "TIME_SYSTEM",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    start_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "START_TIME",
            "type": "Element",
            "namespace": "",
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    stop_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "STOP_TIME",
            "type": "Element",
            "namespace": "",
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    participant_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "PARTICIPANT_1",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    participant_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "PARTICIPANT_2",
            "type": "Element",
            "namespace": "",
        },
    )
    participant_3: Optional[str] = field(
        default=None,
        metadata={
            "name": "PARTICIPANT_3",
            "type": "Element",
            "namespace": "",
        },
    )
    participant_4: Optional[str] = field(
        default=None,
        metadata={
            "name": "PARTICIPANT_4",
            "type": "Element",
            "namespace": "",
        },
    )
    participant_5: Optional[str] = field(
        default=None,
        metadata={
            "name": "PARTICIPANT_5",
            "type": "Element",
            "namespace": "",
        },
    )
    mode: Optional[ModeType] = field(
        default=None,
        metadata={
            "name": "MODE",
            "type": "Element",
            "namespace": "",
        },
    )
    path: Optional[str] = field(
        default=None,
        metadata={
            "name": "PATH",
            "type": "Element",
            "namespace": "",
            "pattern": r"\d{1},\d{1}(,\d{1})*",
        },
    )
    path_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "PATH_1",
            "type": "Element",
            "namespace": "",
            "pattern": r"\d{1},\d{1}(,\d{1})*",
        },
    )
    path_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "PATH_2",
            "type": "Element",
            "namespace": "",
            "pattern": r"\d{1},\d{1}(,\d{1})*",
        },
    )
    ephemeris_name_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPHEMERIS_NAME_1",
            "type": "Element",
            "namespace": "",
        },
    )
    ephemeris_name_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPHEMERIS_NAME_2",
            "type": "Element",
            "namespace": "",
        },
    )
    ephemeris_name_3: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPHEMERIS_NAME_3",
            "type": "Element",
            "namespace": "",
        },
    )
    ephemeris_name_4: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPHEMERIS_NAME_4",
            "type": "Element",
            "namespace": "",
        },
    )
    ephemeris_name_5: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPHEMERIS_NAME_5",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_band: Optional[str] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_BAND",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_band: Optional[str] = field(
        default=None,
        metadata={
            "name": "RECEIVE_BAND",
            "type": "Element",
            "namespace": "",
        },
    )
    turnaround_numerator: Optional[int] = field(
        default=None,
        metadata={
            "name": "TURNAROUND_NUMERATOR",
            "type": "Element",
            "namespace": "",
        },
    )
    turnaround_denominator: Optional[int] = field(
        default=None,
        metadata={
            "name": "TURNAROUND_DENOMINATOR",
            "type": "Element",
            "namespace": "",
        },
    )
    timetag_ref: Optional[TimetagRefType] = field(
        default=None,
        metadata={
            "name": "TIMETAG_REF",
            "type": "Element",
            "namespace": "",
        },
    )
    integration_interval: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "INTEGRATION_INTERVAL",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    integration_ref: Optional[IntegrationRefType] = field(
        default=None,
        metadata={
            "name": "INTEGRATION_REF",
            "type": "Element",
            "namespace": "",
        },
    )
    freq_offset: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FREQ_OFFSET",
            "type": "Element",
            "namespace": "",
        },
    )
    range_mode: Optional[RangemodeType] = field(
        default=None,
        metadata={
            "name": "RANGE_MODE",
            "type": "Element",
            "namespace": "",
        },
    )
    range_modulus: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RANGE_MODULUS",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    range_units: Optional[RangeUnitsType] = field(
        default=None,
        metadata={
            "name": "RANGE_UNITS",
            "type": "Element",
            "namespace": "",
        },
    )
    angle_type: Optional[AngleTypeType] = field(
        default=None,
        metadata={
            "name": "ANGLE_TYPE",
            "type": "Element",
            "namespace": "",
        },
    )
    reference_frame: Optional[RefFrameType] = field(
        default=None,
        metadata={
            "name": "REFERENCE_FRAME",
            "type": "Element",
            "namespace": "",
        },
    )
    interpolation: Optional[str] = field(
        default=None,
        metadata={
            "name": "INTERPOLATION",
            "type": "Element",
            "namespace": "",
        },
    )
    interpolation_degree: Optional[int] = field(
        default=None,
        metadata={
            "name": "INTERPOLATION_DEGREE",
            "type": "Element",
            "namespace": "",
        },
    )
    doppler_count_bias: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DOPPLER_COUNT_BIAS",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    doppler_count_scale: Optional[int] = field(
        default=None,
        metadata={
            "name": "DOPPLER_COUNT_SCALE",
            "type": "Element",
            "namespace": "",
        },
    )
    doppler_count_rollover: Optional[YesNoType] = field(
        default=None,
        metadata={
            "name": "DOPPLER_COUNT_ROLLOVER",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_delay_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_DELAY_1",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    transmit_delay_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_DELAY_2",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    transmit_delay_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_DELAY_3",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    transmit_delay_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_DELAY_4",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    transmit_delay_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_DELAY_5",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    receive_delay_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_DELAY_1",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    receive_delay_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_DELAY_2",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    receive_delay_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_DELAY_3",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    receive_delay_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_DELAY_4",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    receive_delay_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_DELAY_5",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    data_quality: Optional[DataQualityType] = field(
        default=None,
        metadata={
            "name": "DATA_QUALITY",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_angle_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_ANGLE_1",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_angle_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_ANGLE_2",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_doppler: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_DOPPLER",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_mag: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_MAG",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_range: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_RANGE",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_rcs: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_RCS",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_receive: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_RECEIVE",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_transmit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_TRANSMIT",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_aberration_yearly: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_ABERRATION_YEARLY",
            "type": "Element",
            "namespace": "",
        },
    )
    correction_aberration_diurnal: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CORRECTION_ABERRATION_DIURNAL",
            "type": "Element",
            "namespace": "",
        },
    )
    corrections_applied: Optional[YesNoType] = field(
        default=None,
        metadata={
            "name": "CORRECTIONS_APPLIED",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class TrackingDataObservationType:
    class Meta:
        name = "trackingDataObservationType"

    epoch: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPOCH",
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    angle_1: Optional[AngleType] = field(
        default=None,
        metadata={
            "name": "ANGLE_1",
            "type": "Element",
            "namespace": "",
        },
    )
    angle_2: Optional[AngleType] = field(
        default=None,
        metadata={
            "name": "ANGLE_2",
            "type": "Element",
            "namespace": "",
        },
    )
    carrier_power: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CARRIER_POWER",
            "type": "Element",
            "namespace": "",
        },
    )
    clock_bias: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CLOCK_BIAS",
            "type": "Element",
            "namespace": "",
        },
    )
    clock_drift: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "CLOCK_DRIFT",
            "type": "Element",
            "namespace": "",
        },
    )
    doppler_count: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DOPPLER_COUNT",
            "type": "Element",
            "namespace": "",
        },
    )
    doppler_instantaneous: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DOPPLER_INSTANTANEOUS",
            "type": "Element",
            "namespace": "",
        },
    )
    doppler_integrated: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DOPPLER_INTEGRATED",
            "type": "Element",
            "namespace": "",
        },
    )
    dor: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DOR",
            "type": "Element",
            "namespace": "",
        },
    )
    mag: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "MAG",
            "type": "Element",
            "namespace": "",
        },
    )
    pc_n0: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PC_N0",
            "type": "Element",
            "namespace": "",
        },
    )
    pr_n0: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PR_N0",
            "type": "Element",
            "namespace": "",
        },
    )
    pressure: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "PRESSURE",
            "type": "Element",
            "namespace": "",
        },
    )
    range: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RANGE",
            "type": "Element",
            "namespace": "",
        },
    )
    rcs: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RCS",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_freq: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_FREQ",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_freq_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_FREQ_1",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_freq_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_FREQ_2",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_freq_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_FREQ_3",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_freq_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_FREQ_4",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_freq_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_FREQ_5",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_phase_ct_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_PHASE_CT_1",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_phase_ct_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_PHASE_CT_2",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_phase_ct_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_PHASE_CT_3",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_phase_ct_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_PHASE_CT_4",
            "type": "Element",
            "namespace": "",
        },
    )
    receive_phase_ct_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RECEIVE_PHASE_CT_5",
            "type": "Element",
            "namespace": "",
        },
    )
    rhumidity: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "RHUMIDITY",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
            "max_inclusive": Decimal("100.0"),
        },
    )
    stec: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "STEC",
            "type": "Element",
            "namespace": "",
        },
    )
    temperature: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TEMPERATURE",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    transmit_freq_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_1",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    transmit_freq_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_2",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    transmit_freq_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_3",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    transmit_freq_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_4",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    transmit_freq_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_5",
            "type": "Element",
            "namespace": "",
            "min_exclusive": Decimal("0.0"),
        },
    )
    transmit_freq_rate_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_RATE_1",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_freq_rate_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_RATE_2",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_freq_rate_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_RATE_3",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_freq_rate_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_RATE_4",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_freq_rate_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_FREQ_RATE_5",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_phase_ct_1: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_PHASE_CT_1",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_phase_ct_2: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_PHASE_CT_2",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_phase_ct_3: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_PHASE_CT_3",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_phase_ct_4: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_PHASE_CT_4",
            "type": "Element",
            "namespace": "",
        },
    )
    transmit_phase_ct_5: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TRANSMIT_PHASE_CT_5",
            "type": "Element",
            "namespace": "",
        },
    )
    tropo_dry: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TROPO_DRY",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    tropo_wet: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TROPO_WET",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
        },
    )
    vlbi_delay: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "VLBI_DELAY",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class TdmData:
    class Meta:
        name = "tdmData"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    observation: List[TrackingDataObservationType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass
class TdmSegment:
    class Meta:
        name = "tdmSegment"

    metadata: Optional[TdmMetadata] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    data: Optional[TdmData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class TdmBody:
    class Meta:
        name = "tdmBody"

    segment: List[TdmSegment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass
class TdmType:
    class Meta:
        name = "tdmType"

    header: Optional[TdmHeader] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    body: Optional[TdmBody] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    id: str = field(
        init=False,
        default="CCSDS_TDM_VERS",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    version: str = field(
        init=False,
        default="2.0",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
