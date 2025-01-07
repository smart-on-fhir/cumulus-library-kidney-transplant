from typing import List
from irae.variable import vsac_variables

###############################################################################
#
# Make
#
###############################################################################
def make() -> str:
    markdown_list = list()
    for aspect in vsac_variables.list_aspects():
        markdown_list += make_markdown(aspect)
    return header() + '\n'.join(markdown_list)

def header() -> str:
    return columns() + '\n' + line() + '\n'

def columns() -> str:
    return '|Variable|Subtype|VSAC|'

def line() -> str:
    return '|:------:|:-----:|:---:|'

def vsac(oid) -> str:
    url = f'https://vsac.nlm.nih.gov/valueset/{oid}/expansion/Latest'
    return f'[{oid}]({url})'

def make_markdown(aspect) -> List[str]:
    table = list()
    for variable in list(aspect):
        table.append(f'|**{variable.name}**||')
        for valueset in list(variable.value):
            table.append(f'|{variable.name}|{valueset.name}|{vsac(valueset.value)}|')
    return table
