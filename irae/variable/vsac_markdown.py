from typing import List
from pathlib import Path
from irae import resources
from irae.variable.aspect import Aspect
from irae.variable import vsac_variables

###############################################################################
#
# Make
#
###############################################################################
def make() -> str:
    syntax_list = list()
    for aspect in vsac_variables.get_aspect_map().as_list():
        syntax_list += make_markdown_for(aspect)
    markdown = header() + '\n'.join(syntax_list)
    return resources.write_text(markdown, path_readme())

def make_markdown_for(aspect: Aspect) -> List[str]:
    table = list()
    for variable in aspect.variable_list:
        table.append(f'|**{variable.name}**||')
        for valueset in list(variable.valueset_list):
            table.append(f'|{variable.name}|{valueset.name}|{vsac(valueset.oid)}|')
    return table

def path_readme() -> Path:
    return resources.path_parent('README.md')

def header() -> str:
    H1 = '# VSAC ValueSets'
    return H1 + '\n\n' + columns() + '\n' + line() + '\n'

def columns() -> str:
    return '|Study Variable|Subtype|VSAC|'

def line() -> str:
    return '|:------:|:-----:|:---:|'

def vsac(oid) -> str:
    url = f'https://vsac.nlm.nih.gov/valueset/{oid}/expansion/Latest'
    return f'[{oid}]({url})'
