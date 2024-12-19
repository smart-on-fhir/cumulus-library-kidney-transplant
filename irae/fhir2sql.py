import os
import json
from enum import Enum
from typing import List
from fhirclient.models.coding import Coding
from irae import common, guard

PREFIX = 'irae'

###############################################################################
#
# Files: JSON/SQL
#
###############################################################################
def exists_valueset(valueset_file: str) -> bool:
    return os.path.exists(path_valueset(valueset_file))

def path_valueset(valueset_json: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'valueset', valueset_json)

def path_athena(view_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'athena', f'{view_name}.sql')

def path_spreadsheet(table_filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'spreadsheet', f'{table_filename}')

def load_valueset(valueset_json: str) -> dict:
    return common.read_json(path_valueset(valueset_json))

def make_subdir(subdir: str):
    os.makedirs(path_valueset(subdir), exist_ok=True)

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
    if isinstance(valueset_json, str):
        valueset_json = load_valueset(valueset_json)

    parsed = list()

    if not valueset_json.get('compose'):
        print('warning, no valueset content. Extension?')
        return list()

    for include in valueset_json['compose']['include']:
        if 'concept' in include.keys():
            for concept in include['concept']:
                concept['system'] = include['system']
                parsed.append(Coding(concept))
    return parsed

def expansion2codelist(valueset_json: dict) -> List[Coding]:
    contains = valueset_json.get('expansion').get('contains')
    return [Coding(c) for c in contains]

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

def union_view_list(view_list: List[str], view_name: str) -> str:
    _dest = f"{PREFIX}__{view_name}"
    _header = f"create or replace view {PREFIX}__{view_name} as \n "
    _select = [f"select '{item}' as subtype, system, code, display from \n {item}" for item in view_list]
    _sql = _header + '\n UNION '.join(_select)
    return save_sql(_dest, _sql)

def define(codelist: List[Coding], view_name: str) -> str:
    _dest = f"{PREFIX}__{view_name}"
    _sql = codelist2view(codelist, _dest)
    return save_sql(_dest, _sql)

def define_valueset_list(valueset_json_list: List[str], view_name: str, include=True) -> str:
    """
    :param valueset_json_list: VSAC ValueSet JSON files
    :param view_name: create view as
    :param include=True (Default)
    :return: outfile path
    """
    codelist = list()
    for filename in valueset_json_list:
        codelist += valueset2codelist(path_valueset(filename))
    return define(codelist, view_name, include)

def include(codelist: List[Coding], view_name: str) -> str:
    return define(codelist, f'include_{view_name}')

def exclude(codelist: List[Coding], view_name: str) -> str:
    return define(codelist, f'exclude_{view_name}')
