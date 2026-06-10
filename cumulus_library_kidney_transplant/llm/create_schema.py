import os
import json
from pathlib import Path
from cumulus_library_ibd_cds.llm.models.mayo_score import IbdMayoScoreAnnotation
from cumulus_library_ibd_cds.llm.models.uceis import IbdUCEISAnnotation
from cumulus_library_ibd_cds.llm.models.sescd import IbdSESCDAnnotation
from cumulus_library_ibd_cds.llm.models.endoscopy import IbdEndoscopyAnnotation
from cumulus_library_ibd_cds.llm.models.stooling import IbdStoolingAnnotation
from cumulus_library_ibd_cds.llm.models.pucai import IbdPUCAIAnnotation
from cumulus_library_ibd_cds.llm.models.pcdai import IbdPCDAIAnnotation
from cumulus_library_ibd_cds.llm.models.eim import IbdEIMAnnotation

from cumulus_library_ibd_cds.llm.models.diagnosis import IbdDiagnosisAnnotation
from cumulus_library_ibd_cds.llm.models.treatment import IbdTreatmentAnnotations
from cumulus_library_ibd_cds.llm.models.surgery import IbdSurgeryAnnotation
from cumulus_library_ibd_cds.llm.models.paris_classification import IbdParisClassificationAnnotation
from cumulus_library_ibd_cds.llm.models.genetic_findings import IbdGeneticFindingsAnnotation
from cumulus_library_ibd_cds.llm.models.lab_inflammation import IbdInflammationLabAnnotation
from cumulus_library_ibd_cds.llm.models.lab_cytokine import IbdCytokineLabAnnotation
from cumulus_library_ibd_cds.llm.models.lab_panel_iron import IbdIronLabPanelAnnotation
from cumulus_library_ibd_cds.llm.models.lab_panel_nutrients import IbdNutrientsLabPanelAnnotation
from cumulus_library_ibd_cds.llm.models.lab_panel_cbc import IbdCBCLabPanelAnnotation
from cumulus_library_ibd_cds.llm.models.lab_panel_cmp import IbdCMPLabPanelAnnotation
from cumulus_library_ibd_cds.llm.models.document_type import DocumentTypeAnnotation
from cumulus_library_ibd_cds.llm.models.document_topic import TopicRelevanceAnnotation

BASE_DIR = Path(os.path.dirname(__file__))

def create(annotation, filename:str) -> Path:
    """
    Create an IBD schema using BaseModel.model_json_schema()

    :param annotation: Annotation class of type BaseModel
    :param filename: name of the json file to write to
    :return: Path to JSON
    """
    file_path = BASE_DIR / 'schemas' / filename
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(annotation.model_json_schema(), f, indent=2)
    return file_path

def create_ibd_llm_study_variables() -> list[Path]:
    """
    Target for "ibd_llm_study_variables"
    :return: Paths to schema JSON files
    """
    return [
        create(IbdDiagnosisAnnotation, 'ibd-diagnosis-annotation.json'),
        create(IbdTreatmentAnnotations, 'ibd-treatment-annotation.json'),
        create(IbdSurgeryAnnotation, 'ibd-surgery-annotation.json'),
        create(IbdParisClassificationAnnotation, 'ibd-paris-classification-annotation.json'),
        create(IbdGeneticFindingsAnnotation, 'ibd-genetic-findings-annotation.json')
    ]

def create_endoscopic_endpoints() -> list[Path]:
    """
    :return:
    """
    return [
        create(IbdMayoScoreAnnotation, 'ibd-mayo-score-annotation.json'),
        create(IbdUCEISAnnotation, 'ibd-uceis-annotation.json'),
        create(IbdSESCDAnnotation, 'ibd-sescd-annotation.json'),
        create(IbdEndoscopyAnnotation, 'ibd-endoscopy-annotation.json'),
        create(IbdStoolingAnnotation, 'ibd-stooling-annotation.json')
    ]

def create_activity_index() -> list[Path]:
    return [
        create(IbdPUCAIAnnotation, 'ibd-pucai-annotation.json'),
        create(IbdPCDAIAnnotation, 'ibd-pcdai-annotation.json'),
        create(IbdEIMAnnotation, 'ibd-eim-annotation.json')
    ]

def create_labs() -> list[Path]:
    return [
        create(IbdInflammationLabAnnotation, 'ibd-inflammation-lab-annotation.json'),
        create(IbdCytokineLabAnnotation, 'ibd-cytokine-lab-annotation.json'),
        create(IbdIronLabPanelAnnotation, 'ibd-iron-lab-panel-annotation.json'),
        create(IbdNutrientsLabPanelAnnotation, 'ibd-nutrients-lab-panel-annotation.json'),
        create(IbdCBCLabPanelAnnotation, 'ibd-cbc-lab-panel-annotation.json'),
        create(IbdCMPLabPanelAnnotation, 'ibd-cmp-lab-panel-annotation.json')
    ]

def create_document_relevance() -> list[Path]:
    return [create(DocumentTypeAnnotation, 'ibd-document-type-annotation.json'),
            create(TopicRelevanceAnnotation, 'ibd-topic-relevance-annotation.json')]

if __name__ == "__main__":
    print('creating JSON schemas for Annotation(BaseModel)...')
    print('create IBD study variables \n\t', '\n\t'.join([str(p) for p in create_ibd_llm_study_variables()]))
    print('create endoscopic severity \n\t', '\n\t'.join([str(p) for p in create_endoscopic_endpoints()]))
    print('create activity index(s) \n\t', '\n\t'.join([str(p) for p in create_activity_index()]))
    print('create labs \n\t', '\n\t'.join([str(p) for p in create_labs()]))
    print('create document relevance \n\t', '\n\t'.join([str(p) for p in create_document_relevance()]))
