from typing import List
from pathlib import Path
from irae import filetool
from irae import fhir2sql
from irae.variable.aspect import AspectKey
from irae.variable.spreadsheet import SpreadsheetReader, Delimiter, Vocab

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

def union_view_list(rx_or_lab: str, aspect_entries: list, view_name: str) -> Path:
    targets = [f'irae__{rx_or_lab}_{entry}' for entry in aspect_entries]
    return fhir2sql.union_view_list(targets, view_name)

def make_aspect(vocab: Vocab, aspect_key: AspectKey, aspect_entries: list, delimiter: Delimiter) -> List[Path]:
    file_list = list()
    for entry in aspect_entries:
        print(f'custom_variables.py {aspect_key.name}_{entry}')
        filename = filetool.path_spreadsheet(f'{aspect_key.name}_{entry}.{delimiter.name}')
        reader = SpreadsheetReader(filename, entry, vocab, delimiter)
        codes = reader.read_coding_list()
        file_list.append(fhir2sql.define(codes, f'{aspect_key.name}_{entry}'))
    return file_list

def make_lab() -> List[Path]:
    return make_aspect(Vocab.LOINC, AspectKey.lab, LAB_LIST, Delimiter.csv)

def make_rx() -> List[Path]:
    return make_aspect(Vocab.RXNORM, AspectKey.rx, RX_LIST, Delimiter.tsv)

def make_union():
    return [union_view_list('lab', LAB_LIST, f'lab_custom'),
            union_view_list('rx', RX_LIST, f'rx_transplant')]

def make() -> List[Path]:
    return make_lab() + make_rx() + make_union()
