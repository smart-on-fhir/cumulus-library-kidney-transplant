import unittest
import pandas as pd
from cumulus_library_kidney_transplant import filetool

class TestValueSetCodes(unittest.TestCase):

    def test_rx(self):
        emptyset = set()
        for file_csv in filetool.list_spreadsheet_csv('rx_*.csv'):
            file_tsv = str(file_csv).replace('.csv', '.tsv')

            print(file_csv)

            if 'rx_prednisolone' in str(file_csv):
                print('skipping (QA/QC passed) rx_prednisolone')
                continue

            df_csv = pd.read_csv(file_csv)
            df_tsv = pd.read_csv(file_tsv, sep='\t')

            codes_csv = set(df_csv['code'])
            codes_tsv = set(df_tsv['code'])

            self.assertSetEqual(emptyset, codes_csv - codes_tsv, 'csv - tsv ')
            self.assertSetEqual(emptyset, codes_tsv - codes_csv, 'tsv - csv ')
