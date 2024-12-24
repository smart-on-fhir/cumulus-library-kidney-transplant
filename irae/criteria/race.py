from typing import List
from enum import Enum
from fhirclient.models.coding import Coding
from irae import common, fhir2sql

class Race(Enum):
    """
    Race coding has 5 "root" levels, called the R5 shown below.
    http://hl7.org/fhir/r4/v3/Race/cs.html
    """
    asian = ('2028-9', 'Asian')
    black = ('2054-5', 'Black or African American')
    native_american_or_alaska = ('1002-5', 'American Indian or Alaska Native')
    native_hawaiian_pacific_islander = ('2076-8', 'Native Hawaiian or Other Pacific Islander')
    white = ('2106-3', 'White')

    def __init__(self, code, display=None):
        self.system = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'
        self.code = code
        self.display = display

def include(race_list=None) -> str:
    if not race_list:
        race_list = list(Race)
    codes = common.as_coding_list(race_list)
    return fhir2sql.include(codes, 'race')
