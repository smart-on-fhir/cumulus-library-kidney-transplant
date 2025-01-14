from typing import List
from pathlib import Path
from irae import filetool
from irae import fhir2sql
from irae.variable.aspect import AspectKey
from irae.variable.spreadsheet import SpreadsheetReader, Delimiter, Vocab

VAR_LIST = ['rx_custom', 'lab_custom']

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
    return fhir2sql.name_prefix(VAR_LIST)

def list_view_valuesets_rx() -> List[str]:
    valuesets = [f'rx_{drug}' for drug in RX_LIST]
    valuesets.append('rx_custom')
    return fhir2sql.name_prefix(valuesets)

def list_view_valuesets_lab() -> List[str]:
    valuesets = [f'lab_{lab}' for lab in LAB_LIST]
    valuesets.append('lab_custom')
    return fhir2sql.name_prefix(valuesets)

def union_view_list(rx_or_lab: str, aspect_entries: list, view_name: str) -> Path:
    targets = [f'{rx_or_lab}_{entry}' for entry in aspect_entries]
    targets = fhir2sql.name_prefix(targets)
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
            union_view_list('rx', RX_LIST, f'rx_custom')]

def make() -> List[Path]:
    return make_lab() + make_rx() + make_union()
