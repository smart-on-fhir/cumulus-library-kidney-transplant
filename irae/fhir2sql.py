from typing import List
from pathlib import Path
from fhirclient.models.coding import Coding
from irae import guard, resources, manifest
from irae.resources import save_athena_view

PREFIX = manifest.get_study_prefix()

###############################################################################
#
# naming conventions
#
###############################################################################
def name_prefix(table: list | str) -> list | str:
    if guard.is_list(table):
        return [f'{PREFIX}__{table}' for table in guard.uniq(table)]
    else:
        return f'{PREFIX}__{table}'

def name_suffix(name: str, suffix=None) -> str:
    return f'{name}_{suffix}' if suffix else name

def name_simple(table) -> str:
    simple = table
    for part in ['cohort_', 'count_', 'valueset_']:
        simple = simple.replace(name_prefix(part), '')
    return simple.replace(name_prefix(''), '')

def name_join(part: str, table: str) -> str:
    return name_prefix('_'.join([part, name_simple(table)]))

def name_cohort(table: str, suffix=None) -> str:
    part = name_suffix('cohort', suffix)
    return name_join(part, table)

def name_study_population(suffix=None) -> str:
    table = name_suffix('study_population', suffix)
    return name_join('cohort', table)

def name_study_variables(suffix=None) -> str:
    table = name_suffix('study_variables', suffix)
    return name_join('cohort', table)

def name_cube(table: str, suffix: str) -> str:
    part = f'count_{suffix}' if suffix else 'count'
    return name_join(part, table)

def name_valueset(table: str, suffix=None) -> str:
    part = f'valueset_{suffix}' if suffix else 'valueset'
    return name_join(part, table)

###############################################################################
#
# SQL Helper functions
#
###############################################################################
def sql_escape(sql: str) -> str:
    """
    :param sql: SQL potentially containing special chars
    :return: special chars removed like tic(') and semi(;).
    """
    return sql.replace("'", "").replace(";", ".")

def sql_iter(clauses_list, operator=',') -> str:
    if not isinstance(clauses_list, list):
        return sql_iter([clauses_list])
    return f' {operator} \n'.join(clauses_list)

def sql_and(clauses_list) -> str:
    return sql_iter(clauses_list, 'and')

def sql_or(clauses_list) -> str:
    return sql_iter(clauses_list, 'or')

def sql_list(clauses_list) -> str:
    return sql_iter(clauses_list, ',')

def sql_paren(statement: str) -> str:
    return f'({statement})'


###############################################################################
#
# Transforms X->Y
#
###############################################################################

def valueset2codelist(valueset_json: Path | str) -> List[Coding]:
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
        valueset_json = resources.load_valueset(valueset_json)
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
        safe_display = sql_escape(concept.display)
        content.append(f"('{concept.system}', '{concept.code}', '{safe_display}')")
    content = '\n,'.join(content)
    return header + '\n' + content + '\n' + footer

def criteria2view(view_name, cols: list, values: list) -> Path:
    """
    Single inline_template CVAS statement where col[1...n] = value[1...n]
    :param view_name: create view name
    :param cols: list of column names
    :param values: values for the column names
    :return:
    """
    cols = ','.join(guard.as_list_str(cols))
    values = ','.join(guard.as_list_str(values))
    sql = [f"create or replace view {view_name} as ",
           f"select * from (values",
           f"({values})",
           f") AS t ({cols}) ;"]
    sql = '\n'.join(sql)
    return save_athena_view(view_name, sql)

def union_view_list(view_list: List[str], view_name: str) -> Path:
    dest = name_prefix(view_name)
    cvas = f"create or replace view {PREFIX}__{view_name} as \n "
    select = [f"select '{name_simple(view)}' as subtype, system, code, display from \n {view}" for view in view_list]
    sql = cvas + '\n UNION '.join(select)
    return save_athena_view(dest, sql)

def define(codelist: List[Coding], view_name: str) -> Path:
    dest = name_prefix(view_name)
    sql = codelist2view(codelist, dest)
    return Path(save_athena_view(dest, sql))

def include(codelist: List[Coding], view_name: str) -> Path:
    """
    NOTE: Inclusion criteria is currently supported, not exclusion.
    :param codelist: List of codes to include in selection of `study_population`
    :param view_name: criteria view name
    :return: Path to SQL inclusion criteria file.
    """
    return define(codelist, f'include_{view_name}')

def exclude(codelist: List[Coding], view_name: str) -> Path:
    """
    NOTE: Exclusion criteria is not yet implemented in `study_population`, and may never be.
    :param codelist: List of codes to exclude from `study_population`
    :param view_name: criteria view name
    :return: Path to SQL exclusion criteria file.
    """
    return define(codelist, f'exclude_{view_name}')

###############################################################################
#
# @deprecated
#
###############################################################################

def define_valueset_list_deprecated(valueset_json_list: List[str], view_name: str) -> Path:
    """
    :param valueset_json_list: VSAC ValueSet JSON files
    :param view_name: create view as
    :param include=True (Default)
    :return: outfile path
    """
    codelist = list()
    for filename in valueset_json_list:
        codelist += valueset2codelist(resources.path_valueset(filename))
    return define(codelist, view_name)

def codesystem2codelist_deprecated(code_system_json) -> List[Coding]:
    """
    ValueSet is not always available, sometimes "CodeSystem" is the FHIR spec.
    :param code_system_json:
    :return: List Coding (similar to ValueSet)
    """
    codesystem = resources.load_valueset(code_system_json)
    parsed = list()
    url = codesystem.get('url')
    if 'concept' in codesystem.keys():
        for concept in codesystem['concept']:
            concept['system'] = url
            parsed.append(Coding(concept))
    return parsed
