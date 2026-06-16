import unittest
from cumulus_library_kidney_transplant.tools.fhir_reference import Aspect
from cumulus_library_kidney_transplant.tools import study_variable

class TestVariableAspect(unittest.TestCase):

    def test_aspects(self):
        aspect_dict = study_variable.dict_aspects()

        # aspects
        self.assertTrue(Aspect.lab in aspect_dict)
        self.assertTrue(Aspect.rx in aspect_dict)

        # test keys
        self.assertTrue('lab_hla' in aspect_dict[Aspect.lab])
        self.assertTrue('rx_cni_tacrolimus' in aspect_dict[Aspect.rx])
