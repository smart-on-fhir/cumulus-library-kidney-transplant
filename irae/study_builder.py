from typing import List
from irae import common
from irae.fhir2sql import include, path_athena
from irae.criteria import age_at_visit, gender, race, document, study_period
from irae.criteria.encounter_class import EncounterClass
from irae.variable import vsac_variables, custom_variables

def make_study() -> List[str]:
    criteria_sql = [
        make_study_period(),
        make_age_at_visit(),
        make_gender(),
        make_race(),
        make_encounter(),
        make_document_type(),
        make_document_facility(),
        make_document_practice(),
    ]

    file_list = criteria_sql + vsac_variables.make() + custom_variables.make()
    write_manifest(file_list)

    return file_list

def write_manifest(file_list: list) -> str:
    manifest = list()
    for file in file_list:
        _, target = file.split('irae/')
        manifest.append(f"'{target}'")
    return common.write_text(',\n'.join(manifest), path_athena('irae__manifest.txt'))


def make_study_period() -> str:
    return study_period.include(
        period_start='2016-01-01',
        period_end='2025-01-01',
        include_history=False)

def make_age_at_visit(age_min=0, age_max=120) -> str:
    return age_at_visit.include(age_min, age_max)

def make_gender() -> str:
    codes = gender.sex2codelist(female=True, male=True, other=True, unknown=False)
    return include(codes, 'gender')

def make_race() -> str:
    codes = common.as_coding_list(list(race.Race))
    return include(codes, 'race')

def make_encounter() -> str:
    codes = common.as_coding_list(list(EncounterClass))
    return include(codes, 'encounter_class')

def make_document_type() -> str:
    codes = document.get_valueset_doctype()
    return include(codes, 'document_type')

def make_document_facility() -> str:
    codes = document.get_valueset_facility()
    return include(codes, 'document_facility')

def make_document_practice() -> str:
    codes = document.get_valueset_practice()
    return include(codes, 'document_practice')

def command_shell() -> str:
    return "cumulus-library build -s ./ -t irae"


if __name__ == "__main__":
    make_study()
