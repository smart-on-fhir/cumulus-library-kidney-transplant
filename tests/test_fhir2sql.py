import unittest
import csv
from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import guard, fhir2sql, filetool

def csv_headers(file_csv: Path|str) -> List[str]:
    with file_csv.open(newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        return next(reader)

def csv2view(file_csv:Path, view_name) -> str:
    """
    :param codelist: list of concepts
    :param view_name: like define_type
    :return: SQL command
    """
    header_list = csv_headers(file_csv)
    create = f"create or replace view {view_name} as select * from (values"
    footer = f") AS t ({','.join(header_list)}) ;"
    content = list()

    with open(file_csv) as f:
        for row in csv.DictReader(f, header_list):
            parsed = list()
            for col in header_list:
                value = row[col]
                if guard.is_bool(guard.as_bool(value)):
                    value = guard.as_bool(value)
                    parsed.append(str(value))
                else:
                    if value is None or len(str(value)) == 0:
                        parsed.append('')
                    else:
                        value = fhir2sql.sql_escape(value)
                        parsed.append(f"'{value}'")

            parsed = ','.join(parsed)
            content.append(f"\n({parsed})")
        return create + '\n' + ','.join(content) + '\n' + footer

class TestFHIR2sql(unittest.TestCase):

    def test_name_simple(self):
        expected = 'casedef_timeline'
        actual = fhir2sql.name_simple('irae__cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = 'dx_diabetes'
        actual = fhir2sql.name_simple('irae__dx_diabetes')
        self.assertEqual(expected, actual)

    def test_prefix(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = fhir2sql.name_prefix('cohort_casedef_timeline')
        self.assertEqual(expected, actual)

        expected = ['irae__cohort_casedef_timeline', 'irae__dx_diabetes']
        actual = fhir2sql.name_prefix(['cohort_casedef_timeline', 'dx_diabetes'])
        self.assertSetEqual(set(expected), set(actual))

    def test_name_join(self):
        expected = 'irae__cohort_casedef_timeline'
        actual = fhir2sql.name_join('cohort', 'casedef_timeline')
        self.assertEqual(expected, actual)

    def test_headers(self):
        header_list = ['system','code','display',
                       'likely','preop','transplant',
                       'rejection','failure','outcome',
                       'lab','imaging','count_sum']

        file_csv = fhir2sql.filetool.path_spreadsheet('casedef_custom.csv')
        actual = csv_headers(file_csv)
        self.assertEqual(header_list, actual)

    def test_criteria2view(self):
        file_csv = fhir2sql.filetool.path_spreadsheet('casedef_custom.csv')

        _sql = csv2view(file_csv, 'casedef_custom')
        print(_sql)




if __name__ == '__main__':
    unittest.main()
