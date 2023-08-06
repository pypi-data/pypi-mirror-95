from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from ccsds_ndm.models.ndmxml2.ndmxml_2_0_0_common_2_0 import (
    AreaType,
    LengthType,
    MassType,
    Ms2Type,
    ObjectDescriptionType,
    OdParametersType,
    PositionUnits,
    VelocityUnits,
    YesNoType,
)

__NAMESPACE__ = "urn:ccsds:schema:ndmxml"


@dataclass
class CdmHeader:
    class Meta:
        name = "cdmHeader"

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
    message_for: Optional[str] = field(
        default=None,
        metadata={
            "name": "MESSAGE_FOR",
            "type": "Element",
            "namespace": "",
        },
    )
    message_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MESSAGE_ID",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


class CovarianceMethodType(Enum):
    CALCULATED = "CALCULATED"
    CALCULATED_1 = "calculated"
    DEFAULT = "DEFAULT"
    DEFAULT_1 = "default"


class DvUnits(Enum):
    M_S = "m/s"


class M2Units(Enum):
    M_2 = "m**2"


class M2KgUnits(Enum):
    M_2_KG = "m**2/kg"


class M2S2Units(Enum):
    M_2_S_2 = "m**2/s**2"


class M2S3Units(Enum):
    M_2_S_3 = "m**2/s**3"


class M2S4Units(Enum):
    M_2_S_4 = "m**2/s**4"


class M2SUnits(Enum):
    M_2_S = "m**2/s"


class M3KgUnits(Enum):
    M_3_KG = "m**3/kg"


class M3Kgs2Units(Enum):
    M_3_KG_S_2 = "m**3/(kg*s**2)"


class M3KgsUnits(Enum):
    M_3_KG_S = "m**3/(kg*s)"


class M4Kg2Units(Enum):
    M_4_KG_2 = "m**4/kg**2"


class ManeuverableType(Enum):
    YES = "YES"
    YES_1 = "yes"
    NO = "NO"
    NO_1 = "no"
    N_A = "N/A"
    N_A_1 = "n/a"


class ObjectType(Enum):
    OBJECT1 = "OBJECT1"
    OBJECT1_1 = "object1"
    OBJECT2 = "OBJECT2"
    OBJECT2_1 = "object2"


class ReferenceFrameType(Enum):
    EME2000 = "EME2000"
    EME2000_1 = "eme2000"
    GCRF = "GCRF"
    GCRF_1 = "gcrf"
    ITRF = "ITRF"
    ITRF_1 = "itrf"


class ScreenVolumeFrameType(Enum):
    RTN = "RTN"
    RTN_1 = "rtn"
    TVN = "TVN"
    TVN_1 = "tvn"


class ScreenVolumeShapeType(Enum):
    ELLIPSOID = "ELLIPSOID"
    ELLIPSOID_1 = "ellipsoid"
    BOX = "BOX"
    BOX_1 = "box"


class WkgUnits(Enum):
    W_KG = "W/kg"


