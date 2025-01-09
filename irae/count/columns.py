from enum import Enum
from typing import List
from irae import manifest, guard

PREFIX = manifest.get_study_prefix()

class Table(Enum):
    """
    Template tables for cohorts derived from study population
    """
    study_population = 'study_population'
    cohort = 'cohort'
    casedef = 'casedef'

###############################################################################
# Columnn/Attributes
###############################################################################
class Demographic(Enum):
    """
    Default stratifiers for Demographics
    """
    gender = 'gender'
    race = 'race_display'
    ethnicity = 'ethnicity_display'

class Encounter(Enum):
    """
    Default stratifiers for Encounter
    """
    gender = Demographic.gender.value
    age_at_visit = 'age_at_visit'
    enc_class = 'enc_class_code'
    # enc_type = 'enc_type'
    # enc_service_type = 'enc_service_type'

class Document(Enum):
    doc_type = 'doc_type'

class Diagnosis(Enum):
    category = 'dx_category_code'

class Subtype(Enum):
    subtype = 'subtype'

class Medication(Enum):
    category = 'rx_category_code'

class ObservationLab(Enum):
    code = 'lab_observation_code'

class Cohort(Enum):
    """
    Default stratifiers for Study Cohorts
    """
    gender = Demographic.gender.value
    race = Demographic.race.value
    age_at_visit = Encounter.age_at_visit.value
    enc_class = Encounter.enc_class.value

###############################################################################
# Stratify duration
###############################################################################
class Duration(Enum):
    week = ['enc_period_start_week']
    month = ['enc_period_start_month']
    year = ['enc_period_start_year']

###############################################################################
# Count distinct column
###############################################################################
class CountDistinct(Enum):
    """
    Count distinct FHIR Resource Types
    """
    subject_ref = 'subject_ref'
    encounter_ref = 'encounter_ref'
    observation_ref = 'observation_ref'
    document_ref = 'doc_ref'

###############################################################################
# Helper
###############################################################################
def enum_names(enum_list: List[Enum]) -> List[str]:
    return [entry.name for entry in enum_list]

def enum_values(enum_list: List[Enum]) -> List[str]:
    return [entry.value for entry in enum_list]

class Columns(Enum):
    cohort = enum_values(list(Cohort))
    subtype = enum_values(list(Subtype))
    demographics = enum_values(list(Demographic))
    diagnoses = enum_values(list(Diagnosis))
    medications = enum_values(list(Medication))
    documents = enum_values(list(Document))
    labs = enum_values(list(ObservationLab))
