from typing import List
from irae import resources

TABLE = 'irae__cohort_study_population'

def list_tables():
    type_list = ['dx', 'rx', 'lab', 'doc', 'proc']
    type_list = [f'{TABLE}_{t}' for t in type_list]
    return [TABLE] + type_list

def make() -> List[str]:
    file_list = list()
    for table in list_tables():
        sql = resources.read_text(resources.path_template(f'{table}.sql'))
        file_list.append(resources.save_athena_view(table, sql))
    return file_list
