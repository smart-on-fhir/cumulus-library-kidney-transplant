import os
from kidney_transplant import common, fhir2sql

def filepath(filename: str) -> str:
    pwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(pwd, filename)

def document_type() -> str:
    valueset = fhir2sql.valueset2coding(filepath('valueset-c80-doc-typecodes.json'))
    return fhir2sql.coding2view('kidney_transplant__document_type', valueset)

def facility_codes() -> str:
    valueset = fhir2sql.valueset2coding(filepath('valueset-c80-facilitycodes.json'))
    return fhir2sql.coding2view('kidney_transplant__document_facility_codes', valueset)

def practice_codes() -> str:
    valueset = fhir2sql.valueset2coding(filepath('valueset-c80-practice-codes.json'))
    return fhir2sql.coding2view('kidney_transplant__document_practice_codes', valueset)
