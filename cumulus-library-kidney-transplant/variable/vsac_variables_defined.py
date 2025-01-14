from typing import List
from irae.variable.aspect import Variable, Valueset
from irae.variable.aspect import Aspect, AspectMap, Diagnoses, Medications, Labs, Procedures

###############################################################################
#
# Proc Procedures
#
###############################################################################
def get_procedures() -> Procedures:
    return Procedures([
        Variable('Nephrectomy', {
            'sct': '2.16.840.1.113762.1.4.1248.200',
            'icd10pcs': '2.16.840.1.113762.1.4.1248.4'}),
        Variable('Dialysis', {
            'services': '2.16.840.1.113883.3.464.1003.109.12.1013'}),
        Variable('Surgery', {
            'other_major': '2.16.840.1.113883.3.464.1003.198.12.1075'})])

###############################################################################
#
# Dx Diagnosis
#
###############################################################################
def get_diagnoses() -> Diagnoses:
    vars = list()
    vars.append(Variable(
        'Transplant', {
            'kidney': '2.16.840.1.113762.1.4.1078.16',
            'solid_organ': '2.16.840.1.113762.1.4.1032.205',
            'recipient': '2.16.840.1.113762.1.4.1111.27'}))
    vars.append(Variable(
        'Kidney', {
            'condition': '2.16.840.1.113883.17.4077.3.2028',
            'renal_disease': '2.16.840.1.113762.1.4.1029.335',
            'esrd': '2.16.840.1.113762.1.4.1235.172',
            'ckd': '2.16.840.1.113762.1.4.1078.114',
            'dialysis': '2.16.840.1.113762.1.4.1078.342',
            'nephrotic_syndrome': '2.16.840.1.113883.3.464.1003.109.12.1018'}))
    vars.append(Variable(
        'Autoimmune', {
            'inflammatory': '2.16.840.1.113883.3.3157.1834',
            'ibd': '2.16.840.1.113762.1.4.1078.879',
            'crohns': '2.16.840.1.113762.1.4.1034.576',
            'arthritis_ra': '2.16.840.1.113762.1.4.1222.651',
            'arthritis_disorders': '2.16.840.1.113762.1.4.1222.81',
            'lupus': '2.16.840.1.113883.3.464.1003.117.12.1010'}))
    vars.append(Variable(
        'Cancer', {
            'malignant_melanoma_sct': '2.16.840.1.113883.3.1434.1038',
            'malignant_melanoma_icd10': '2.16.840.1.113883.3.464.1003.108.11.1018'}))
    vars.append(Variable(
        'Compromised', {
            'immunocompromised': '2.16.840.1.113883.3.666.5.1940',
            'immunocompromising': '2.16.840.1.113762.1.4.1235.212'}))
    vars.append(Variable(
        'Infection', {
            'bacterial': '2.16.840.1.113762.1.4.1200.288',
            'pna': '2.16.840.1.113762.1.4.1078.738',
            'cmv_icd10': '2.16.840.1.113762.1.4.1146.2234',
            'cmv_sct': '2.16.840.1.113762.1.4.1146.2233',
            'rsv': '2.16.840.1.113762.1.4.1078.754',
            'influenza': '2.16.840.1.113762.1.4.1078.747',
            'shingles': '2.16.840.1.113762.1.4.1222.1478',
            'hepatitis_b': '2.16.840.1.113883.3.464.1003.110.12.1025',
            'hepatitis_c': '2.16.840.1.113762.1.4.1222.30'}))
    vars.append(Variable(
        'Heart', {
            'cardiomyopathy': '2.16.840.1.113762.1.4.1222.579',
            'attack': '2.16.840.1.113883.3.666.5.3011',
            'failure': '2.16.840.1.113762.1.4.1222.1543',
            'cohort': '2.16.840.1.113762.1.4.1182.308'}))
    vars.append(Variable(
        'HTN', {
            'essential': '2.16.840.1.113883.3.464.1003.104.12.1011',
            'any': '2.16.840.1.113762.1.4.1251.12',
            'hypertensive_ckd': '2.16.840.1.113883.3.464.1003.109.12.1017'}))
    vars.append(Variable(
        'Diabetes', {
            'disorder': '2.16.840.1.113762.1.4.1219.35',
            'preexisting': '2.16.840.1.113883.3.464.1003.198.12.1075',
            'complications': '2.16.840.1.113762.1.4.1222.1537',
            'td2_related_dx': '2.16.840.1.113762.1.4.1078.440',
            'diabetic_nephropathy': '2.16.840.1.113883.3.464.1003.109.12.1004',
            'diabetic_ckd': '2.16.840.1.113762.1.4.1078.124'}))
    return Diagnoses(vars)

