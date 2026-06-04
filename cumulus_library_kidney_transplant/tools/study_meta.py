from pathlib import Path
from cumulus_library_kidney_transplant.tools import manifest, template

DATA_PACKAGE_VERSION = 4

def make_study_meta_sql(data_package_version:int = DATA_PACKAGE_VERSION) -> list[Path]:
    """
    https://docs.smarthealthit.org/cumulus/library/creating-studies.html#metadata-tables
    """
    return [template.copy(f"meta_date.sql"),
            template.copy(f"meta_version.sql", data_package_version=str(data_package_version))]

def make():
    """
    Make SQL study meta and suggest TOML, example

    [[actions]]
    description = "export metadata"
    type = "build:serial"
    files = [
        'athena/irae__meta_date.sql',
        'athena/irae__meta_version.sql'
    ]

    [[actions]]
    description = "export metadata"
    type = "export:meta"
    tables = [
        'irae__meta_date',
        'irae__meta_version'
    ]
    """
    file_list = make_study_meta_sql()
    return [
        manifest.as_toml_sql(file_list, 'SQL study metadata'),
        manifest.as_toml_tables(file_list, 'export study metadata', 'export:meta')
    ]

if __name__ == '__main__':
    for target in make():
        print(target)
