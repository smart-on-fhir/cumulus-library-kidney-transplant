from typing import List
from pathlib import Path
import tomllib
from irae import resources

def path_manifest() -> Path:
    return resources.path_home('manifest.toml')

def read_manifest() -> dict:
    with open(path_manifest(), 'rb') as f:
        data = tomllib.load(f)
    return data

def write_manifest(file_list: List[Path] | List[str]) -> Path:
    manifest = list()
    for filename in file_list:
        filename = str(filename)
        if 'irae/' in filename:
            _, filename = filename.split('irae/')
        manifest.append(f"'{filename}'")
    text = ',\n'.join(manifest)
    return resources.save_athena('file_names.manifest.toml', text)

def get_study_prefix():
    return read_manifest().get('study_prefix')
