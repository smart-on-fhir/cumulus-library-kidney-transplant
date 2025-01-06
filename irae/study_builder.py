from typing import List
from irae import resources, counts
from irae import criteria, study_population, cohorts, casedef
from irae.variable import vsac_variables, custom_variables

def make_study() -> List[str]:
    """
    $cumulus-library build -s ./ -t irae

    :return: list of SQL files to execute in Athena.
    """
    criteria_sql = [
        criteria.study_period.include('2016-01-01', '2025-01-01', include_history=True),
        criteria.utilization.include(enc_min=3, enc_max=1000, days_min=90),
        criteria.age_at_visit.include(),
        criteria.encounter_class.include(),
        criteria.gender.include(female=True, male=True, other=True, unknown=False),
        criteria.race.include()]

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
    return resources.save_athena('file_names.manifest.toml', text)

def command_shell() -> str:
    # bch-aws-login while on VPN
    return "cumulus-library build -s ./ -t irae"


if __name__ == "__main__":
    make_study()