###############################################################################
#
# Lab Laboratory Observations
#
###############################################################################
def get_labs() -> Labs:
    # return get_lab_analytes()
    panels = get_lab_panels()
    analytes = get_lab_analytes()
    return Labs(panels.variable_list + analytes.variable_list)

def get_lab_panels() -> Labs:
    return Labs([
        Variable('CBC', {'with_diff': '1.3.6.1.4.1.6997.4.1.2.271.13.38167.1.1.999.594'}),
        Variable('CMP', {'comprehensive': '2.16.840.1.113762.1.4.1078.867'}),
        Variable('GFR', {'egfr': '2.16.840.1.113762.1.4.1078.397'}),
        Variable('LFT', {
            'function': '2.16.840.1.113762.1.4.1078.867',
            'ggt': '2.16.840.1.113762.1.4.1222.806',
            'pt': '2.16.840.1.113883.3.3616.200.110.102.5037',
            'inr': '2.16.840.1.113883.3.117.1.7.1.213'})])

def get_lab_analytes() -> Labs:
    return Labs([
        Variable('Creatinine', {
            'serum_cr': '2.16.840.1.113762.1.4.1146.2206',
            'urine_cr': '2.16.840.1.113762.1.4.1178.87',
            'urine_alb_cr_ratio': '2.16.840.1.113883.3.6929.3.1007',
            'urine_protein_cr_ratio': '2.16.840.1.113762.1.4.1222.790',
            'blood_cr': '2.16.840.1.113762.1.4.1222.111'}),
        Variable('Autoimmune', {
            'serum_rf': '2.16.840.1.113762.1.4.1222.812',       # rf= Rheumatoid Factor
            'blood_esr': '2.16.840.1.113762.1.4.1222.1609',     # esr= Erythrocyte Sedimentation Rate
            'crp': '2.16.840.1.113762.1.4.1146.1933',           # crp= C Reactive Protein
            'tsh': '2.16.840.1.113762.1.4.1146.2156',           # tsh= Thyroid Stimulating Hormone
            't3': '2.16.840.1.113762.1.4.1078.864',             # t3= Triiodothyronine
            't4': '2.16.840.1.113762.1.4.1078.865'}),           # t4 = Thyroxine
        Variable('Diabetes', {
            'screening': '2.16.840.1.113762.1.4.1221.122',
            'glucose_test': '2.16.840.1.113762.1.4.1045.134'
        })
    ])

###############################################################################
#
# Rx Medications
#
###############################################################################
def get_medications() -> Medications:
    return Medications([
        Variable('Immunosuppressive', {
            'drugs': '2.16.840.1.113762.1.4.1219.192',
            'systemic_therapy': '2.16.840.1.113883.3.666.5.803',
            'immune_modulators': '2.16.840.1.113762.1.4.1248.124',
            'coricosteroids_systemic': '2.16.840.1.113883.3.3616.200.110.102.2061'}),
        Variable('immunoCompromised', {'therapies': '2.16.840.1.113762.1.4.1235.212'}),
        Variable('diabetes', {'drugs': '2.16.840.1.113762.1.4.1190.58'}),
        Variable('HTN', {'drugs': '2.16.840.1.113883.3.600.1476'}),
        Variable('Diuretics', {
            'loop': '2.16.840.1.113762.1.4.1078.898',
            'potassium': '2.16.840.1.113762.1.4.1213.41',
            'thiazide': '2.16.840.1.113762.1.4.1078.8'})])

###############################################################################
#
# Deprecated - maybe return to these later?
#
###############################################################################
def deprecated() -> List[Variable]:
    return [
        Variable('SurgeryOther', {'surgical_cohort': '2.16.840.1.113762.1.4.1182.127'}),
        Variable('ADE', {
            'common_reactant': '2.16.840.1.113762.1.4.1010.1',
            'common_allergy_intolerance': '2.16.840.1.113762.1.4.1186.8'}),
    ]

def get_aspect_map() -> AspectMap:
    return AspectMap(
        diagnoses=get_diagnoses(),
        medications=get_medications(),
        labs=get_labs(),
        procedures=get_procedures())
