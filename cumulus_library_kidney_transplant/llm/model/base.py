from enum import StrEnum
from pydantic import BaseModel, Field

class SpanAugmentedMention(BaseModel):
    """
    A mention of a particular concept in the text, augmented with the character spans 
    where the mention was found.
    This allows for validation of LLM-generated findings, as well as the ability to link
    mentions back to the original text for review and auditing purposes.
    """
    has_mention: bool = Field(
        ...,
        description='Indicates whether the concept was mentioned in the text.'
    )   
    spans: list[str] = Field(
        ...,
        description='The verbatim text where this concept was mentioned.'
    )


##########################################################
#
#           Medication Related Classes/Enums
#
##########################################################

###############################################################################
# Timing related to MedicationRequest.frequency


class RxFrequency(StrEnum):
    """
    QD: once daily (1x/day)
    BID: twice daily (2x/day)
    TID: three times daily (3x/day)
    QID: four times daily (4x/day)
    QOD: every other day (1/2x/day)
    Q6H: every 6 hours (4x/day)
    Q8H: every 8 hours (3x/day)
    Q12H: every 12 hours (2x/day)
    WEEKLY: once every 7 days
    Q2W: once every 2 weeks (14 days)
    Q4W: once every 4 weeks (28 days)
    MONTHLY: once every 4 weeks (28 days)
    OTHER: use timing_text for non-standard frequency
    NONE_OF_THE_ABOVE: None of the above
    """

    QD = "QD"
    BID = "BID"
    TID = "TID"
    QID = "QID"
    QOD = "QOD"
    Q6H = "Q6H"
    Q8H = "Q8H"
    Q12H = "Q12H"
    WEEKLY = "WEEKLY"
    Q2W = "Q2W"
    Q4W = "Q4W"
    MONTHLY = "MONTHLY"
    OTHER = "OTHER"
    NONE_OF_THE_ABOVE = "NONE_OF_THE_ABOVE"


###############################################################################
# MedicationRequest.status


class RxStatus(StrEnum):
    """
    Medication Status (including Intent because chart review is NOT always identical to Med Request)
    https://build.fhir.org/valueset-medicationrequest-status.html
    https://build.fhir.org/valueset-medicationrequest-intent.html

    ACTIVE: Medication order is active (currently prescribed and intended for ongoing use).
    INTENDED: Medication is planned/ordered/prescribed but therapy has not yet started.
    COMPLETED: Medication course is finished (all doses given or intended duration completed).
    STOPPED: Medication was stopped or permanently discontinued before completion.
    CANCELED: Medication order was canceled/withdrawn before any doses were administered.
    ON_HOLD: Medication is temporarily paused (on-hold, suspended, or interrupted).
    NONE_OF_THE_ABOVE: None of the above
    """

    ACTIVE = "ACTIVE"
    INTENDED = "INTENDED"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    CANCELED = "CANCELED"
    ON_HOLD = "ON_HOLD"
    NONE_OF_THE_ABOVE = "NONE_OF_THE_ABOVE"


###############################################################################
# MedicationRequest.category


class RxCategory(StrEnum):
    """
    https://build.fhir.org/valueset-medicationrequest-admin-location.html

    INPATIENT: Medication ordered/administered during an inpatient/acute care setting
    OUTPATIENT: Medication ordered/administered during an outpatient setting
    COMMUNITY: Medication ordered/consumed by the patient in their home (including long term care, nursing homes, etc)
    NONE_OF_THE_ABOVE: None of the above
    """

    INPATIENT = "INPATIENT"
    OUTPATIENT = "OUTPATIENT"
    COMMUNITY = "COMMUNITY"
    NONE_OF_THE_ABOVE = "NONE_OF_THE_ABOVE"


###############################################################################
# MedicationRequest.route


