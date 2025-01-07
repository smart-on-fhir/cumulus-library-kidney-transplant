import unittest
from irae import manifest, resources

class TestManifest(unittest.TestCase):

    def test_read(self):
        keyval = manifest.read_manifest()
        print(keyval['file_config'])
        print(keyval.values())


