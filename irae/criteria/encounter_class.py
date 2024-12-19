import os
from typing import List
from enum import Enum
from fhirclient.models.coding import Coding
from irae import fhir2sql, common

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
