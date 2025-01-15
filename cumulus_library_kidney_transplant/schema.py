from enum import Enum
from typing import List
from cumulus_library_kidney_transplant import manifest
from cumulus_library_kidney_transplant.guard import as_list_values
from cumulus_library_kidney_transplant.study_prefix import PREFIX

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
    type_display = 'doc_type_display'

class Diagnosis(Enum):
    category = 'dx_category_code'
    code_display = 'dx_display'

class Medication(Enum):
    category = 'rx_category_code'
    code_display = 'rx_display'

class Procedure(Enum):
    code_display = 'proc_display'

class ObservationLab(Enum):
    code = 'lab_observation_code'

class Cohort(Enum):
    """
    Default stratifiers for Study Cohorts
    """
    gender = Demographic.gender.value
    age_at_visit = Encounter.age_at_visit.value
    enc_class = Encounter.enc_class.value

class CohortSubtype(Enum):
    gender = Demographic.gender.value
    race = Demographic.race.value
    age_at_visit = Encounter.age_at_visit.value
    enc_class = Encounter.enc_class.value
    subtype = 'subtype'


###############################################################################
# Stratify duration
###############################################################################
class Duration(Enum):
    """
    enc_period_start_day is not included as that could trigger HIPAA considerations
    also, counts would be so small anyway that it wouldn't be useful in nearly all cases.
    """
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
class Columns(Enum):
    cohort = as_list_values(list(Cohort))
    cohort_subtype = as_list_values(list(CohortSubtype))
    encounter = as_list_values(list(Encounter))
    demographics = as_list_values(list(Demographic))
    diagnoses = as_list_values(list(Diagnosis))
    medications = as_list_values(list(Medication))
    documents = as_list_values(list(Document))
    procedures = as_list_values(list(Procedure))
    labs = as_list_values(list(ObservationLab))
