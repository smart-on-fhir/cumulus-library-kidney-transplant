import json
import unittest
from enum import Enum
import pandas as pd
import numpy as np
from math import ceil
from scipy.stats import norm


# scale invariant
# NUM_SAMPLES chosen to make it easy to pick INTEGER
NUM_SAMPLES = 100 * 1000

class KappaEnum(Enum):
    no = range(0,10)
    slight = range(10, 21)
    fair = range(21, 41)
    moderate = range(41, 61)
    substantial = range(61, 81)
    near_perfect = range(81, 100)
    perfect = range(100, 101)

def agree_no(k:float) -> bool:
    return int(k*100) in KappaEnum.no.value or (k <= 0)

def agree_slight(k:float) -> bool:
    return int(k*100) in KappaEnum.slight.value

def agree_fair(k:float) -> bool:
    return int(k*100) in KappaEnum.fair.value

def agree_moderate(k:float) -> bool:
    return int(k*100) in KappaEnum.moderate.value

def agree_subtantial(k:float) -> bool:
    return int(k*100) in KappaEnum.substantial.value

def agree_near_perfect(k:float) -> bool:
    return int(k*100) in KappaEnum.near_perfect.value

def agree_perfect(k:float) -> bool:
    return int(k*100) in KappaEnum.perfect.value

def agree_interpret(k:float) -> KappaEnum | None:
    if agree_no(k):
        return KappaEnum.no
    if agree_slight(k):
        return KappaEnum.slight
    if agree_fair(k):
        return KappaEnum.fair
    if agree_moderate(k):
        return KappaEnum.moderate
    if agree_subtantial(k):
        return KappaEnum.substantial
    if agree_near_perfect(k):
        return KappaEnum.near_perfect
    if agree_perfect(k):
        return KappaEnum.perfect
    return None

def confusion_matrix(f1_score=0.95, prevalence=0.5, n=NUM_SAMPLES) -> dict:
    return {'balanced': confusion_matrix_balanced(f1_score, prevalence, n),
            'precision': confusion_matrix_max_precision(f1_score, prevalence, n),
            'recall': confusion_matrix_max_recall(f1_score, prevalence, n)}

def confusion_matrix_balanced(f1_score=0.95, prevalence=0.5, n=NUM_SAMPLES) -> dict:
    """
    Balanced: Precision = Recall = F1
    """
    positives = int(n * prevalence)
    negatives = n - positives

    tp = int(round(f1_score * positives))
    fn = positives - tp
    fp = int(round(tp * (1 - f1_score) / f1_score))
    tn = negatives - fp

    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn}


def confusion_matrix_max_precision(f1_score=0.95, prevalence=0.5, n=NUM_SAMPLES) -> dict:
    """
    Max precision: Precision = 1.0, solve Recall from F1
    """
    positives = int(n * prevalence)
    negatives = n - positives

    recall = f1_score / (2 - f1_score)  # solved above
    tp = int(round(recall * positives))
    fn = positives - tp
    fp = 0  # precision = 1 means no false positives
    tn = negatives - fp

    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn}


def confusion_matrix_max_recall(f1_score=0.95, prevalence=0.5, n=NUM_SAMPLES):
    """
    Max recall: Recall = 1.0, solve Precision from F1
    """
    positives = int(n * prevalence)
    negatives = n - positives

    precision = f1_score / (2 - f1_score)  # solved above
    tp = positives  # recall = 1 means all positives captured
    fn = 0
    # Solve FP from precision = TP / (TP+FP)
    fp = int(round(tp * (1 - precision) / precision))
    tn = negatives - fp

    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn}

def calc_confusion_matrix_dict(matrix:dict) -> dict:
    return calc_confusion_matrix(
        a=matrix["TP"],
        b=matrix["FP"],
        c=matrix["FN"],
        d=matrix["TN"])

def calc_confusion_matrix(a:int, b:int, c:int, d:int) -> dict:
    """
    Calculate Cohen's Kappa, F1, PPV, Recall, and Precision
    from a 2x2 confusion matrix.

    Parameters:
        a (int): True Positives (TP)
        b (int): False Positives (FP)
        c (int): False Negatives (FN)
        d (int): True Negatives (TN)

    :return dict of calculated Cohen's Kappa, F1, PPV, Recall, and Precision
    """
    # Totals
    n = a + b + c + d
    if n == 0:
        raise ValueError("Confusion matrix is empty.")

    # Observed agreement
    po = (a + d) / n

    # Expected agreement
    p_yes_true = (a + c) / n
    p_yes_pred = (a + b) / n
    p_no_true = (b + d) / n
    p_no_pred = (c + d) / n
    pe = p_yes_true * p_yes_pred + p_no_true * p_no_pred

    # Cohen's kappa
    kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 0.0

    # Precision (PPV)
    precision = a / (a + b) if (a + b) > 0 else 0.0

    # Recall (Sensitivity)
    recall = a / (a + c) if (a + c) > 0 else 0.0

    # F1-score
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) > 0 else 0.0)

    return {
        "kappa_k": kappa,
        "kappa_enum": str(agree_interpret(kappa)),
        "f1": f1,
        "precision": precision,
        "ppv": precision,  # synonym
        "recall": recall
    }