@dataclass
class CdmMetadata:
    class Meta:
        name = "cdmMetadata"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    object: Optional[ObjectType] = field(
        default=None,
        metadata={
            "name": "OBJECT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    object_designator: Optional[str] = field(
        default=None,
        metadata={
            "name": "OBJECT_DESIGNATOR",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    catalog_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CATALOG_NAME",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    object_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "OBJECT_NAME",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    international_designator: Optional[str] = field(
        default=None,
        metadata={
            "name": "INTERNATIONAL_DESIGNATOR",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    object_type: Optional[ObjectDescriptionType] = field(
        default=None,
        metadata={
            "name": "OBJECT_TYPE",
            "type": "Element",
            "namespace": "",
        },
    )
    operator_contact_position: Optional[str] = field(
        default=None,
        metadata={
            "name": "OPERATOR_CONTACT_POSITION",
            "type": "Element",
            "namespace": "",
        },
    )
    operator_organization: Optional[str] = field(
        default=None,
        metadata={
            "name": "OPERATOR_ORGANIZATION",
            "type": "Element",
            "namespace": "",
        },
    )
    operator_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "OPERATOR_PHONE",
            "type": "Element",
            "namespace": "",
        },
    )
    operator_email: Optional[str] = field(
        default=None,
        metadata={
            "name": "OPERATOR_EMAIL",
            "type": "Element",
            "namespace": "",
        },
    )
    ephemeris_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "EPHEMERIS_NAME",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    covariance_method: Optional[CovarianceMethodType] = field(
        default=None,
        metadata={
            "name": "COVARIANCE_METHOD",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    maneuverable: Optional[ManeuverableType] = field(
        default=None,
        metadata={
            "name": "MANEUVERABLE",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    orbit_center: Optional[str] = field(
        default=None,
        metadata={
            "name": "ORBIT_CENTER",
            "type": "Element",
            "namespace": "",
        },
    )
    ref_frame: Optional[ReferenceFrameType] = field(
        default=None,
        metadata={
            "name": "REF_FRAME",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    gravity_model: Optional[str] = field(
        default=None,
        metadata={
            "name": "GRAVITY_MODEL",
            "type": "Element",
            "namespace": "",
        },
    )
    atmospheric_model: Optional[str] = field(
        default=None,
        metadata={
            "name": "ATMOSPHERIC_MODEL",
            "type": "Element",
            "namespace": "",
        },
    )
    n_body_perturbations: Optional[str] = field(
        default=None,
        metadata={
            "name": "N_BODY_PERTURBATIONS",
            "type": "Element",
            "namespace": "",
        },
    )
    solar_rad_pressure: Optional[YesNoType] = field(
        default=None,
        metadata={
            "name": "SOLAR_RAD_PRESSURE",
            "type": "Element",
            "namespace": "",
        },
    )
    earth_tides: Optional[YesNoType] = field(
        default=None,
        metadata={
            "name": "EARTH_TIDES",
            "type": "Element",
            "namespace": "",
        },
    )
    intrack_thrust: Optional[YesNoType] = field(
        default=None,
        metadata={
            "name": "INTRACK_THRUST",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class CdmPositionType:
    class Meta:
        name = "cdmPositionType"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[PositionUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CdmVelocityType:
    class Meta:
        name = "cdmVelocityType"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[VelocityUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DvType:
    class Meta:
        name = "dvType"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[DvUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M2Type:
    class Meta:
        name = "m2Type"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M2Units] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M2KgType:
    class Meta:
        name = "m2kgType"

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "min_inclusive": Decimal("0.0"),
        },
    )
    units: Optional[M2KgUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M2S2Type:
    class Meta:
        name = "m2s2Type"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M2S2Units] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M2S3Type:
    class Meta:
        name = "m2s3Type"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M2S3Units] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M2S4Type:
    class Meta:
        name = "m2s4Type"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M2S4Units] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M2SType:
    class Meta:
        name = "m2sType"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M2SUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M3KgType:
    class Meta:
        name = "m3kgType"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M3KgUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M3Kgs2Type:
    class Meta:
        name = "m3kgs2Type"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M3Kgs2Units] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M3KgsType:
    class Meta:
        name = "m3kgsType"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M3KgsUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class M4Kg2Type:
    class Meta:
        name = "m4kg2Type"

    value: Optional[Decimal] = field(
        default=None,
    )
    units: Optional[M4Kg2Units] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class WkgType:
    class Meta:
        name = "wkgType"

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "min_inclusive": Decimal("0.0"),
        },
    )
    units: Optional[WkgUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AdditionalParametersType:
    class Meta:
        name = "additionalParametersType"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    area_pc: Optional[AreaType] = field(
        default=None,
        metadata={
            "name": "AREA_PC",
            "type": "Element",
            "namespace": "",
        },
    )
    area_drg: Optional[AreaType] = field(
        default=None,
        metadata={
            "name": "AREA_DRG",
            "type": "Element",
            "namespace": "",
        },
    )
    area_srp: Optional[AreaType] = field(
        default=None,
        metadata={
            "name": "AREA_SRP",
            "type": "Element",
            "namespace": "",
        },
    )
    mass: Optional[MassType] = field(
        default=None,
        metadata={
            "name": "MASS",
            "type": "Element",
            "namespace": "",
        },
    )
    cd_area_over_mass: Optional[M2KgType] = field(
        default=None,
        metadata={
            "name": "CD_AREA_OVER_MASS",
            "type": "Element",
            "namespace": "",
        },
    )
    cr_area_over_mass: Optional[M2KgType] = field(
        default=None,
        metadata={
            "name": "CR_AREA_OVER_MASS",
            "type": "Element",
            "namespace": "",
        },
    )
    thrust_acceleration: Optional[Ms2Type] = field(
        default=None,
        metadata={
            "name": "THRUST_ACCELERATION",
            "type": "Element",
            "namespace": "",
        },
    )
    sedr: Optional[WkgType] = field(
        default=None,
        metadata={
            "name": "SEDR",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class CdmCovarianceMatrixType:
    class Meta:
        name = "cdmCovarianceMatrixType"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    cr_r: Optional[M2Type] = field(
        default=None,
        metadata={
            "name": "CR_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ct_r: Optional[M2Type] = field(
        default=None,
        metadata={
            "name": "CT_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ct_t: Optional[M2Type] = field(
        default=None,
        metadata={
            "name": "CT_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cn_r: Optional[M2Type] = field(
        default=None,
        metadata={
            "name": "CN_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cn_t: Optional[M2Type] = field(
        default=None,
        metadata={
            "name": "CN_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cn_n: Optional[M2Type] = field(
        default=None,
        metadata={
            "name": "CN_N",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    crdot_r: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CRDOT_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    crdot_t: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CRDOT_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    crdot_n: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CRDOT_N",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    crdot_rdot: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CRDOT_RDOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ctdot_r: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CTDOT_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ctdot_t: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CTDOT_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ctdot_n: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CTDOT_N",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ctdot_rdot: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CTDOT_RDOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    ctdot_tdot: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CTDOT_TDOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cndot_r: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CNDOT_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cndot_t: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CNDOT_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cndot_n: Optional[M2SType] = field(
        default=None,
        metadata={
            "name": "CNDOT_N",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cndot_rdot: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CNDOT_RDOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cndot_tdot: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CNDOT_TDOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cndot_ndot: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CNDOT_NDOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    cdrg_r: Optional[M3KgType] = field(
        default=None,
        metadata={
            "name": "CDRG_R",
            "type": "Element",
            "namespace": "",
        },
    )
    cdrg_t: Optional[M3KgType] = field(
        default=None,
        metadata={
            "name": "CDRG_T",
            "type": "Element",
            "namespace": "",
        },
    )
    cdrg_n: Optional[M3KgType] = field(
        default=None,
        metadata={
            "name": "CDRG_N",
            "type": "Element",
            "namespace": "",
        },
    )
    cdrg_rdot: Optional[M3KgsType] = field(
        default=None,
        metadata={
            "name": "CDRG_RDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    cdrg_tdot: Optional[M3KgsType] = field(
        default=None,
        metadata={
            "name": "CDRG_TDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    cdrg_ndot: Optional[M3KgsType] = field(
        default=None,
        metadata={
            "name": "CDRG_NDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    cdrg_drg: Optional[M4Kg2Type] = field(
        default=None,
        metadata={
            "name": "CDRG_DRG",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_r: Optional[M3KgType] = field(
        default=None,
        metadata={
            "name": "CSRP_R",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_t: Optional[M3KgType] = field(
        default=None,
        metadata={
            "name": "CSRP_T",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_n: Optional[M3KgType] = field(
        default=None,
        metadata={
            "name": "CSRP_N",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_rdot: Optional[M3KgsType] = field(
        default=None,
        metadata={
            "name": "CSRP_RDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_tdot: Optional[M3KgsType] = field(
        default=None,
        metadata={
            "name": "CSRP_TDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_ndot: Optional[M3KgsType] = field(
        default=None,
        metadata={
            "name": "CSRP_NDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_drg: Optional[M4Kg2Type] = field(
        default=None,
        metadata={
            "name": "CSRP_DRG",
            "type": "Element",
            "namespace": "",
        },
    )
    csrp_srp: Optional[M4Kg2Type] = field(
        default=None,
        metadata={
            "name": "CSRP_SRP",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_r: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CTHR_R",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_t: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CTHR_T",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_n: Optional[M2S2Type] = field(
        default=None,
        metadata={
            "name": "CTHR_N",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_rdot: Optional[M2S3Type] = field(
        default=None,
        metadata={
            "name": "CTHR_RDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_tdot: Optional[M2S3Type] = field(
        default=None,
        metadata={
            "name": "CTHR_TDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_ndot: Optional[M2S3Type] = field(
        default=None,
        metadata={
            "name": "CTHR_NDOT",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_drg: Optional[M3Kgs2Type] = field(
        default=None,
        metadata={
            "name": "CTHR_DRG",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_srp: Optional[M3Kgs2Type] = field(
        default=None,
        metadata={
            "name": "CTHR_SRP",
            "type": "Element",
            "namespace": "",
        },
    )
    cthr_thr: Optional[M2S4Type] = field(
        default=None,
        metadata={
            "name": "CTHR_THR",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class CdmStateVectorType:
    class Meta:
        name = "cdmStateVectorType"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    x: Optional[CdmPositionType] = field(
        default=None,
        metadata={
            "name": "X",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    y: Optional[CdmPositionType] = field(
        default=None,
        metadata={
            "name": "Y",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    z: Optional[CdmPositionType] = field(
        default=None,
        metadata={
            "name": "Z",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    x_dot: Optional[CdmVelocityType] = field(
        default=None,
        metadata={
            "name": "X_DOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    y_dot: Optional[CdmVelocityType] = field(
        default=None,
        metadata={
            "name": "Y_DOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    z_dot: Optional[CdmVelocityType] = field(
        default=None,
        metadata={
            "name": "Z_DOT",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class RelativeStateVectorType:
    class Meta:
        name = "relativeStateVectorType"

    relative_position_r: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_POSITION_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    relative_position_t: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_POSITION_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    relative_position_n: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_POSITION_N",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    relative_velocity_r: Optional[DvType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_VELOCITY_R",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    relative_velocity_t: Optional[DvType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_VELOCITY_T",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    relative_velocity_n: Optional[DvType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_VELOCITY_N",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class CdmData:
    class Meta:
        name = "cdmData"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    od_parameters: Optional[OdParametersType] = field(
        default=None,
        metadata={
            "name": "odParameters",
            "type": "Element",
            "namespace": "",
        },
    )
    additional_parameters: Optional[AdditionalParametersType] = field(
        default=None,
        metadata={
            "name": "additionalParameters",
            "type": "Element",
            "namespace": "",
        },
    )
    state_vector: Optional[CdmStateVectorType] = field(
        default=None,
        metadata={
            "name": "stateVector",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    covariance_matrix: Optional[CdmCovarianceMatrixType] = field(
        default=None,
        metadata={
            "name": "covarianceMatrix",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class RelativeMetadataData:
    class Meta:
        name = "relativeMetadataData"

    comment: List[str] = field(
        default_factory=list,
        metadata={
            "name": "COMMENT",
            "type": "Element",
            "namespace": "",
        },
    )
    tca: Optional[str] = field(
        default=None,
        metadata={
            "name": "TCA",
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    miss_distance: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "MISS_DISTANCE",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    relative_speed: Optional[DvType] = field(
        default=None,
        metadata={
            "name": "RELATIVE_SPEED",
            "type": "Element",
            "namespace": "",
        },
    )
    relative_state_vector: Optional[RelativeStateVectorType] = field(
        default=None,
        metadata={
            "name": "relativeStateVector",
            "type": "Element",
            "namespace": "",
        },
    )
    start_screen_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "START_SCREEN_PERIOD",
            "type": "Element",
            "namespace": "",
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    stop_screen_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "STOP_SCREEN_PERIOD",
            "type": "Element",
            "namespace": "",
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    screen_volume_frame: Optional[ScreenVolumeFrameType] = field(
        default=None,
        metadata={
            "name": "SCREEN_VOLUME_FRAME",
            "type": "Element",
            "namespace": "",
        },
    )
    screen_volume_shape: Optional[ScreenVolumeShapeType] = field(
        default=None,
        metadata={
            "name": "SCREEN_VOLUME_SHAPE",
            "type": "Element",
            "namespace": "",
        },
    )
    screen_volume_x: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "SCREEN_VOLUME_X",
            "type": "Element",
            "namespace": "",
        },
    )
    screen_volume_y: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "SCREEN_VOLUME_Y",
            "type": "Element",
            "namespace": "",
        },
    )
    screen_volume_z: Optional[LengthType] = field(
        default=None,
        metadata={
            "name": "SCREEN_VOLUME_Z",
            "type": "Element",
            "namespace": "",
        },
    )
    screen_entry_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "SCREEN_ENTRY_TIME",
            "type": "Element",
            "namespace": "",
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    screen_exit_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "SCREEN_EXIT_TIME",
            "type": "Element",
            "namespace": "",
            "pattern": r"\-?\d{4}\d*-((\d{2}\-\d{2})|\d{3})T\d{2}:\d{2}:\d{2}(\.\d*)?(Z|[+|\-]\d{2}:\d{2})?|[+|\-]?\d*(\.\d*)?",
        },
    )
    collision_probability: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "COLLISION_PROBABILITY",
            "type": "Element",
            "namespace": "",
            "min_inclusive": Decimal("0.0"),
            "max_inclusive": Decimal("1.0"),
        },
    )
    collision_probability_method: Optional[str] = field(
        default=None,
        metadata={
            "name": "COLLISION_PROBABILITY_METHOD",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass
class CdmSegment:
    class Meta:
        name = "cdmSegment"

    metadata: Optional[CdmMetadata] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    data: Optional[CdmData] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class CdmBody:
    class Meta:
        name = "cdmBody"

    relative_metadata_data: Optional[RelativeMetadataData] = field(
        default=None,
        metadata={
            "name": "relativeMetadataData",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    segment: List[CdmSegment] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 2,
            "max_occurs": 2,
        },
    )


@dataclass
class CdmType:
    class Meta:
        name = "cdmType"

    header: Optional[CdmHeader] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    body: Optional[CdmBody] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    id: str = field(
        init=False,
        default="CCSDS_CDM_VERS",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    version: str = field(
        init=False,
        default="1.0",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
