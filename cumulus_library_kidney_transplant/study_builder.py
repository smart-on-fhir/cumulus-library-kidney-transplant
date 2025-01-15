from typing import List
from pathlib import Path
from cumulus_library_kidney_transplant import (
    manifest,
    filetool,
    criteria,
    study_population,
    cohorts,
    casedef)
from cumulus_library_kidney_transplant.count import cube, cube_custom
from cumulus_library_kidney_transplant.criteria.race import Race
from cumulus_library_kidney_transplant.criteria.encounter_class import EncounterClass
from cumulus_library_kidney_transplant.variable import (
    vsac_variables,
    vsac_markdown,
    custom_variables)

###############################################################################
#
# Config(...)
#
###############################################################################

class StudyBuilderConfig:
    period_start: str = '2016-01-01'
    period_end: str = '2025-02-01'
    include_history: bool = True
    enc_class_list: List[EncounterClass] | List[str] = None
    enc_min: int = 3
    enc_max: int = 1000
    days_min: int = 90
    days_max: int = 36500
    age_min: int = 0
    age_max: int = 120
    gender_female: bool = True
    gender_male: bool = True
    gender_other: bool = True
    gender_unknown: bool = True
    race_list: List[Race] | List[str] = None

    def __init__(self, form: dict = None):
        """
        :param form: TODO refactor should use a parser class not DIY methods
        """
        if not form:
            form = dict()
        self.period_start = form.get('period_start', '2016-01-01')
        self.period_end = form.get('period_end', '2025-02-01')
        self.include_history = bool(form.get('include_history', True))
        self.enc_class_list = form.get('enc_class_list', None)
        self.enc_min = int(form.get('enc_min', 3))
        self.enc_max = int(form.get('enc_max', 1000))
        self.days_min = int(form.get('days_min', 90))
        self.days_max = int(form.get('days_max', 365000))
        self.age_min = int(form.get('age_min', 0))
        self.age_max = int(form.get('age_max', 120))
        self.gender_female = bool(form.get('gender_female', True))
        self.gender_male = bool(form.get('gender_male', True))
        self.gender_other = bool(form.get('gender_other', True))
        self.gender_unknown = bool(form.get('gender_unknown', True))
        self.race_list = form.get('race_list', None)

    def as_json(self) -> dict:
        return self.__dict__

    @staticmethod
    def read_config(from_path: str | Path = None):
        if not from_path:
            from_path = filetool.path_home('StudyBuilderConfig.json')
        return filetool.read_json(from_path)

    @staticmethod
    def make_config(from_path: str | Path = None):
        return StudyBuilderConfig(StudyBuilderConfig.read_config(from_path))


###############################################################################
#
# Make
#
###############################################################################

def make_study(study: StudyBuilderConfig) -> Path:
    """
    $cumulus-library build -s ./ -t irae

    :return: list of SQL files to execute in Athena.
    """
    criteria_sql = [
        criteria.study_period.include(
            period_start=study.period_start,
            period_end=study.period_end,
            include_history=study.include_history
        ),
        criteria.utilization.include(
            enc_min=study.enc_min,
            enc_max=study.enc_max,
            days_min=study.days_min,
            days_max=study.days_max
        ),
        criteria.age_at_visit.include(
            age_min=study.age_min,
            age_max=study.age_max
        ),
        criteria.encounter_class.include(
            enc_class_list=study.enc_class_list
        ),
        criteria.gender.include(
            female=study.gender_female,
            male=study.gender_male,
            other=study.gender_other,
            unknown=study.gender_unknown
        ),
        criteria.race.include(
            race_list=study.race_list)]

    studypop_sql = study_population.make()
    variables_sql = vsac_variables.make() + custom_variables.make()
    cohorts_sql = cohorts.make()
    casedef_sql = casedef.make()
    counts_sql = cube.make() + cube_custom.make()

    vsac_markdown.make()
    print('README.md')

    return manifest.write_manifest(
        criteria_sql + studypop_sql + variables_sql + cohorts_sql + casedef_sql + counts_sql)


if __name__ == "__main__":
    study = StudyBuilderConfig.make_config()

    make_study(study)
