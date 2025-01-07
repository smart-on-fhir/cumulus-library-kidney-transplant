import unittest
from irae import manifest, resources

class TestManifest(unittest.TestCase):

    def test_read(self):
        keyval = manifest.read_manifest()
        print(keyval)

        print(resources.path_parent('manifest.toml'))
