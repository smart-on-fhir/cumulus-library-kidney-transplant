from pathlib import Path
from cumulus_library_kidney_transplant.tools import filetool, template, tablespace, manifest
from cumulus_library_kidney_transplant.tools.study_variable import Aspect, list_aspect_names

########################################################################################################
# make samples
##########################################################################################################
def make_samples() -> list[Path]:
    """
    Make note samples for each casedef temporality [pre, per, peri_post, post]
    Make note samples for each casedef variable type (aspect like dx, rx, lab)
    """
    samples = [template.copy('sample_casedef.sql')]

    for aspect in list_aspect_names():
        samples.append(make_aspect(aspect))

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

def make_aspect(aspect:Aspect|str) -> Path:
    """
    Intended use:
    * Aspect.dx:    sample casedef notes that have an encounter matching 1+ "dx" study variable(s)
                    Validate if case definition was "first" kidney transplant.
    * Aspect.rx:    sample casedef notes that have an encounter matching 1+ "rx" study variable(s)
                    Validate medications were active/stopped/etc
    * Aspect.lab:   sample casedef notes that have an encounter matching 1+ "lab" study variable(s)
                    Validate lab values

    :param aspect: name of aspect to sample
    :return: path to Athena SQL
    """
    if isinstance(aspect, Aspect):
        return make_aspect(aspect.name)
    content = template.load('sample_casedef_aspect.sql', aspect=aspect)
    table = tablespace.name_prefix(f'sample_casedef_{aspect}')
    path = filetool.path_athena(f'{table}.sql')
    return filetool.save_athena(path, content)

#-----------------------------------------------------------------------------
# Make
#-----------------------------------------------------------------------------
def make() -> list[str]:
    sample_list = make_samples()

    return [manifest.as_toml_sql(sample_list, 'samples for casedef temporality [pre, per, peri_post, post]')]

if __name__ == '__main__':
    for target in make():
        print(target)


