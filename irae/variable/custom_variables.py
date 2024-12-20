from typing import List
from irae import fhir2sql
from irae.variable.spreadsheet import SpreadsheetReader, Vocab

RX_LIST = ['atg',
           'azathioprine',
           'belatacept',
           'cyclosporin',
           'sirolimus',
           'tacrolimus']

LAB_LIST = ['azathioprine',
            'cyclosporin',
            'hemoglobin_a1c',
            'sirolimus',
            'azathioprine_tpmt_gene',
            'cytomegalovirus',
            'mycophenolate',
            'tacrolimus']

def union_aspect(aspect: str, aspect_entries: list, view_name: str) -> str:
    targets = [f'{fhir2sql.PREFIX}__{aspect}_{entry}' for entry in aspect_entries]
    return fhir2sql.union_view_list(targets, view_name)

def make_aspect(vocab: Vocab, aspect: str, aspect_entries: list, filetype='csv') -> List[str]:
    delimiter = ',' if filetype == 'csv' else '\t'

    sql_filelist = list()

    for entry in aspect_entries:
        print(f'make {aspect}_{entry}')
        filename = fhir2sql.path_spreadsheet(f'{aspect}_{entry}.{filetype}')
        reader = SpreadsheetReader(filename, entry, vocab)
        codes = reader.read_coding_list(delimiter)
        sql_filelist.append(fhir2sql.define(codes, f'{aspect}_{entry}'))
    return sql_filelist

def make_lab() -> List[str]:
    return make_aspect(Vocab.LOINC, 'lab', LAB_LIST, 'csv')

def make_rx() -> List[str]:
    return make_aspect(Vocab.RXNORM, 'rx', RX_LIST, 'tsv')

def make_union():
    return [union_aspect('lab', LAB_LIST, f'lab_drug_levels'),
            union_aspect('rx', RX_LIST, f'rx_drug_levels')]

def make() -> List[str]:
    return make_lab() + make_rx() + make_union()


if __name__ == "__main__":
    make()






