from typing import List
from irae import common, counts
from irae.fhir2sql import path_athena
from irae.criteria import age_at_visit, gender, race, encounter_class, study_period, utilization
from irae.variable import vsac_variables, custom_variables
from irae import study_population, cohorts, casedef

def make_study() -> List[str]:
    criteria_sql = [
        study_period.include('2016-01-01', '2025-01-01', include_history=True),
        utilization.include(enc_min=3, enc_max=1000, days_min=90),
        age_at_visit.include(),
        encounter_class.include(),
        gender.include(female=True, male=True, other=True, unknown=False),
        race.include()]

    studypop_sql = study_population.make()
    variables_sql = vsac_variables.make() + custom_variables.make()
    cohorts_sql = cohorts.make()
    casedef_sql = casedef.make()
    counts_sql = counts.make()

    manifest_list = criteria_sql + studypop_sql + variables_sql + cohorts_sql + casedef_sql + counts_sql

    write_manifest(manifest_list)

    return manifest_list

def write_manifest(file_list: list) -> str:
    manifest = list()
    for file in file_list:
        if 'irae/' in file:
            _, file = file.split('irae/')
        manifest.append(f"'{file}'")
    text = ',\n'.join(manifest)
    print(text)
    return common.write_text(text, path_athena('file_names.manifest.toml'))

def command_shell() -> str:
    # bch-aws-login while on VPN
    return "cumulus-library build -s ./ -t irae"


if __name__ == "__main__":
    make_study()
