from typing import List
from irae import fhir2sql, common

TABLE = 'irae__cohort_study_population'

def list_tables():
    return [TABLE, f'{TABLE}_dx', f'{TABLE}_rx', f'{TABLE}_lab', f'{TABLE}_doc']

def make() -> List[str]:
    file_list = list()
    for table in list_tables():
        sql = common.read_text(fhir2sql.path_template(f'{table}.sql'))
        file_list.append(fhir2sql.save_athena_sql(table, sql))
    return file_list
