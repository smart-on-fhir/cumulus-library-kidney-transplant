import os
from typing import List
from fhirclient.models.coding import Coding
from kidney_transplant import fhir2sql

def include_document_type(doctype_list: List[Coding]) -> str:
    criteria_document_type(doctype_list, True)

def exclude_document_type(doctype_list: List[Coding]) -> str:
    criteria_document_type(doctype_list, False)

def criteria_document_type(doctype_list: List[Coding], include=True) -> str:
    if not doctype_list:
        doctype_list = fhir2sql.valueset2codelist('valueset-c80-doc-typecodes.json')

    return fhir2sql.criteria(doctype_list, 'document_type', include)

def include_facility_codes(facility_list: List[Coding]) -> str:
    return criteria_facility_codes(facility_list, True)

def exclude_facility_codes(facility_list: List[Coding]) -> str:
    return criteria_facility_codes(facility_list, False)

def criteria_facility_codes(facility_list: List[Coding], include=True) -> str:
    if not facility_list:
        facility_list = fhir2sql.valueset2codelist('valueset-c80-facilitycodes.json')

    return fhir2sql.criteria(facility_list, 'facility_codes', include)

def criteria_practice_codes(practice_list: List[Coding], include=True) -> str:
    if not practice_list:
        practice_list = fhir2sql.valueset2codelist('valueset-c80-practice-codes.json')

    return fhir2sql.criteria(practice_list, 'practice_codes', include)
