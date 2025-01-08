import unittest
from irae.variable.aspect import Aspect, AspectMap, AspectKey
from irae.variable.aspect import Procedures, Variable, Valueset
from irae.variable.vsac_variables_defined import Diagnoses, Medications, Labs, Procedures
from irae.variable.vsac_variables_defined import get_aspect_map

class TestAspect(unittest.TestCase):

    def get_proc_variable_list(self):
        return Procedures([
            Variable('Nephrectomy', {
                'sct': '2.16.840.1.113762.1.4.1248.200',
                'icd10pcs': '2.16.840.1.113762.1.4.1248.4'}),
            Variable('Dialysis', {
                'services': '2.16.840.1.113883.3.464.1003.109.12.1013'})])

    def get_proc_variable_dict(self):
        return Procedures({
            'Nephrectomy': {
                'sct': '2.16.840.1.113762.1.4.1248.200',
                'icd10pcs': '2.16.840.1.113762.1.4.1248.4'},
            'Dialysis': {
                'services': '2.16.840.1.113883.3.464.1003.109.12.1013'}})

    def test_proc_dict_vs_list(self):
        expected = self.get_proc_variable_list().as_json()
        actual = self.get_proc_variable_dict().as_json()
        self.assertEqual(expected, actual)

    def test_aspect_map_as_json(self):
        aspect_map = get_aspect_map()
        aspect_json = aspect_map.as_json()

        self.assertEqual(4, len(aspect_json.keys()))
        self.assertTrue(AspectKey.dx.name in aspect_json.keys())
        self.assertTrue(AspectKey.rx.name in aspect_json.keys())
        self.assertTrue(AspectKey.lab.name in aspect_json.keys())
        self.assertTrue(AspectKey.proc.name in aspect_json.keys())

        self.assertTrue(len(aspect_map.diagnosis.variable_list) > 1)
        self.assertTrue(len(aspect_map.medications.variable_list) > 1)
        self.assertTrue(len(aspect_map.labs.variable_list) > 1)
        self.assertTrue(len(aspect_map.procedures.variable_list) > 1)
