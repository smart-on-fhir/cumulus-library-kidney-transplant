from typing import List
from pathlib import Path
import tomllib
import tomli_w
from cumulus_library_kidney_transplant import guard, filetool

def get_file_config() -> List:
    return read_manifest().get('file_config')

def path_manifest() -> Path:
    return filetool.path_home('../manifest.toml')

def read_manifest() -> dict:
    with open(path_manifest(), 'rb') as f:
        data = tomllib.load(f)
    return data

def get_study_prefix() -> str:
    return str(read_manifest().get('study_prefix'))

def write_manifest(file_names: List[Path] | List[str]) -> Path:
    saved = read_manifest()
    saved['file_config']['file_names'] = path_relative(file_names)
    saved['export_config']['count_list'] = list_tables(file_names, '_count_')

    with open(str(path_manifest()), 'wb') as f:
        tomli_w.dump(saved, f)
    print('saved ' + str(path_manifest()))
    return path_manifest()

def list_tables(file_names: List[Path] | List[str], search_term: str = None) -> List[str]:
    """
    "athena/irae__include_study_period.sql",
    :param file_names:
    :return:
    """
    table_names = list()
    for table in path_relative(file_names):
        table = table.replace('athena/', '').replace('.sql', '')
        if search_term:
            if search_term in table:
                table_names.append(table)
        else:
            table_names.append(table)
    return table_names

def path_relative(file_names: List[Path] | List[str]) -> List[str]:
    split_token = 'cumulus_library_kidney_transplant/'
    simpler = list()
    for filename in guard.as_list_str(file_names):
        if split_token in filename:
            _, filename = filename.split(split_token)
        simpler.append(filename)
    return simpler
