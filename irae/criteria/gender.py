from typing import List
from enum import Enum
from fhirclient.models.coding import Coding
from irae import fhir2sql, guard

class Gender(Enum):
    """
    http://hl7.org/fhir/codesystem-gender-identity.html
    http://hl7.org/fhir/patient.html#gender
    http://hl7.org/fhir/valueset-administrative-gender.html
    """
    male = 'male'
    female = 'female'
    trans_female = 'transgender-female'
    trans_male = 'transgender-male'
    non_binary = 'non-binary'
    non_disclose = 'non-disclose'
    other = 'other'
    unknown = 'unknown'

    def __init__(self, code=None):
        self.system = 'http://hl7.org/fhir/ValueSet/administrative-gender'
        self.code = code
        self.display = code

def sex2codelist(female=True, male=True, other=True, unknown=True) -> List[Coding]:
    codelist = list()

    if female:
        codelist.append(Gender.female)
    if male:
        codelist.append(Gender.male)
    if other:
        codelist.append(Gender.other)
    if unknown:
        codelist.append(Gender.unknown)

    return [guard.as_coding(c) for c in codelist]

def include(female=True, male=True, other=True, unknown=True) -> str:
    codes = sex2codelist(female, male, other, unknown)
    return fhir2sql.include(codes, 'gender')
