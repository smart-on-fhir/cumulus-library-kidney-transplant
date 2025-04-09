from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import filetool
from cumulus_library_kidney_transplant import fhir2sql
from cumulus_library_kidney_transplant.variable.aspect import AspectKey
from cumulus_library_kidney_transplant.variable.spreadsheet import SpreadsheetReader, Delimiter, Vocab

# List of aggregated Rx and Lab custom variables.
VAR_LIST = ['rx_custom', 'lab_custom']

# List of Rx Immunosuppressive medications
RX_LIST = ['atg',
           'azathioprine',
           'belatacept',
           'cyclosporin',
           'evorolimus',
           'mycophenolate',
           'sirolimus',
           'tacrolimus']

# List of Lab Drug Levels, important for finding measures of Patient Compliance.
# Example, https://pubmed.ncbi.nlm.nih.gov/15021850/
LAB_DRUG_LIST = ['azathioprine',
                 'azathioprine_tpmt_gene',
                 'cyclosporin',
                 'cytomegalovirus',
                 'mycophenolate',
                 'sirolimus',
                 'tacrolimus']

# List of lab metabolic measures
LAB_METABOLIC_LIST = ['hemoglobin_a1c',
                      'insulin',
                      'c_peptide',
                      'albumin_urine',
                      'ketone_urine',
                      'gad',  # glutamic acid decarboxylase
                      'glucose',
                      'triglyceride',
                      'hdl',
                      'ldl']

# List of other lab viral measures
LAB_VIRUS_LIST = ['cytomegalovirus']

LAB_LIST = LAB_DRUG_LIST + LAB_METABOLIC_LIST + LAB_VIRUS_LIST

DX_TRANSPLANT_LIST = ['transplant_complication',
                      'transplant_donor',
                      'transplant_status']

def deprecated_list_view_valuesets() -> List[str]:
    return list_view_valuesets_rx() + \
           list_view_valuesets_lab() + \
           list_view_valuesets_dx()

def list_view_variables() -> List[str]:
    return fhir2sql.name_prefix(VAR_LIST)

def list_view_valuesets_rx() -> List[str]:
    """
    :return: List of SQL files for each rx in `RX_LIST`
    """
    valuesets = [f'rx_{drug}' for drug in RX_LIST]
    valuesets.append('rx_custom')
    return sorted(list(set(fhir2sql.name_prefix(valuesets))))

def list_view_valuesets_lab() -> List[str]:
    """
    :return: List of SQL files for each lab in `LAB_LIST`
    """
    valuesets = [f'lab_{lab}' for lab in LAB_LIST]
    valuesets.append('lab_custom')
    return sorted(list(set(fhir2sql.name_prefix(valuesets))))

def list_view_valuesets_dx() -> List[str]:
    """
    :return: List of SQL files for each dx in `DX_TRANSPLANT_LIST`
    """
    valuesets = [f'dx_{dx}' for dx in DX_TRANSPLANT_LIST]
    valuesets.append('lab_dx_transplant')
    return sorted(list(set(fhir2sql.name_prefix(valuesets))))

def union_view_list(rx_or_lab: str, variable_list: list, view_name: str) -> Path:
    """
    :param rx_or_lab: "rx" or "lab" target
    :param variable_list: list of variables to aggregate
    :param view_name: Path to SQL table of variables aggregated.
    :return:
    """
    targets = [f'{rx_or_lab}_{entry}' for entry in variable_list]
    targets = fhir2sql.name_prefix(targets)
    return fhir2sql.union_view_list(targets, view_name)

def make_union() -> List[Path]:
    """
    :return: Variable aggregations for SQL query convenience.
    """
    return [union_view_list('lab', LAB_LIST, f'lab_custom'),
            union_view_list('rx', RX_LIST, f'rx_custom')]

def make_aspect(vocab: Vocab, aspect_key: AspectKey, variable_list: list, delimiter: Delimiter) -> List[Path]:
    """
    Make SQL table for each custom variable CSV/TSV definition.

    :param vocab: the "system" for the custom defined valueset
    :param aspect_key: AspectKey: 'lab', 'rx', or 'dx" currently suported
    :param variable_list: List of variable names
    :param delimiter: CSV or TSV data
    :return: List of SQL files for custom variables
    """
    file_list = list()
    for entry in variable_list:
        print(f'custom_variables.py {aspect_key.name}_{entry}')
        filename = filetool.path_spreadsheet(f'{aspect_key.name}_{entry}.{delimiter.name}')
        reader = SpreadsheetReader(filename, entry, vocab, delimiter)
        codes = reader.read_coding_list()
        file_list.append(fhir2sql.define(codes, f'{aspect_key.name}_{entry}'))
    return sorted(list(set(file_list)))

def make_lab() -> List[Path]:
    """
    :return: Lab Variables {system=Vocab.LOINC}
    """
    return make_aspect(Vocab.LOINC, AspectKey.lab, LAB_LIST, Delimiter.csv)

def make_rx() -> List[Path]:
    """
    :return: Lab Variables {system=Vocab.RXNORM}
    """
    return make_aspect(Vocab.RXNORM, AspectKey.rx, RX_LIST, Delimiter.tsv)

def make_dx() -> List[Path]:
    """
    :return: Lab Variables {system=Vocab.ICD10CM}
    """
    return make_aspect(Vocab.ICD10CM, AspectKey.dx, DX_TRANSPLANT_LIST, Delimiter.csv)

def make() -> List[Path]:
    """
    Custom variables are used when VSAC ValueSets are not sufficient for the study needs.

    currently three AspectKey have custom definitions
        * "make_dx()"  --> DX_TRANSPLANT_LIST
        * "make_lab()" --> LAB_LIST
        * "make_rx()"  --> RX_LIST
        # "make_union()" --> Valueset aggregations for SQL convenience.

    Each make target will read custom variable defintions from `spreadsheet/` folder.
    Each csv or tsv file produces a custom valueset with the same column names as a VSAC ValueSet.
    example:
     * code    32594-4
     * display Tacrolimus [Mass] of Dose
     * system  http://loinc.org

     SQL tables are written for each variable to the `athena` folder in the form
        irae__$aspect_$variable

    :return: List of athena SQL files for each custom variable
    """
    return make_dx() + make_lab() + make_rx() + make_union()
