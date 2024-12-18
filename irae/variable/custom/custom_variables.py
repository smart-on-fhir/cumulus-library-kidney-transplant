from irae import fhir2sql, common
from irae.variable.custom import spreadsheet

LAB_LIST = [
    'azathioprine',
    'cyclosporin',
    'hemoglobin_a1c',
    'sirolimus',
    'azathioprine_tpmt_gene',
    'cytomegalovirus',
    'mycophenolate',
    'tacrolimus']

RX_LIST = [
    'atg',
    'azathioprine',
    'belatacept',
    'cyclosporin',
    'sirolimus',
    'tacrolimus',
]

if __name__ == "__main__":
    for lab in LAB_LIST:
        fhir2sql.path_spreadsheet()
