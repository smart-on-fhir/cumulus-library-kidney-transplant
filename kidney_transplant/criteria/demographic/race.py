import os
from typing import List
from enum import Enum
from fhirclient.models.coding import Coding
from kidney_transplant import fhir2sql, common

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

    def as_coding(self) -> Coding:
        c = Coding()
        c.system = self.system
        c.code = self.code
        c.display = self.display
        return c


def filepath(filename: str) -> str:
    pwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(pwd, filename)

def as_sql(race_list: None | List[Race]) -> str:
    """
    :param race_list: List of Race codes from CDC. Default = all races.
    :return: str SQL statement for create view $studyname__demographic_race
    """
    """
    :param race_list: list of supported race types
    :return:
    """
    if not race_list:
        race_list = list(Race)

    race_list = [r.as_coding() for r in race_list]

    return fhir2sql.coding2view('kidney_transplant__demographic_race', race_list)
