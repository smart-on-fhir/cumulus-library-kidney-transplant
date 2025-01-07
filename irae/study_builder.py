from typing import List
from pathlib import Path
from irae import manifest, resources
from irae import criteria, study_population, cohorts, casedef
from irae import counts
from irae.variable import vsac_variables, vsac_markdown
from irae.variable import custom_variables

def make_study() -> List[Path]:
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

    manifest.write_manifest(manifest_list)
    return manifest_list


if __name__ == "__main__":
    make_study()

    content = vsac_markdown.make()
    resources.path_home()
