import os
from enum import Enum
from typing import List
from pathlib import Path
from irae import resources
from irae import fhir2sql
from irae.fhir2sql import PREFIX
from irae.variable import vsac_api
from irae.variable.aspect import Aspect, AspectMap, AspectKey
from irae.variable.vsac_variables_defined import get_aspect_map

###############################################################################
#
# LIST of
#
###############################################################################

def list_view_valuesets() -> List[str]:
    valueset_list = list()
    for aspect in get_aspect_map().as_list():
        for variable in aspect.variable_list:
            for valueset in variable.valuesets:
                valueset_list.append(f"{variable.name}_{valueset.name}")
    return fhir2sql.name_prefix(valueset_list)

def list_view_variables() -> List[str]:
    variable_list = list()
    for aspect in get_aspect_map().as_list():
        for variable in aspect.variable_list:
            variable_list.append(variable.name)
    return fhir2sql.name_prefix(variable_list)

###############################################################################
#
# Make
#
###############################################################################
def make_aspect(aspect: Aspect) -> List[Path]:
    """
    :param aspect: see `list_aspects()`, Dx, Rx, Lab, LabPanel, Proc
    :return: Path to SQL File to create variable definition valuesets.
    """
    api = vsac_api.UmlsApi()
    var_list = list()
    print('================================')
    print(f'* aspect {aspect.key.as_json()}')
    for variable in aspect.variable_list:
        print(f'** {variable.name}')
        valueset_list = list()
        for valueset in variable.valuesets:
            print(f'*** {variable.name} -> {valueset.name}')
            json_file = resources.path_valueset(f"{PREFIX}__{variable.name}/{valueset.name}.json")
            view_name = f"{PREFIX}__{variable.name}_{valueset.name}"
            view_file = resources.path_athena(f'{view_name}.sql')

            if not os.path.exists(json_file):
                print(f'**** Downloading {variable.name} {valueset.as_json()}')
                json_list = api.get_vsac_valuesets(url=None, oid=valueset.oid)
                resources.save_valueset(json_file, json_list)

            if not os.path.exists(view_file):
                print(f'**** Writing {view_file}')
                code_list = list()
                for entry in resources.read_json(json_file):
                    code_list += fhir2sql.expansion2codelist(entry)
                sql = fhir2sql.codelist2view(code_list, view_name)
                resources.save_athena_view(view_name, sql)

            var_list.append(view_file)
            valueset_list.append(view_name)
        var_list.append(fhir2sql.union_view_list(valueset_list, variable.name))
    return var_list

def make() -> List[Path]:
    """
    Make vsac variables with 1+ vsac valuesets for each variable.
    :return: List SQL files to define each vsac_variable
    """
    file_list = list()
    for aspect in get_aspect_map().as_list():
        file_list += make_aspect(aspect)
    return file_list


if __name__ == "__main__":
    make()
