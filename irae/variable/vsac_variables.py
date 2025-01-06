import os
from typing import List
from enum import Enum
from irae import resources
from irae import fhir2sql
from irae.variable import vsac_api

###############################################################################
#
# Surgical
#
###############################################################################
class Nephrectomy(Enum):
    sct = '2.16.840.1.113762.1.4.1248.200'
    icd10pcs = '2.16.840.1.113762.1.4.1248.4'

class Dialysis(Enum):
    services = '2.16.840.1.113883.3.464.1003.109.12.1013'

class SurgeryOther(Enum):
    major = '2.16.840.1.113883.3.464.1003.198.12.1075'
    # cohort = '2.16.840.1.113762.1.4.1182.127'

class AspectProcedure(Enum):
    proc_surgery = SurgeryOther
    proc_dialysis = Dialysis
    proc_nephrectomy = Nephrectomy


###############################################################################
#
# Diagnoses
#
###############################################################################
class DxTransplant(Enum):
    kidney = '2.16.840.1.113762.1.4.1078.16'
    solid_organ = '2.16.840.1.113762.1.4.1032.205'
    recipient = '2.16.840.1.113762.1.4.1111.27'

class DxKidney(Enum):
    condition = '2.16.840.1.113883.17.4077.3.2028'
    renal_disease = '2.16.840.1.113762.1.4.1029.335'
    esrd = '2.16.840.1.113762.1.4.1235.172'
    ckd = '2.16.840.1.113762.1.4.1078.114'
    dialysis = '2.16.840.1.113762.1.4.1078.342'
    nephrotic_syndrome = '2.16.840.1.113883.3.464.1003.109.12.1018'

class DxAutoimmune(Enum):
    inflammatory = '2.16.840.1.113883.3.3157.1834'
    ibd = '2.16.840.1.113762.1.4.1078.879'
    crohns = '2.16.840.1.113762.1.4.1034.576'
    arthritis_ra = '2.16.840.1.113762.1.4.1222.651'
    arthritis_disorders = '2.16.840.1.113762.1.4.1222.81'
    lupus = '2.16.840.1.113883.3.464.1003.117.12.1010'

class DxCancer(Enum):
    # any = '2.16.840.1.113883.3.526.3.1010'
    malignant_melanoma_sct = '2.16.840.1.113883.3.1434.1038'
    malignant_melanoma_icd10 = '2.16.840.1.113883.3.464.1003.108.11.1018'

class DxImmmunoCompromised(Enum):
    immunocompromised = '2.16.840.1.113883.3.666.5.1940'
    immunocompromising = '2.16.840.1.113762.1.4.1235.212'

class DxInfection(Enum):
    # any = '2.16.840.1.113883.17.4077.3.2054'
    # id = '2.16.840.1.113883.10.20.22.5.306'
    bacterial = '2.16.840.1.113762.1.4.1200.288'
    pna = '2.16.840.1.113762.1.4.1078.738'
    cmv_icd10 = '2.16.840.1.113762.1.4.1146.2234'
    cmv_sct = '2.16.840.1.113762.1.4.1146.2233'
    rsv = '2.16.840.1.113762.1.4.1078.754'
    influenza = '2.16.840.1.113762.1.4.1078.747'
    shingles = '2.16.840.1.113762.1.4.1222.1478'
    hepatitis_b = '2.16.840.1.113883.3.464.1003.110.12.1025'
    hepatitis_c = '2.16.840.1.113762.1.4.1222.30'

class DxHeart(Enum):
    cardiomyopathy = '2.16.840.1.113762.1.4.1222.579'
    attack = '2.16.840.1.113883.3.666.5.3011'
    failure = '2.16.840.1.113762.1.4.1222.1543'
    cohort = '2.16.840.1.113762.1.4.1182.308'

class DxHypertension(Enum):
    essential = '2.16.840.1.113883.3.464.1003.104.12.1011'
    any = '2.16.840.1.113762.1.4.1251.12'
    hypertensive_ckd = '2.16.840.1.113883.3.464.1003.109.12.1017'

class DxDiabetes(Enum):
    disorder = '2.16.840.1.113762.1.4.1219.35'
    preexisting = '2.16.840.1.113883.3.464.1003.198.12.1075'
    complications = '2.16.840.1.113762.1.4.1222.1537'
    td2_related_dx = '2.16.840.1.113762.1.4.1078.440'
    diabetic_nephropathy = '2.16.840.1.113883.3.464.1003.109.12.1004'
    diabetic_ckd = '2.16.840.1.113762.1.4.1078.124'

class AspectDx(Enum):
    dx_transplant = DxTransplant
    dx_autoimmune = DxAutoimmune
    dx_cancer = DxCancer
    dx_diabetes = DxDiabetes
    dx_heart = DxHeart
    dx_htn = DxHypertension
    dx_compromised = DxImmmunoCompromised
    dx_infection = DxInfection
    dx_kidney = DxKidney

