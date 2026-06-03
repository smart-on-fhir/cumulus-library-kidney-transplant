from pathlib import Path
from cumulus_library_kidney_transplant.tools import filetool, template, tablespace, manifest

########################################################################################################
# make samples
##########################################################################################################
def make_samples() -> list[Path]:
    """
    Make note samples for each casedef temporality [pre, per, peri_post, post]
    """
    samples = [template.copy('sample_casedef.sql')]

    for temporality in ['pre', 'peri', 'peri_post', 'post']:
        samples += [make_temporality(f'sample_casedef_temporality', temporality),
                    make_temporality(f'sample_casedef_temporality_limit_patient', temporality, 10),
                    make_temporality(f'sample_casedef_temporality_limit_note', temporality, 50)]
    return samples

def make_temporality(template_name:str, temporality:str, limit: int = None) -> Path:
    """
    :param template_name: name of the SQL template to load
    :param temporality: str one of ['pre', 'peri', 'peri_post', 'post']
    :param limit: int patients or notes in sample
    :return: path to Athena SQL
    """
    table_name = template_name.replace('temporality', temporality)

    if limit:
        limit = str(limit)
        table_name = f'{table_name}_{limit}'
    else:
        limit = ''

    text = template.load(f'{template_name}.sql',
                         temporality=temporality,
                         limit=limit)

    target_table = tablespace.name_prefix(table_name)
    target_file = filetool.path_athena(f'{target_table}.sql')
    return Path(filetool.write_text(text, target_file))

#-----------------------------------------------------------------------------
# Make
#-----------------------------------------------------------------------------
def make() -> list[str]:
    sample_list = make_samples()
    return [manifest.as_toml_sql(sample_list, 'samples for casedef temporality [pre, per, peri_post, post]')]

if __name__ == '__main__':
    for target in make():
        print(target)


