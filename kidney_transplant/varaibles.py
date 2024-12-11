from enum import Enum
from kidney_transplant import vsac

class DX_Kidney(Enum):
    renal_disease = '2.16.840.1.113762.1.4.1029.335'
    chronic_kidney_disease = '2.16.840.1.113762.1.4.1078.114'
    ckd_stages = '2.16.840.1.113762.1.4.1222.159'
    kidney_stones = '2.16.840.1.113883.17.4077.2.2009'
    dkd_diabetic_kidney_disease = '2.16.840.1.113762.1.4.1078.124'
    hypertensive_ckd = '2.16.840.1.113883.3.464.1003.109.12.1017'
    esrd = '2.16.840.1.113762.1.4.1235.172'

class DX_Autoimmune(Enum):
    inflammatory_and_autoimmune = '2.16.840.1.113762.1.4.1248.124'
    ibd = '2.16.840.1.113762.1.4.1078.879'
    crohns = '2.16.840.1.113762.1.4.1034.576'
    arthritis = '2.16.840.1.113762.1.4.1222.651'
    arthritis_dx = '2.16.840.1.113762.1.4.1222.81'

class DX_Immunocompromised:
    immunocompromised = '2.16.840.1.113883.3.666.5.1940'
    immunocompromising = '2.16.840.1.113762.1.4.1235.212'

class RX_immunocompromised:
    immunocompromised_therapies = '2.16.840.1.113762.1.4.1235.212'

class Treatment(Enum):
    dialysis = '2.16.840.1.113762.1.4.1078.342'

class Transplant(Enum):
    kidney_transplant = '2.16.840.1.113762.1.4.1078.16'
    nephrectomy_sct = '2.16.840.1.113762.1.4.1248.200'
    nephrectomy_icd10 = '2.16.840.1.113762.1.4.1248.4'
    major_transplant = '2.16.840.1.113883.3.464.1003.198.12.1075'
    solid_organ_transplant = '2.16.840.1.113762.1.4.1032.205'
    solid_organ_transplant_recipient = '2.16.840.1.113762.1.4.1111.27'

class Diabetes(Enum):
    preexisting_diabetes = '2.16.840.1.113883.3.464.1003.198.12.1075'
    diabetes_disorder = '2.16.840.1.113762.1.4.1219.35'
    td2_related_conditions = '2.16.840.1.113762.1.4.1078.440'
    complications_due_to_diabetes = '2.16.840.1.113762.1.4.1222.1537'

class Medications(Enum):
    diabetes_rx = '2.16.840.1.113762.1.4.1190.58'

class Immunosuppressive(Enum):
    immunosuppressive = '2.16.840.1.113762.1.4.1219.192'
    systemic_therapy = '2.16.840.1.113883.3.666.5.803'
    immune_modulators = '2.16.840.1.113762.1.4.1248.124'






# umls = vsac.UmlsApi()
#
# print(kidney_conditions)

# kidney_conditions = umls.get_vsac_valuesets(url=None, oid='2.16.840.1.113883.17.4077.3.2028')