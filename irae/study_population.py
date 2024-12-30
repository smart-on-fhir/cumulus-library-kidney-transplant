from typing import List
from irae import fhir2sql, common

TABLE = 'irae__cohort_study_population'

def list_tables():
    type_list = ['dx', 'rx', 'lab', 'doc', 'proc']
    type_list = [f'{TABLE}_{t}' for t in type_list]
    return [TABLE] + type_list

def make() -> List[str]:
    file_list = list()
    for table in list_tables():
        sql = common.read_text(fhir2sql.path_template(f'{table}.sql'))
        file_list.append(fhir2sql.save_athena_sql(table, sql))
    return file_list
