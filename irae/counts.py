from typing import List
from irae.fhir2sql import PREFIX, save_athena_sql
from cumulus_library.builders.counts import CountsBuilder

def name_cohort(tablename: str) -> str:
    return f'{PREFIX}__cohort_{tablename}'

def name_cube(tablename: str) -> str:
    return f'{PREFIX}__cube_{tablename}'

def count_study_population() -> str:
    view_name = name_cube('study_population')
    from_table = name_cohort('study_population')
    cols = ['enc_class_code',
            'enc_type_display',
            'age_at_visit',
            'gender',
            'race_display',
            'ethnicity_display']

    sql = CountsBuilder(PREFIX).count_encounter(view_name, from_table, cols)
    return save_athena_sql(view_name, sql)

def make():
    return [count_study_population()]
