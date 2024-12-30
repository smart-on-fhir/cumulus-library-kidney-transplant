import os
from typing import List
from enum import Enum
from fhirclient.models.coding import Coding
from irae import fhir2sql, common

def include(enc_min=0, enc_max=1000) -> str:
    view = 'irae__include_cnt_encounter'
    cols = ['enc_min', 'enc_max']
    values = [str(enc_min), str(enc_max)]
    return fhir2sql.values2view(view, cols, values)
