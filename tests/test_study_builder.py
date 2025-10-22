import unittest
from cumulus_library_kidney_transplant import study_builder, manifest

# This test is currently failing, and should mock the API call, since it fails
# randomly due to intermittent unavailability at the source.
# It also creates files in the project root and should be pointed at a tmp dir.

#class TestStudyBuilder(unittest.TestCase):

    # def test_issue_26(self):
    #     """
    #     each make_study() run causes churn in the manifest.toml
    #     https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/26
    #     :return:
    #     """
    #     backup_path = manifest.backup_manifest()
    #     study_builder.make_study()
    #     saved_dict = manifest.read_manifest()
    #     backup_dict = manifest.read_manifest(backup_path)

    #     self.assertEqual(saved_dict.keys(), backup_dict.keys())

    #     self.assertEqual(saved_dict['export_config']['count_list'],
    #                      backup_dict['export_config']['count_list'])

    #     self.assertEqual(saved_dict['file_config']['file_names'],
    #                      backup_dict['file_config']['file_names'])

    #     self.assertDictEqual(backup_dict, saved_dict)
    #     backup_path.unlink()