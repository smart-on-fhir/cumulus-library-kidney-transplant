import os
import json
from enum import Enum
from typing import List
from fhirclient.models.coding import Coding
from kidney_transplant import common, guard

PREFIX = 'kidney_transplant'

###############################################################################
#
# Files: JSON/SQL
#
###############################################################################
def path_valueset(valueset_json: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'valueset', valueset_json)

def path_athena(view_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'athena', f'{view_name}.sql')

def load_valueset(valueset_json: str) -> dict:
    return common.read_json(path_valueset(valueset_json))

def save_sql(view_name, view_sql: str) -> str:
    """
    :param view_name: create view as
    :param view_sql: SQL commands
    :return: outfile path
    """
    return common.write_text(view_sql, path_athena(view_name))

###############################################################################
#
# Transforms X->Y
#
###############################################################################

def valueset2codelist(valueset_json) -> List[Coding]:
    """
    Obtain a list of Coding "concepts" from a ValueSet.
    This method currently supports only "include" of "concept" defined fields.
    Not supported: recursive fetching of contained ValueSets, which requires UMLS API Key and Wget, etc.

    examples
    https://vsac.nlm.nih.gov/valueset/2.16.840.1.113762.1.4.1146.1629/expansion/Latest
    https://cts.nlm.nih.gov/fhir/res/ValueSet/2.16.840.1.113762.1.4.1146.1629?_format=json

    :param valueset_json: ValueSet file, expecially those provided by NLM/ONC/VSAC
    :return: list of codeable concepts (system, code, display) to include
    """
    valueset = load_valueset(valueset_json)
    parsed = list()

    for include in valueset['compose']['include']:
        if 'concept' in include.keys():
            for concept in include['concept']:
                concept['system'] = include['system']
                parsed.append(Coding(concept))
    return parsed

def codesystem2codelist(code_system_json) -> List[Coding]:
    """
    ValueSet is not always available, sometimes "CodeSystem" is the FHIR spec.
    :param code_system_json:
    :return: List Coding (similar to ValueSet)
    """
    codesystem = load_valueset(code_system_json)
    parsed = list()
    url = codesystem.get('url')
    if 'concept' in codesystem.keys():
        for concept in codesystem['concept']:
            concept['system'] = url
            parsed.append(Coding(concept))
    return parsed

def escape(sql: str) -> str:
    """
    :param sql: SQL potentially containing special chars
    :return: special chars removed like tic(') and semi(;).
    """
    return sql.replace("'", "").replace(";", ".")


def codelist2view(codelist: List[Coding], view_name) -> str:
    """
    :param codelist: list of concepts
    :param view_name: like define_type
    :return: SQL command
    """
    header = f"create or replace view {view_name} as select * from (values"
    footer = ") AS t (system, code, display) ;"
    content = list()
    for concept in codelist:
        safe_display = escape(concept.display)
        content.append(f"('{concept.system}', '{concept.code}', '{safe_display}')")
    content = '\n,'.join(content)
    return header + '\n' + content + '\n' + footer

def criteria(codelist: List[Coding], view_name: str, include: bool) -> str:
    _criteria = 'include' if include else 'exclude'
    _dest = f"{PREFIX}__{_criteria}_{view_name}"
    _sql = codelist2view(codelist, _dest)
    return save_sql(_dest, _sql)

def include(codelist: List[Coding], view_name: str) -> str:
    return criteria(codelist, view_name, include=True)

def exclude(codelist: List[Coding], view_name: str) -> str:
    return criteria(codelist, view_name, include=False)

def criteria_valueset_list(valueset_json_list: List[str], view_name: str, include=True) -> str:
    """
    :param valueset_json_list: VSAC ValueSet JSON files
    :param view_name: create view as
    :param include=True (Default)
    :return: outfile path
    """
    codelist = list()
    for filename in valueset_json_list:
        codelist += valueset2codelist(path_valueset(filename))
    return criteria(codelist, view_name, include)

def include_valueset_list(valueset_json_list: List[str], view_name: str) -> str:
    return criteria_valueset_list(valueset_json_list, view_name, include=True)

def exclude_valueset_list(valueset_json_list: List[str], view_name: str) -> str:
    return criteria_valueset_list(valueset_json_list, view_name, include=False)
