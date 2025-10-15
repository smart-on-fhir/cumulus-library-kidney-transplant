from pathlib import Path
import shutil
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
    valueset_col = set(list(valueset_df.columns)).intersection({'code', 'LOINC_NUM'}).pop()
    valueset_codes = set(valueset_df[valueset_col].dropna().unique())
    loinc_codes = set(loinc_df['code'].dropna().unique())

    print(valueset_csv)
    print(len(valueset_codes), ' #valueset')
    print(len(loinc_codes), ' #loinc (official)')
    print(len(valueset_codes & loinc_codes), ' #intersection')
    print(len(loinc_codes - valueset_codes), ' #difference loinc')
    print(len(valueset_codes - loinc_codes), ' #difference valueset')

    if valueset_codes - loinc_codes:
        raise Exception('missing ', valueset_codes - loinc_codes)

    backup_csv = str(valueset_csv) + '.backup.csv'
    temp_csv = str(valueset_csv) + '.hydrate.csv'

    shutil.copy(valueset_csv, backup_csv)

    filtered = loinc_df[loinc_df['code'].isin(valueset_codes)].copy()
    filtered.to_csv(filetool.path_spreadsheet(temp_csv), index=False)
    fhir2sql.csv2view(Path(temp_csv), view_name)



