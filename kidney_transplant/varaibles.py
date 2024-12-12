from enum import Enum
from kidney_transplant import vsac

class DxKidney(Enum):
    renal_disease = '2.16.840.1.113762.1.4.1029.335'
    chronic_kidney_disease = '2.16.840.1.113762.1.4.1078.114'
    ckd_stages = '2.16.840.1.113762.1.4.1222.159'
    diabetic_nephropathy = '2.16.840.1.113883.3.464.1003.109.12.1004'
    kidney_stones = '2.16.840.1.113883.17.4077.2.2009'
    dkd_diabetic_kidney_disease = '2.16.840.1.113762.1.4.1078.124'
    hypertensive_ckd = '2.16.840.1.113883.3.464.1003.109.12.1017'
    esrd = '2.16.840.1.113762.1.4.1235.172'

class DxAutoimmune(Enum):
    inflammatory_and_autoimmune = '2.16.840.1.113762.1.4.1248.124'
    ibd = '2.16.840.1.113762.1.4.1078.879'
    crohns = '2.16.840.1.113762.1.4.1034.576'
    arthritis = '2.16.840.1.113762.1.4.1222.651'
    arthritis_dx = '2.16.840.1.113762.1.4.1222.81'

class DxCancer(Enum):
    cancer = '2.16.840.1.113883.3.526.3.1010'
    malignant_melanoma_sct = '2.16.840.1.113883.3.1434.1038'
    malignant_melanoma_icd10 = '2.16.840.1.113883.3.464.1003.108.11.1018'

class DxInfection(Enum):
    infection = '2.16.840.1.113883.17.4077.3.2054'
    infectious_disease = '2.16.840.1.113883.10.20.22.5.306'
    bacterial = '2.16.840.1.113762.1.4.1200.288'
    pna = '2.16.840.1.113762.1.4.1078.738'
    cmv_icd10 = '2.16.840.1.113762.1.4.1146.2234'
    cmv_sct = '2.16.840.1.113762.1.4.1146.2233'
    rsv = '2.16.840.1.113762.1.4.1078.754'
    influenza = '2.16.840.1.113762.1.4.1078.747'
    shingles = '2.16.840.1.113762.1.4.1222.1478'
    hepatitis_b = '2.16.840.1.113883.3.464.1003.110.12.1025'
    hepatitis_c = '2.16.840.1.113762.1.4.1222.30'

class DxImmunocompromised:
    immunocompromised = '2.16.840.1.113883.3.666.5.1940'
    immunocompromising = '2.16.840.1.113762.1.4.1235.212'

class DxHeart(Enum):
    cardiomyopathy = '2.16.840.1.113762.1.4.1222.579'
    heart_attack = '2.16.840.1.113883.3.666.5.3011'
    heart_failure = '2.16.840.1.113762.1.4.1222.1543'
    cardiovascular_cohort = ' 2.16.840.1.113762.1.4.1182.308'

class Rximmunocompromised:
    immunocompromised_therapies = '2.16.840.1.113762.1.4.1235.212'

class Dialysis(Enum):
    dialysis = '2.16.840.1.113762.1.4.1078.342'

class Surgery(Enum):
    kidney_transplant = '2.16.840.1.113762.1.4.1078.16'
    nephrectomy_sct = '2.16.840.1.113762.1.4.1248.200'
    nephrectomy_icd10 = '2.16.840.1.113762.1.4.1248.4'
    major_transplant = '2.16.840.1.113883.3.464.1003.198.12.1075'
    solid_organ_transplant = '2.16.840.1.113762.1.4.1032.205'
    solid_organ_transplant_recipient = '2.16.840.1.113762.1.4.1111.27'
    surgery_cohort_icd10 = '2.16.840.1.113762.1.4.1182.127'

class Diabetes(Enum):
    preexisting_diabetes = '2.16.840.1.113883.3.464.1003.198.12.1075'
    diabetes_disorder = '2.16.840.1.113762.1.4.1219.35'
    td2_related_conditions = '2.16.840.1.113762.1.4.1078.440'
    complications_due_to_diabetes = '2.16.840.1.113762.1.4.1222.1537'

class RxDiabetes(Enum):
    diabetes_medications = '2.16.840.1.113762.1.4.1190.58'

class RxImmunosuppressive(Enum):
    immunosuppressive = '2.16.840.1.113762.1.4.1219.192'
    systemic_therapy = '2.16.840.1.113883.3.666.5.803'
    immune_modulators = '2.16.840.1.113762.1.4.1248.124'

class RxSubstance(Enum):
    substance_reactant = '2.16.840.1.113762.1.4.1010.1'
    common_substances_for_allergy_and_intollerance = '2.16.840.1.113762.1.4.1186.8'
    drug_class = '2.16.840.1.113883.3.88.12.80.18'

class LabGFR(Enum):
    eGFR = '2.16.840.1.113883.3.88.12.80.18'

class LabCreatinine(Enum):
    serum_cr = '2.16.840.1.113762.1.4.1146.2206'
    urine_cr = '2.16.840.1.113762.1.4.1178.87'
    urine_alb_cr_ratio = '2.16.840.1.113883.3.6929.3.1007'
    urine_protein_cr_ratio = '2.16.840.1.113762.1.4.1222.790'
    blood_cr = '2.16.840.1.113762.1.4.1222.111'

class LabAutoimmune(Enum):
    serum_rf = '2.16.840.1.113762.1.4.1222.812'     # Rheumatoid Factor
    blood_esr = '2.16.840.1.113762.1.4.1222.1609'   # Erythrocyte Sedimentation Rate
    crp = '2.16.840.1.113762.1.4.1146.1933'         # C Reactive Protein
    tsh = '2.16.840.1.113762.1.4.1146.2156'         # Thyroid Stimulating Hormone
    t3 = '2.16.840.1.113762.1.4.1078.864'           # Triiodothyronine
    t4 = '2.16.840.1.113762.1.4.1078.865'           # Thyroxine

class PanelCBC(Enum):
    cbc_with_diff = '1.3.6.1.4.1.6997.4.1.2.271.13.38167.1.1.999.594'

class PanelCMP(Enum):
    bmp_cmp = '2.16.840.1.113762.1.4.1078.867'

class PanelLFT(Enum):
    hepatic_function = '2.16.840.1.113762.1.4.1078.867'

class LabLFT(Enum):
    ggt = '2.16.840.1.113762.1.4.1222.806'
    pt_prothrombin_time = '2.16.840.1.113883.3.3616.200.110.102.5037'
    inr = '2.16.840.1.113883.3.117.1.7.1.213'

class LabDiabetes(Enum):
    diabetes_screening = '2.16.840.1.113762.1.4.1221.122'
    glucose_test = '2.16.840.1.113762.1.4.1045.134'

