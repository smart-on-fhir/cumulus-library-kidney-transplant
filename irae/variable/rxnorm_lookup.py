from typing import List

###############################################################################
#
# Curated Keywords for Kidney Transplant Drugs
#
###############################################################################
atg = ['ATG',
       'Anti-Thymocyte Globulin',
       'Anti Thymocyte Globulin']

azathioprine = [
    'azathioprine',
    'imuran',
    'Azasan',
    'Thiopurine immunosuppressant',
    '6-Mercaptopurine',
    '6 Mercaptopurine'
]

belatacept = [
    'belatacept',
    'Nulojix',
]

cyclosporin = [
    'cyclosporin',
    'cyclosporine',
    'ciclosporin',
    'Neoral',
    'Sandimmune',
    'Gengraf',
    'Restasis',
    'Cequa',
]

mycophenolate = [
    'mycophenolate',
    'MMF',
    'CellCept',
    'Myfortic',
    'Mycophenolic Acid'
]

sirolimus = [
    'sirolimus',
    'AY-22989',
    'Rapamune',
    'Rapamycin',
    'Streptomyces hygroscopicus',
    'Macrolide immunosuppressant'
]

tacrolimus = [
    'tacrolimus',
    'FK506',
    'prograf',
    'advagraf',
    'Fujimycin',
    'envarsus']


DRUG_LIST = [
    azathioprine,
    atg,
    belatacept,
    cyclosporin,
    mycophenolate,
    sirolimus,
    tacrolimus
]

# For QA checking of missed false positives
class_moa = [
    'immunosuppressant',
    'immunosuppressive',
    'immunomod',
    'calcineurin',
    'Macrolide',
    'systemic corticosteroid'
    'DMARD',
    'CTLA-4'
    'mTOR Inhibitor']

###############################################################################
#
# Simple helper functions
#
###############################################################################

def str_like(keywords: List[str]) -> str:
    _where = list()
    for token in keywords:
        _where.append(f"lower(str) like lower('%{token}%')")
    return '\nOR '.join(_where)

def select_code_display(keywords, sab='RXNORM') -> str:
    _select = 'SELECT distinct code, str as display from umls.MRCONSO_drugs'
    _where = f" WHERE SAB='{sab}' and \n ( {str_like(keywords)})"
    _order = ' order by code, display'

    return _select + _where + _order + ';\n'

###############################################################################
#
# Build a SQL file for executing against UMLS/Athena
#
###############################################################################


if __name__ == "__main__":
    _sql = [select_code_display(drug) for drug in DRUG_LIST]
    _sql = '\n'.join(_sql)

    print(_sql)
