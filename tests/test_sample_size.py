import unittest
from cumulus_library_kidney_transplant.accuracy import kappa, sample_size
from cumulus_library_kidney_transplant.accuracy.kappa import KappaEnum

class TestSampleSize(unittest.TestCase):

    def test_calc_confusion_matrix_perfect_balance(self):
        # Example usage:
        f1_score = 0.95; n = 100000; prevalence = 0.5
        tp = 48; fp = 2; fn = 2; tn = 48
        matrix = sample_size.calc_confusion_matrix(tp=tp, fp=fp, fn=fn, tn=tn)
        expected = 0.96
        self.assertEqual(matrix["f1"], expected)
        self.assertEqual(matrix["recall"], expected)
        self.assertEqual(matrix["ppv"], expected)
        self.assertEqual(matrix["specificity"], expected)
        self.assertTrue(matrix["kappa_k"] > 0.90)
        self.assertTrue(kappa.agree_near_perfect(matrix['kappa_k']))
        self.assertTrue(matrix['kappa_enum'], KappaEnum.near_perfect.name)


    def test_confusion_matrix_boundaries(self):
        matrix = sample_size.confusion_matrix(f1_score=0.95, n=100000, prevalence=0.5)

        # F1 harmonic balance (precision and recall)
        self.assertEqual(matrix['balanced']['TP'], matrix['balanced']['TN'])
        self.assertEqual(matrix['balanced']['FP'], matrix['balanced']['FN'])

        # optimized for precision (PPV)
        self.assertEqual(matrix['max_precision']['FP'], 0)
        self.assertTrue(matrix['max_precision']['TP'] < matrix['balanced']['TN'])

        # optimized for recall (sensitivity)
        self.assertEqual(matrix['max_recall']['FN'], 0)
        self.assertTrue(matrix['max_recall']['TP'] > matrix['balanced']['TN'])


    def test_agree_kappa_not_null(self):
        for k_int in range(0, 101):
            k_float = (k_int / 100)
            k_agree = kappa.agree_interpret(k_float)
            print('k*100', '\t', str(k_float), '\t', k_agree)
            self.assertIsNotNone(k_agree)

    def test_agree_kappa_ranges(self):
        self.assertEqual(KappaEnum.no, kappa.agree_interpret(k=0/100))
        self.assertEqual(KappaEnum.no, kappa.agree_interpret(k=1/100))
        self.assertEqual(KappaEnum.no, kappa.agree_interpret(k=9/100))

        self.assertEqual(KappaEnum.slight, kappa.agree_interpret(k=10 / 100))
        self.assertEqual(KappaEnum.slight, kappa.agree_interpret(k=20 / 100))

        self.assertEqual(KappaEnum.fair, kappa.agree_interpret(k=21 / 100))
        self.assertEqual(KappaEnum.fair, kappa.agree_interpret(k=40 / 100))

        self.assertEqual(KappaEnum.moderate, kappa.agree_interpret(k=41 / 100))
        self.assertEqual(KappaEnum.moderate, kappa.agree_interpret(k=60 / 100))

        self.assertEqual(KappaEnum.substantial, kappa.agree_interpret(k=61 / 100))
        self.assertEqual(KappaEnum.substantial, kappa.agree_interpret(k=80 / 100))

        self.assertEqual(KappaEnum.near_perfect, kappa.agree_interpret(k=81 / 100))
        self.assertEqual(KappaEnum.near_perfect, kappa.agree_interpret(k=99 / 100))

        self.assertEqual(KappaEnum.perfect, kappa.agree_interpret(k=100 / 100))