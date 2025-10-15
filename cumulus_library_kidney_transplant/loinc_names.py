from pathlib import Path
import pandas as pd
from cumulus_library_kidney_transplant import filetool, fhir2sql

##############################################################################
# LOINC 2.8.1 files
#
#   For simplicity, these CSV files have been processed into "valueset",
#   code, display, system='http://loinc.org'
#
##############################################################################
LOINC_CSV = filetool.path_spreadsheet('Loinc.csv')
LOINC_VALUESET_CSV = filetool.path_spreadsheet('Loinc_valueset.csv')

def loinc2valueset() -> None:
    """
    Save LOINC_CSV as {code,display,system}
    """
    entries = list()
    for row in pd.read_csv(LOINC_CSV).itertuples(index=False):
        entries.append({'system': 'http://loinc.org',
                        'code': row.LOINC_NUM,
                        'display': row.LONG_COMMON_NAME})
    entries = sorted(entries, key=lambda x: x['code'])
    valueset_csv = pd.DataFrame.from_records(entries)
    valueset_csv.to_csv(LOINC_VALUESET_CSV, index=False)

def hydrate(valueset_csv:Path, view_name:str) -> None:
    loinc_df = pd.read_csv(LOINC_VALUESET_CSV)
    valueset_df = pd.read_csv(valueset_csv)

    valueset_keys = set(valueset_df['code'].dropna().unique())
    loinc_keys = set(loinc_df['code'].dropna().unique())

    print(valueset_csv)
    print(len(valueset_keys), ' #valueset')
    print(len(loinc_keys), ' #loinc (official)')
    print(len(valueset_keys & loinc_keys), ' #intersection')
    print(len(loinc_keys - valueset_keys), ' #difference loinc')
    print(len(valueset_keys - loinc_keys), ' #difference valueset')

    if valueset_keys - loinc_keys:
        print('missing ', valueset_keys - loinc_keys)

    # if not valueset_csv.exists():
    #     print(valueset_csv, 'does not exist')

    temp_csv = str(valueset_csv) + '.hydrate.csv'

    filtered = loinc_df[loinc_df['code'].isin(valueset_keys)].copy()
    filtered.to_csv(filetool.path_spreadsheet(temp_csv), index=False)
    fhir2sql.csv2view(Path(temp_csv), view_name)


if __name__ == "__main__":
    valueset_csv = filetool.path_spreadsheet('lab_hla.csv')
    hydrate(filetool.path_spreadsheet(valueset_csv), 'irae__lab_hla')

