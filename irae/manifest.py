from typing import List
from pathlib import Path
import tomllib
import tomli_w
from irae import guard, resources

def get_study_prefix() -> str:
    return str(read_manifest().get('study_prefix'))

def get_file_config() -> List:
    return read_manifest().get('file_config')

def path_manifest() -> Path:
    return resources.path_home('manifest.toml')

def read_manifest() -> dict:
    with open(path_manifest(), 'rb') as f:
        data = tomllib.load(f)
    return data

def write_manifest(file_names: List[Path] | List[str]) -> Path:
    saved = read_manifest()
    saved['file_config']['file_names'] = path_relative(file_names)

    with open(str(path_manifest()), 'wb') as f:
        tomli_w.dump(saved, f)
    print('saved ' + str(path_manifest()))
    return path_manifest()

def path_relative(file_names: List[Path] | List[str]) -> List[str]:
    prefix = get_study_prefix() + '/'
    simpler = list()
    for filename in guard.as_list_str(file_names):
        if prefix in filename:
            _, filename = filename.split(prefix)
        simpler.append(filename)
    return simpler
