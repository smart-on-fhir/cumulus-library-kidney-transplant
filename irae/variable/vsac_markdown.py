from typing import List
from pathlib import Path
from irae import resources
from irae.variable import vsac_variables

###############################################################################
#
# Make
#
###############################################################################
def make() -> str:
    syntax_list = list()
    for aspect in vsac_variables.list_aspects():
        syntax_list += make_markdown_for(aspect)
    markdown = header() + '\n'.join(syntax_list)
    return resources.write_text(markdown, path_readme())

def make_markdown_for(aspect) -> List[str]:
    table = list()
    for variable in list(aspect):
        table.append(f'|**{variable.name}**||')
        for valueset in list(variable.value):
            table.append(f'|{variable.name}|{valueset.name}|{vsac(valueset.value)}|')
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
