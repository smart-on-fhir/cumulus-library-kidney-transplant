import os
from typing import List
from enum import Enum
from fhirclient.models.coding import Coding
from kidney_transplant import fhir2sql, common

class EncounterClass(Enum):
    AMB = ('AMB', 'ambulatory')
    EMER = ('EMER', 'emergency')
    FLD = ('FLD', 'field')
    HH = ('HH', 'home health')
    IMP = ('IMP', 'inpatient encounter')
    ACUTE = ('ACUTE', 'inpatient acute')
    NONAC = ('NONAC', 'inpatient non-acute')
    OBSENC = ('OBSENC', 'observation encounter')
    PRENC = ('PRENC', 'pre-admission')
    SS = ('SS', 'short stay')
    VR = ('VR', 'virtual')

    def __init__(self, code, display=None):
        """
        https://terminology.hl7.org/1.0.0//ValueSet-v3-ActEncounterCode.html
        :param code: encounter code
        :param display: display label
        """
        self.system = 'http://terminology.hl7.org/ValueSet/v3-ActEncounterCode'
        self.code = code
        self.display = display

    def as_coding(self) -> Coding:
        c = Coding()
        c.system = self.system
        c.code = self.code
        c.display = self.display
        return c

def as_sql(encounter_class_list: List[EncounterClass]):
    if not encounter_class_list:
        encounter_class_list = list(EncounterClass)

    encounter_class_list = [e.as_coding() for e in encounter_class_list]

    return fhir2sql.coding2view('kidney_transplant__encounter_class', encounter_class_list)
