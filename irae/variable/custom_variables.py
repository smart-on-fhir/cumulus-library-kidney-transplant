from typing import List
from irae import resources
from irae import fhir2sql
from irae.variable.spreadsheet import SpreadsheetReader, Vocab

RX_LIST = ['atg',
           'azathioprine',
           'belatacept',
           'cyclosporin',
           'mycophenolate',
           'sirolimus',
           'tacrolimus']

LAB_LIST = ['azathioprine',
            'azathioprine_tpmt_gene',
            'cyclosporin',
            'cytomegalovirus',
            'hemoglobin_a1c',
            'mycophenolate',
            'sirolimus',
            'tacrolimus']

def list_view_valuesets() -> List[str]:
    return list_view_valuesets_rx() + list_view_valuesets_lab()

def list_view_variables() -> List[str]:
    return list_view_valuesets_rx() + list_view_valuesets_lab()

def list_view_valuesets_rx() -> List[str]:
    var_list = [f'rx_{drug}' for drug in RX_LIST]
    var_list.append('rx_transplant')
    return [f'irae__{var}' for var in var_list]

def list_view_valuesets_lab() -> List[str]:
    var_list = [f'lab_{lab}' for lab in LAB_LIST]
    var_list.append('lab_custom')
    return [f'irae__{var}' for var in var_list]

def union_aspect(aspect: str, aspect_entries: list, view_name: str) -> str:
    targets = [f'irae__{aspect}_{entry}' for entry in aspect_entries]
    return fhir2sql.union_view_list(targets, view_name)

def make_aspect(vocab: Vocab, aspect: str, aspect_entries: list, filetype='csv') -> List[str]:
    file_list = list()
    delimiter = ',' if filetype == 'csv' else '\t'
    for entry in aspect_entries:
        print(f'custom_variables.py {aspect}_{entry}')
        filename = resources.path_spreadsheet(f'{aspect}_{entry}.{filetype}')
        reader = SpreadsheetReader(filename, entry, vocab)
        codes = reader.read_coding_list(delimiter)
        file_list.append(fhir2sql.define(codes, f'{aspect}_{entry}'))
    return file_list

def make_lab() -> List[str]:
    return make_aspect(Vocab.LOINC, 'lab', LAB_LIST, 'csv')

def make_rx() -> List[str]:
    return make_aspect(Vocab.RXNORM, 'rx', RX_LIST, 'tsv')

def make_union():
    return [union_aspect('lab', LAB_LIST, f'lab_custom'),
            union_aspect('rx', RX_LIST, f'rx_transplant')]

def make() -> List[str]:
    return make_lab() + make_rx() + make_union()