class RxRoute(StrEnum):
    """
    Route of Administration can "help" (but not deterministic) for drug metadata, examples
    * Injection --> antibody for induction/rescue therapy
    * Topical --> skin lesions
    * Inhalation --> Steroid
    https://build.fhir.org/valueset-route-codes.html

    PO: Oral (includes swallowed and sublingual routes)
    NG: Nasogastric/Feeding tube (NG/PEG)
    INJECTION: Injection (IV, SC, or IM)
    INHALATION: Inhalation (respiratory route)
    TOPICAL: Topical (skin or mucosal surface)
    NONE_OF_THE_ABOVE: None of the above
    """

    PO = "PO"
    NG = "NG"
    INJECTION = "INJECTION"
    INHALATION = "INHALATION"
    TOPICAL = "TOPICAL"
    NONE_OF_THE_ABOVE = "NONE_OF_THE_ABOVE"


###############################################################################
# MedicationRequest.dispenseRequest
#
# MedicationRequest.dispenseRequest.validityPeriod


class RxExpectedSupplyDaysMention(SpanAugmentedMention):
    """
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.expectedSupplyDuration
    """

    expected_supply_days: int | None = Field(
        default=None,
        description="Number of days the medication supply is supposed to last (stale dating the prescription)",
    )


# MedicationRequest.dispenseRequest.expectedSupplyDuration
class RxValidityPeriodMention(SpanAugmentedMention):
    """
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.validityPeriod
    """

    start_date: str | None = Field(
        default=None, description="Start date of the prescribed or administered medication"
    )

    end_date: str | None = Field(
        default=None, description="End date of the prescribed or administered medication"
    )


class RxQuantityUnit(StrEnum):
    """
    UCUM unit codes for medication quantity.

    Mass: MG=mg, G=g, UG=ug (microgram/mcg), KG=kg
    Volume: ML=mL, L=L
    International Units: U=U, IU=[iU]
    Countable: TABLET={tablet}, CAPSULE={capsule}, PUFF={puff}, PATCH={patch}, SUPPOSITORY={suppository}
    Ratios: MG_PER_ML=mg/mL, MG_PER_KG=mg/kg, U_PER_KG=U/kg, UG_PER_KG_PER_MIN=ug/kg/min
    Time (infusion rates): H=h, MIN=min, D=d
    NONE_OF_THE_ABOVE: None of the above
    """

    # Mass
    MG = "MG"
    G = "G"
    UG = "UG"
    KG = "KG"

    # Volume
    ML = "ML"
    L = "L"

    # International Units
    U = "U"
    IU = "IU"

    # Countable units
    TABLET = "TABLET"
    CAPSULE = "CAPSULE"
    PUFF = "PUFF"
    PATCH = "PATCH"
    SUPPOSITORY = "SUPPOSITORY"

    # Ratios
    MG_PER_ML = "MG_PER_ML"
    MG_PER_KG = "MG_PER_KG"
    U_PER_KG = "U_PER_KG"
    UG_PER_KG_PER_MIN = "UG_PER_KG_PER_MIN"

    # Time units (for infusion rates)
    H = "H"
    MIN = "MIN"
    D = "D"
    NONE_OF_THE_ABOVE = "NONE_OF_THE_ABOVE"


