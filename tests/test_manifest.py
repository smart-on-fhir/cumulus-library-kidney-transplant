import unittest
from cumulus_library_kidney_transplant import manifest, filetool

class TestManifest(unittest.TestCase):

    def test_read(self):
        self.assertTrue('manifest.toml' in str(manifest.path_manifest()))

        self.assertTrue(manifest.read_manifest().get('file_config'),
                        msg='save_manifest.tom missing [file_config] section')

        keyval = manifest.read_manifest()
        print(keyval['file_config'])
        print(keyval.values())
