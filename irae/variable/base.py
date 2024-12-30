from typing import List, Dict
from fhirclient.models.coding import Coding

class Vocab:
    RXNORM = 'http://www.nlm.nih.gov/research/umls/rxnorm'
    LOINC = 'http://loinc.org'
    ICD10CM = 'http://hl7.org/fhir/sid/icd-10'
    ICD10PCS = 'http://www.icd10data.com/icd10pcs'
    SNOMED = 'http://snomed.info/sct'
    CPT = 'http://www.ama-assn.org/go/cpt'
    HCPCS = 'http://www.nlm.nih.gov/research/umls/hcpcs'

#############################################################
# Base Variable Type
#
#############################################################
class Variable:
    alias: str = None
    concepts: List[Coding] = list()

    def concept_json(self) -> List[dict]:
        return [c.as_json() for c in self.concepts]

    def as_json(self) -> Dict[str, List]:
        return {self.alias: self.concept_json()}

#############################################################
# Simple variable denotes "presence", impliclity
# True = code present
# False = code absent
#############################################################
class BinaryClass(Variable):
    alias: str = None
    concepts: List[Coding] = list()

    def __init__(self, alias: str, concepts: List[Coding] = None):
        """
        :param alias: str name like "drug_immunosuppresive"
        :param values: List[Coding]
        """
        self.alias = alias
        self.concepts = concepts if concepts else list()


#############################################################
# Variable with multiple classes, examples
#
#  Asthma: severe, moderate, mild, None
#  Chronic Kidney Disease: Stage 1-5
#  Suicidality: ideation, self-harm, attempt
#  Blood pressure: HYPERtensive, HYPOtensive, Normal
#############################################################
class MultiClass(Variable):
    alias: str = None
    subtypes: Dict[str, BinaryClass] = dict()

    def __init__(self, alias: str):
        """
        :param alias: str name like "ckd_staging"
        """
        self.alias = alias

    def as_json(self) -> Dict[str, List]:
        out = dict()
        for subtype in self.subtypes:
            out[subtype] = list()
            for coding in self.subtypes[subtype].concepts:
                out[subtype].append(coding.as_json())
        return out
