from typing import List
from pathlib import Path
from irae import fhir2sql
from irae import filetool

def list_tables() -> List[str]:
    """
    :return: list of tables in the `study_population`, one for each aspect such as Dx, Rx, Lab,
    """
    table = fhir2sql.name_join('cohort', 'study_population')
    aspect_list = ['dx', 'rx', 'lab', 'doc', 'proc']
    aspect_list = [f'{table}_{t}' for t in aspect_list]
    return [table] + aspect_list

def make_study_population() -> List[Path]:
    """
    :return: list of SQL `study_population`
    """
    file_list = list()
    for table in list_tables():
        sql = filetool.load_template(f'{table}.sql')
        sql = filetool.inline_template(sql)
        file_list.append(filetool.save_athena_view(table, sql))
    return file_list

def make() -> List[Path]:
    return make_study_population()
