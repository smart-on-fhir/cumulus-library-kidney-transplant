from typing import List
from fhirclient.models.coding import Coding
from irae import fhir2sql

VALUESET_DOCTYPE = 'valueset-c80-doc-typecodes.json'
VALUESET_FACILITY = 'valueset-c80-facilitycodes.json'
VALUESET_PRACTICE = 'valueset-c80-practice-codes.json'

###############################################################################
#
# Get Coding using the "key" code
#
#   *DocType
#   *Facility
#   *Practice
#
#
###############################################################################

def get_coding_doctype(code: str) -> Coding:
    return get_coding(code, VALUESET_DOCTYPE)

def get_coding_facility(code: str) -> Coding:
    return get_coding(code, VALUESET_FACILITY)

def get_coding_practice(code: str) -> Coding:
    return get_coding(code, VALUESET_PRACTICE)

def get_coding(code: str, valueset_json: str) -> Coding:
    """
    :param code: code to find in valueset
    :param valueset_json: ValueSet containing [System, Code, Display]
    :return: Coding type
    """
    for entry in fhir2sql.valueset2codelist(valueset_json):
        if entry.code == code:
            return entry

###############################################################################
#
# Get ValueSet
#
#   *DocType
#   *Facility
#   *Practice
#
###############################################################################

def get_valueset_doctype() -> List[Coding]:
    return fhir2sql.valueset2codelist(VALUESET_DOCTYPE)

def get_valueset_facility() -> List[Coding]:
    return fhir2sql.valueset2codelist(VALUESET_FACILITY)

def get_valueset_practice() -> List[Coding]:
    return fhir2sql.valueset2codelist(VALUESET_PRACTICE)
