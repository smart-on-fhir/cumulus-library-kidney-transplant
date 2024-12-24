from typing import List
from irae import common, counts
from irae.fhir2sql import include, path_athena
from irae.criteria import age_at_visit, gender, race, document, study_period
from irae.criteria import encounter_class
from irae.variable import vsac_variables, custom_variables

def make_study() -> List[str]:
    criteria = [
        study_period.include('2016-01-01', '2025-01-01', False),
        age_at_visit.include(0, 120),
        encounter_class.include(),
        gender.include(female=True, male=True, other=True, unknown=False),
        race.include()]

    file_list = criteria + vsac_variables.make() + custom_variables.make() + counts.make()
    write_manifest(file_list)

    return file_list

def write_manifest(file_list: list) -> str:
    manifest = list()
    for file in file_list:
        _, target = file.split('irae/')
        manifest.append(f"'{target}'")
    return common.write_text(',\n'.join(manifest), path_athena('irae__manifest.txt'))

def command_shell() -> str:
    return "cumulus-library build -s ./ -t irae"


if __name__ == "__main__":
    make_study()
