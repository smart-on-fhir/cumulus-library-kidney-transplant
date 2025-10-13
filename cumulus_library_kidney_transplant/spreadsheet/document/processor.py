import pandas as pd
from cumulus_library_kidney_transplant import filetool, fhir2sql
from cumulus_library_kidney_transplant.spreadsheet.document import (
    service,
    domain,
    kind,
    role,
    study_keywords
)

ONTOLOGY_CSV = filetool.path_spreadsheet('document/DocumentOntology.csv')
LOINC_CSV = filetool.path_spreadsheet('document/Loinc.csv')
LOINC_VALUESET_CSV = filetool.path_spreadsheet('document/Loinc_valueset.csv')

def unique(part_type_name:str) -> list:
    df = pd.read_csv(ONTOLOGY_CSV)
    mask = df["PartTypeName"] == part_type_name
    return df.loc[mask, "PartName"].unique()

def term_frequency(part_type_name:str):
    df = pd.read_csv(ONTOLOGY_CSV)
    mask = df["PartTypeName"] == part_type_name
    return df.loc[mask, "PartName"].value_counts()

def print_tf(part_type_name:str)-> None:
    for part_name, tf in term_frequency(part_type_name).items():
        print(f"'{part_name}',", '\t#', tf)

def loinc2valueset():
    entries = list()
    for row in pd.read_csv(LOINC_CSV).itertuples(index=False):
        entries.append({'system': 'http://loinc.org',
                        'code': row.LOINC_NUM,
                        'display': row.LONG_COMMON_NAME})
    entries = sorted(entries, key=lambda x: x['code'])
    valueset_csv = pd.DataFrame.from_records(entries)
    valueset_csv.to_csv(LOINC_VALUESET_CSV, index=False)
    # fhir2sql.csv2view(filetool.path_spreadsheet('document/Loinc_valueset.csv'),'loinc_valueset')

def process_all():
    process_loinc_part('Document.Kind')
    process_loinc_part('Document.TypeOfService')
    process_loinc_part('Document.SubjectMatterDomain')
    process_loinc_part('Document.Role')

def process_loinc_part(loinc_part_type:str) -> None:
    ontology_df = pd.read_csv(ONTOLOGY_CSV)
    loinc_df = pd.read_csv(LOINC_VALUESET_CSV)
    loinc_df = loinc_df.drop_duplicates(subset="code", keep="first")
    lookup = loinc_df.set_index("code")["display"].to_dict()
    matches = dict()

    for row in ontology_df.itertuples(index=False):
        name = row.PartName
        code = row.LoincNumber
        display = None
        if loinc_part_type == row.PartTypeName:
            if row.PartTypeName == 'Document.Kind':
                if name in kind.INCLUDE:
                    display = lookup[code]
            elif row.PartTypeName == 'Document.TypeOfService':
                if name in service.INCLUDE:
                    display = lookup[code]
            elif row.PartTypeName == 'Document.SubjectMatterDomain':
                if name in domain.INCLUDE:
                    display = lookup[code]
            elif row.PartTypeName == 'Document.Role':
                if name in role.INCLUDE:
                    display = lookup[code]
            if display and code not in matches.keys():
                matches[code] = display

    # convert to list output CSV
    output = list()
    for code, display in matches.items():
        matches = study_keywords.match_list(display)
        matches = '|'.join(matches)
        output.append({'system':'http://loinc.org',
                       'code':code,
                       'display':display,
                       'keyword':matches})

    loinc_part_alias = loinc_part_type.replace('Document.', '').lower()

    output = sorted(output, key=lambda x: x['code'])
    output_csv = f"document/doc_{loinc_part_alias}.csv"
    view_name = f"irae__doc_ontology_{loinc_part_alias}"

    df_filtered = pd.DataFrame(output, columns=['system', 'code', 'display', 'keyword'])
    df_filtered.to_csv(filetool.path_spreadsheet(output_csv), index=False)
    fhir2sql.csv2view(filetool.path_spreadsheet(output_csv), view_name)


if __name__ == "__main__":
    loinc2valueset()
    process_all()