###############################################################################
#
# Lab Panels
#
###############################################################################
class PanelCBC(Enum):
    with_diff = '1.3.6.1.4.1.6997.4.1.2.271.13.38167.1.1.999.594'

class PanelCMP(Enum):
    comprehensive = '2.16.840.1.113762.1.4.1078.867'

class PanelLFT(Enum):
    hepatic_function = '2.16.840.1.113762.1.4.1078.867'

class AspectLabPanel(Enum):
    lab_panel_cbc = PanelCBC
    lab_panel_cmp = PanelCMP
    lab_panel_lft = PanelLFT

###############################################################################
#
# Lab individual Labs
#
###############################################################################

class LabGFR(Enum):
    eGFR = '2.16.840.1.113762.1.4.1078.397'

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

class LabLFT(Enum):
    ggt = '2.16.840.1.113762.1.4.1222.806'
    pt_prothrombin_time = '2.16.840.1.113883.3.3616.200.110.102.5037'
    inr = '2.16.840.1.113883.3.117.1.7.1.213'

class LabDiabetes(Enum):
    # screening = '2.16.840.1.113762.1.4.1221.122'    # TODO use custom_variables.py HA1C instead?
    glucose_test = '2.16.840.1.113762.1.4.1045.134'

class AspectLab(Enum):
    lab_gfr = LabGFR
    lab_creatinine = LabCreatinine
    lab_autoimmune = LabAutoimmune
    lab_lft = LabLFT
    lab_diabetes = LabDiabetes


###############################################################################
#
# Rx Medications
#
###############################################################################
class RximmunoCompromised(Enum):
    therapies = '2.16.840.1.113762.1.4.1235.212'

class RxDiabetes(Enum):
    drugs = '2.16.840.1.113762.1.4.1190.58'

class RxHypertension(Enum):
    drugs = '2.16.840.1.113883.3.600.1476'

class RxImmunosuppressive(Enum):
    drugs = '2.16.840.1.113762.1.4.1219.192'
    systemic_therapy = '2.16.840.1.113883.3.666.5.803'
    immune_modulators = '2.16.840.1.113762.1.4.1248.124'

class RxSubstance(Enum):
    substance_reactant = '2.16.840.1.113762.1.4.1010.1'
    common_substances_for_allergy_and_intollerance = '2.16.840.1.113762.1.4.1186.8'
    drug_class = '2.16.840.1.113883.3.88.12.80.18'

class RxDiuretics(Enum):
    thiazide = '2.16.840.1.113762.1.4.1078.8'
    loop = '2.16.840.1.113762.1.4.1078.898'
    potassium = '2.16.840.1.113762.1.4.1213.41'

class AspectRx(Enum):
    rx_diabetes = RxDiabetes
    rx_htn = RxHypertension
    rx_immunosuppressive = RxImmunosuppressive
    rx_compromised = RximmunoCompromised
    rx_diuretics = RxDiuretics
    # rx_substance = RxSubstance

###############################################################################
#
# LIST of
#
###############################################################################
def list_aspects() -> List:
    return [AspectProcedure, AspectDx, AspectRx, AspectLab, AspectLabPanel]

def list_view_valuesets() -> List[str]:
    valueset_list = list()
    for aspect in list_aspects():
        for variable in list(aspect):
            for valueset in list(variable.value):
                valueset_list.append(f"{variable.name}_{valueset.name}")
    return fhir2sql.prefix(valueset_list)

def list_view_variables() -> List[str]:
    variable_list = list()
    for aspect in list_aspects():
        for variable in list(aspect):
            variable_list.append(variable.name)
    return fhir2sql.prefix(variable_list)

###############################################################################
#
# Make
#
###############################################################################
def make():
    file_list = list()
    for aspect in list_aspects():
        file_list += make_aspect(aspect)
    return file_list

def make_aspect(aspect) -> List[str]:
    api = vsac_api.UmlsApi()

    var_list = list()

    for variable in list(aspect):
        print(variable)
        valueset_list = list()
        for valueset in list(variable.value):
            print(valueset)

            json_file = resources.path_valueset(f"irae__{variable.name}/{valueset.name}.json")
            view_name = f"irae__{variable.name}_{valueset.name}"
            view_file = resources.path_athena(f'{view_name}.sql')

            if not os.path.exists(json_file):
                json_list = api.get_vsac_valuesets(url=None, oid=valueset.value)
                resources.save_valueset(json_file, json_list)

            if not os.path.exists(view_file):
                code_list = list()
                for entry in resources.read_json(json_file):
                    code_list += fhir2sql.expansion2codelist(entry)
                _sql = fhir2sql.codelist2view(code_list, view_name)
                resources.save_athena_view(view_name, _sql)

            var_list.append(view_file)
            valueset_list.append(view_name)
        var_list.append(fhir2sql.union_view_list(valueset_list, variable.name))
    return var_list
