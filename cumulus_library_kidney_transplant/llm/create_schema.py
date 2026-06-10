import os
import json
from pathlib import Path

from cumulus_library_kidney_transplant.llm.model import (
    KidneyTransplantDonorGroupAnnotation,
    ImmunosuppressiveMedicationsAnnotation,
    KidneyTransplantLongitudinalAnnotation,
    MultipleTransplantHistoryAnnotation,
)

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

if __name__ == "__main__":
    print('creating JSON schemas for Annotation(BaseModel)...')
    files_created = [
        create(KidneyTransplantDonorGroupAnnotation, 'irae_donor.json'),
        create(ImmunosuppressiveMedicationsAnnotation, 'irae_medications.json'),
        create(KidneyTransplantLongitudinalAnnotation, 'irae_outcomes.json'),
        create(MultipleTransplantHistoryAnnotation, 'irae_multiple_transplant_history.json'),
    ]
    print('created the following schemas \n\t', '\n\t'.join([str(p) for p in files_created]))
