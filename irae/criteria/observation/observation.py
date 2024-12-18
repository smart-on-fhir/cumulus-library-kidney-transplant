import os
from enum import Enum
from typing import List
from fhirclient.models.coding import Coding
from irae import common, fhir2sql

class ObservationCategory(Enum):

    social_history = ('social-history', 'Occupational, lifestyle, social, familial, environmental, health risk factors')
    vital_signs = ('vital-signs', 'Vital Signs: BP, HR, RR, height, weight, BMI, head circumference, O2SAT, Temp')
    imaging = ('imaging', 'x-ray, ultrasound, CT, MRI, angiography, echocardiography, and nuclear medicine')
    laboratory = ('laboratory', 'chem, heme, serology, histology, cytology, pathology, microbiology, virology')
    procedure = ('procedure', 'interventional and non-interventional procedures')
    survey = ('survey', 'assessment tool/survey instrument observations')
    exam = ('exam', 'physical exam findings')
    therapy = ('therapy', 'occupational, physical, radiation, nutritional and medication therapy')
    activity = ('activity', 'bodily activity that enhances or maintains physical fitness')

    def __init__(self, code, display):
        self.system = 'http://terminology.hl7.org/CodeSystem/observation-category'
        self.code = code
        self.display = display


def enum2codelist(category_list: List[ObservationCategory]) -> List[Coding]:
    if not category_list:
        category_list = fhir2sql.codesystem2codelist('CodeSystem-observation-category.json')

    return [fhir2sql.as_coding(c) for c in category_list]
