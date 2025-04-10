import unittest

def powerset(iterable):
    s = list(iterable)
    n = len(s)
    return [[s[j] for j in range(n) if (i & (1 << j))] for i in range(2**n)]


import numpy as np
import pandas as pd
from itertools import chain, combinations


def powerset_matrix(iterable):
    elements = sorted(iterable)  # Sort to ensure consistent order
    n = len(elements)

    # Generate powerset
    subsets = list(chain.from_iterable(combinations(elements, r) for r in range(n + 1)))

    # Create matrix with binary representation
    matrix = np.zeros((2 ** n, n), dtype=int)

    for i, subset in enumerate(subsets):
        for element in subset:
            matrix[i, elements.index(element)] = 1

    # Convert to DataFrame for better visualization
    df = pd.DataFrame(matrix, index=[str(s) for s in subsets], columns=elements)

    return df

#########################

class TestPowerset(unittest.TestCase):
    def test(self):
        # Example usage
        print(powerset({1, 2, 3}))

        # Example usage
        elements = {'a', 'b', 'c'}
        df = powerset_matrix(elements)

        # Print the matrix
        print(df)