def json_to_csv(filename_json:str):
    with open(filename_json, "r") as f:
        content = json.load(f)
    df = pd.json_normalize(content)
    df.columns = df.columns.str.replace(r"\.", "_", regex=True)
    return df.to_csv(f'{filename_json}.csv', index=False)

#####################################################################################################################
"""
Minimal sample size calculators using numpy/scipy.
"""
#####################################################################################################################

def n_single_prevalence(p: float, margin_error: float, alpha: float = 0.05, fpc_N: int | None = None, deff: float = 1.0) -> float:
    z = norm.ppf(1 - alpha/2.0)
    n = (z**2) * p * (1 - p) / (margin_error**2)
    n *= deff
    if fpc_N is not None:
        n = (n * fpc_N) / (n + fpc_N - 1)
    return n

def n_two_proportions(p1: float, p2: float, alpha: float = 0.05, power: float = 0.80, ratio: float = 1.0, deff: float = 1.0) -> tuple[float, float]:
    z_alpha = norm.ppf(1 - alpha/2.0)
    z_beta  = norm.ppf(power)
    k = ratio
    p_bar = (p1 + k*p2) / (1 + k)
    q_bar = 1 - p_bar
    se0 = np.sqrt((1 + 1/k) * p_bar * q_bar)
    se1 = np.sqrt(p1*(1-p1) + (p2*(1-p2))/k)
    delta = abs(p1 - p2)
    n1 = ((z_alpha*se0 + z_beta*se1) / delta) ** 2
    n1 *= deff
    n2 = k * n1
    return n1, n2

def ceil_int(x: float) -> int:
    return ceil(x)


class TestSampleSize(unittest.TestCase):

    def ignpre__test_prevalence(self):
        # Example usage:
        conf = calc_confusion_matrix(a=48, b=2, c=2, d=48)
        for k, v in conf.items():
            print(f"{k}: {v:.3f}")

        # Example usage:
        conf = confusion_matrix(f1_score=0.95, n=100000, prevalence=0.5)
        print(conf)

    def ignore_test_agree_kappa_not_null(self):
        for k_int in range(0, 101):
            k_float = (k_int / 100)
            k_agree = agree_interpret(k_float)
            print('k*100', '\t', str(k_float), '\t', k_agree)
            self.assertIsNotNone(k_agree)

    def test_agree_kappa_ranges(self):
        self.assertEqual(KappaEnum.no, agree_interpret(k=0/100))
        self.assertEqual(KappaEnum.no, agree_interpret(k=1/100))
        self.assertEqual(KappaEnum.no, agree_interpret(k=9/100))

        self.assertEqual(KappaEnum.slight, agree_interpret(k=10 / 100))
        self.assertEqual(KappaEnum.slight, agree_interpret(k=20 / 100))

        self.assertEqual(KappaEnum.fair, agree_interpret(k=21 / 100))
        self.assertEqual(KappaEnum.fair, agree_interpret(k=40 / 100))

        self.assertEqual(KappaEnum.moderate, agree_interpret(k=41 / 100))
        self.assertEqual(KappaEnum.moderate, agree_interpret(k=60 / 100))

        self.assertEqual(KappaEnum.substantial, agree_interpret(k=61 / 100))
        self.assertEqual(KappaEnum.substantial, agree_interpret(k=80 / 100))

        self.assertEqual(KappaEnum.near_perfect, agree_interpret(k=81 / 100))
        self.assertEqual(KappaEnum.near_perfect, agree_interpret(k=99 / 100))

        self.assertEqual(KappaEnum.perfect, agree_interpret(k=100 / 100))

    def test_near_perfect(self):
        output = list()
        for f1_score in [0.80, 0.85, 0.9, 0.95]:
            for prevalence in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:

                balanced = confusion_matrix_balanced(f1_score, prevalence=prevalence, n=NUM_SAMPLES)
                max_precision  = confusion_matrix_max_precision(f1_score, prevalence=prevalence, n=NUM_SAMPLES)
                max_recall = confusion_matrix_max_recall(f1_score, prevalence=prevalence, n=NUM_SAMPLES)

                output.append({
                    'f1':f1_score,
                    'prevalence':prevalence,
                    'balanced': {'matrix': balanced, 'calc': calc_confusion_matrix_dict(balanced)},
                    'precision': {'matrix': max_precision, 'calc': calc_confusion_matrix_dict(max_precision)},
                    'recall': {'matrix': max_recall, 'calc': calc_confusion_matrix_dict(max_recall)},
                })
        print(output)
        with open('sample_size.json', 'w') as f:
            json.dump(output, f, indent=4)

        json_to_csv('sample_size.json')

if __name__ == '__main__':
    unittest.main()
