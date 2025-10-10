import unittest
import pandas as pd
from cumulus_library_kidney_transplant import filetool, fhir2sql
from cumulus_library_kidney_transplant.spreadsheet.document import (
    service,
    domain,
    kind,
    role
)

def load_df() -> pd.DataFrame:
    return pd.read_csv(filetool.path_spreadsheet('document/DocumentOntology.csv'))

def unique(part_type_name:str) -> list:
    df = load_df()
    mask = df["PartTypeName"] == part_type_name
    return df.loc[mask, "PartName"].unique()

def term_frequency(part_type_name:str):
    df = load_df()
    mask = df["PartTypeName"] == part_type_name
    return df.loc[mask, "PartName"].value_counts()

def print_tf(part_type_name:str)-> None:
    for part_name, tf in term_frequency(part_type_name).items():
        print(f"'{part_name}',", '\t#', tf)


class TestDocumentOntology(unittest.TestCase):
    def setUp(self):
        self.ont = pd.read_csv(filetool.path_spreadsheet('document/DocumentOntology.csv'))

    def ignore_test_print(self):
        # print_tf('Document.SubjectMatterDomain')
        # print_tf('Document.TypeOfService')
        # print_tf('Document.Setting')
        # print_tf('Document.Kind')
        # print_tf('Document.Role')
        pass

    def ignore_test_write_valueset_loinc(self):
        entries = list()
        for row in pd.read_csv(filetool.path_spreadsheet('document/Loinc.csv')).itertuples(index=False):
            entries.append({'system':'http://loinc.org',
                            'code': row.LOINC_NUM,
                            'display': row.LONG_COMMON_NAME})
        valueset_csv = pd.DataFrame.from_records(entries)
        valueset_csv.to_csv(filetool.path_spreadsheet('document/Loinc_valueset.csv'), index=False)
        # fhir2sql.csv2view(filetool.path_spreadsheet('document/Loinc_valueset.csv'),'loinc_valueset')

    def test_document_ontology(self):
        df = pd.read_csv(filetool.path_spreadsheet('document/Loinc_valueset.csv'))
        df = df.drop_duplicates(subset="code", keep="first")
        lookup = df.set_index("code")["display"].to_dict()
        matches = dict()

        for row in self.ont.itertuples(index=False):
            name = row.PartName
            code = row.LoincNumber
            display = None
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
            output.append({'system':'http://loinc.org',
                           'code':code,
                           'display':display})

        df_filtered = pd.DataFrame(output, columns=['system', 'code', 'display'])
        df_filtered.to_csv(filetool.path_spreadsheet('document/filtered.csv'), index=False)




