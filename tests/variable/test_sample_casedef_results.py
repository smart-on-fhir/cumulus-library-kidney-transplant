import unittest

from cumulus_library_kidney_transplant.count import cube


class TestSampleCasedefResults(unittest.TestCase):

    def test_cube(self):
        from_table = 'irae__cohort_casedef_post_1000_results'
        create_enc = 'irae__count_encounter_casedef_post_1000_results'
        create_pat = 'irae__count_patient_casedef_post_1000_results'
        create_doc = 'irae__count_document_casedef_post_1000_results'
        cols_drug = ['ade']
        cols_visit = ['period_start_month', 'enc_class_display', 'age_at_visit', 'gender', 'race_display']
        cols_doc = ['doc_type_display', 'doc_type_system']
        cols = cols_drug + cols_visit + cols_doc
        output = cube.cube_doc(from_table, cols, create_doc)

        # output = [cube.cube_enc(from_table, cols, create_enc),
        #           cube.cube_pat(from_table, cols, create_pat)]
        # print(output)
