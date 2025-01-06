from typing import List
from irae import fhir2sql
from irae import resources

def list_tables():
    """
    :return: list of tables in the `study_population`, one for each aspect such as Dx, Rx, Lab,
    """
    table = fhir2sql.name_join('cohort', 'study_population')
    aspect_list = ['dx', 'rx', 'lab', 'doc', 'proc']
    aspect_list = [f'{table}_{t}' for t in aspect_list]
    return [table] + aspect_list

def make() -> List[str]:
    """
    :return: list of `study_population` tables
    """
    file_list = list()
    for table in list_tables():
        sql = resources.read_text(resources.path_template(f'{table}.sql'))
        file_list.append(resources.save_athena_view(table, sql))
    return file_list