# MedicationRequest.dispenseRequest.quantity
class RxQuantity(SpanAugmentedMention):
    """
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.quantity
    """

    unit: RxQuantityUnit = Field(
        default=RxQuantityUnit.NONE_OF_THE_ABOVE,
        description=(
            "Medication prescribed unit. "
            "Mass: MG=mg, G=g, UG=ug (microgram), KG=kg; "
            "Volume: ML=mL, L=L; "
            "International Units: U=U, IU=[iU]; "
            "Countable: TABLET, CAPSULE, PUFF, PATCH, SUPPOSITORY; "
            "Ratios: MG_PER_ML, MG_PER_KG, U_PER_KG, UG_PER_KG_PER_MIN; "
            "Time: H=hours, MIN=minutes, D=days; "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    value: str | None = Field(
        default=None,
        description="Numeric amount of medication prescribed or administered (FHIR Quantity.value)",
    )


###############################################################################
# Treatment Phase


class TreatmentPhase(StrEnum):
    """
    Treatment Phase

    INDUCTION: Induction therapy
    MAINTENANCE: Maintenance therapy
    RESCUE: Rescue therapy
    NONE_OF_THE_ABOVE: None of the above
    """

    INDUCTION = "INDUCTION"
    MAINTENANCE = "MAINTENANCE"
    RESCUE = "RESCUE"
    NONE_OF_THE_ABOVE = "NONE_OF_THE_ABOVE"


###############################################################################
# Base class for Medication Mentions


class MedicationMention(SpanAugmentedMention):
    """
    https://build.fhir.org/valueset-medicationrequest-status.html
    https://build.fhir.org/valueset-medicationrequest-admin-location.html
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.expectedSupplyDuration
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.validityPeriod
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.numberOfRepeatsAllowed
    http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.quantity
    """

    status: RxStatus = Field(
        default=RxStatus.NONE_OF_THE_ABOVE,
        description=(
            "What is the status of this medication? "
            "ACTIVE: Medication order is active (currently prescribed and intended for ongoing use); "
            "INTENDED: Medication is planned/ordered/prescribed but therapy has not yet started; "
            "COMPLETED: Medication course is finished (all doses given or intended duration completed); "
            "STOPPED: Medication was stopped or permanently discontinued before completion; "
            "CANCELED: Medication order was canceled/withdrawn before any doses were administered; "
            "ON_HOLD: Medication is temporarily paused (on-hold, suspended, or interrupted); "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    category: RxCategory = Field(
        default=RxCategory.NONE_OF_THE_ABOVE,
        description=(
            "In which healthcare setting is this medication prescribed/administered? "
            "INPATIENT: Medication ordered/administered during an inpatient/acute care setting; "
            "OUTPATIENT: Medication ordered/administered during an outpatient setting; "
            "COMMUNITY: Medication ordered/consumed by the patient in their home (including long term care, nursing homes, etc); "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    route: RxRoute = Field(
        default=RxRoute.NONE_OF_THE_ABOVE,
        description=(
            "What is the route of administration for this medication? "
            "PO: Oral (includes swallowed and sublingual routes); "
            "NG: Nasogastric/Feeding tube (NG/PEG); "
            "INJECTION: Injection (IV, SC, or IM); "
            "INHALATION: Inhalation (respiratory route); "
            "TOPICAL: Topical (skin or mucosal surface); "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    phase: TreatmentPhase = Field(
        default=TreatmentPhase.NONE_OF_THE_ABOVE,
        description=(
            "What is the treatment phase for this medication? "
            "INDUCTION: Induction therapy; "
            "MAINTENANCE: Maintenance therapy; "
            "RESCUE: Rescue therapy; "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    expected_supply_days: int | None = Field(
        default=None,
        description="Number of days the medication supply is supposed to last (stale dating the prescription)",
    )

    number_of_repeats_allowed: int | None = Field(
        default=None,
        description="number of times (aka refills or repeats) that the patient can receive the prescribed medication",
    )

    frequency: RxFrequency = Field(
        default=RxFrequency.NONE_OF_THE_ABOVE,
        description=(
            "What is the frequency of this medication? "
            "QD: once daily; BID: twice daily; TID: three times daily; QID: four times daily; "
            "QOD: every other day; Q6H: every 6 hours; Q8H: every 8 hours; Q12H: every 12 hours; "
            "WEEKLY: once weekly; Q2W: once every 2 weeks; Q4W: once every 4 weeks; MONTHLY: once monthly; "
            "OTHER: non-standard frequency (use timing_text); "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    start_date: str | None = Field(
        None, description="Start date of the prescribed or administered medication"
    )

    end_date: str | None = Field(
        None, description="End date of the prescribed or administered medication"
    )

    quantity_unit: RxQuantityUnit = Field(
        RxQuantityUnit.NONE_OF_THE_ABOVE,
        description=(
            "Medication prescribed unit. "
            "Mass: MG=mg, G=g, UG=ug (microgram), KG=kg; "
            "Volume: ML=mL, L=L; "
            "International Units: U=U, IU=[iU]; "
            "Countable: TABLET, CAPSULE, PUFF, PATCH, SUPPOSITORY; "
            "Ratios: MG_PER_ML, MG_PER_KG, U_PER_KG, UG_PER_KG_PER_MIN; "
            "Time: H=hours, MIN=minutes, D=days; "
            "NONE_OF_THE_ABOVE: None of the above"
        ),
    )

    quantity_value: str | None = Field(
        None,
        description="Numeric amount of medication prescribed or administered (FHIR Quantity.value)",
    )
