from pathlib import Path
from functools import lru_cache
from cumulus_library import StudyManifest
from cumulus_library_kidney_transplant.tools import filetool

#-----------------------------------------------------------------------------
# get study manifest using cumulus library
#-----------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_manifest(manifest_path: Path|str = None) -> StudyManifest:
    """
    This method encapsulated changes to v6 StudyManifest
    default: filetool.path_project() = "cumulus_library_irae_cds"

    :param manifest_path: optional path to manifest file
    :return: StudyManifest
    """
    if not manifest_path:
        manifest_path = filetool.path_project()
    if isinstance(manifest_path, str):
        manifest_path = filetool.path_project(manifest_path)
    return StudyManifest(manifest_path)

#-----------------------------------------------------------------------------
# LOAD ONCE
#-----------------------------------------------------------------------------
MANIFEST = get_manifest()
PREFIX = get_manifest().get_study_prefix()

#-----------------------------------------------------------------------------
# TOML helpers
#-----------------------------------------------------------------------------
def _quote(text:str, quote_char:str='"') -> str:
    return quote_char + text + quote_char

def header(name:str='actions') -> str:
    return f"\n[[{name}]]\n"

def as_toml_sql(file_list:list[Path], description:str=None, type_build='build:parallel') -> str:
    """
    @Refactor: TOML templates be Jinja `template.py`

    :param description: key name to display during build
    :param file_list: list of paths to files to execute in parallel
    :param type_build builld:serial False if builld:parallel
    :return: str content for `manifest.toml` submanifest
    """
    _desc = f'description={_quote(description)}'
    _type = 'type=' + _quote(type_build)
    _files = [_quote('athena/'+f.name) for f in file_list]
    _files = 'files= [\n\t'+ ',\n\t'.join(_files) + '\n]'
    return  header() + '\n'.join([_desc, _type, _files])

def as_toml_tables(file_list:list[Path], description:str=None, type_export='export:counts') -> str:
    """
    @Refactor: TOML templates be Jinja `template.py`

    :param description: key name to display during build
    :param file_list: list of paths to files to execute in parallel
    :param type_export: supports one of ['export:counts', 'export:annotated_counts', 'export:flat', 'export:metadata']
    :return: str content for `manifest.toml` submanifest
    """
    _desc = f'description={_quote(description)}'
    _type = 'type=' + _quote(type_export)

    _files = [_quote(f.stem) for f in file_list]
    _files = 'tables= [\n\t'+ ',\n\t'.join(_files) + '\n]'
    return  header() + '\n'.join([_desc, _type, _files])

def as_toml_file_upload(file_list:list[Path]) -> str:
    """
    @Refactor: TOML templates be Jinja `template.py`

    :return: str content for `manifest.toml` submanifest
    """
    out = ['config_type="file_upload"']
    for filename in file_list:
        simple  = filetool.file_to_simplename(filename.name)
        if 'include' in filename.name:
            out.append(f'[tables.{simple}]')
        else:
            out.append(f'[tables.valueset_{simple}]')
        out.append(f'file = "{filename.name}"')
        out.append('')
    return '\n'.join(out)

