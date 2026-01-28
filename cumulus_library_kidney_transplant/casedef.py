from pathlib import Path
from typing import List
from cumulus_library_kidney_transplant import fhir2sql, filetool

########################################################################################################
# CASE DEFINITION
##########################################################################################################
def name_casedef() -> str:
    """
    :return: str Tablename of casedef like irae__cohort_casedef
    """
    return fhir2sql.name_join('cohort', 'casedef')

def make_casedef_custom_csv() -> Path:
    """
    Load the custom case definition CSV file.
    """
    file_csv = filetool.path_spreadsheet('casedef_custom.csv')
    view_name_csv = fhir2sql.name_prefix('casedef_custom_csv')
    return fhir2sql.csv2view(file_csv, view_name_csv)

def make_casedef_custom() -> Path:
    """
    Flag Include/Exclude rules for "First" encounters.
    """
    file_sql = filetool.load_template('casedef.sql')
    view_name = fhir2sql.name_prefix('casedef')
    return fhir2sql.save_athena_view(view_name, file_sql)

########################################################################################################
# Select cohorts matching casedef
##########################################################################################################
def make_cohort(include_exclude: str = None) -> Path:
    """
    :param include_exclude: name of the SQL Template to make the cohort from
    :return: Path to cohort_casedef SQL
    """
    if include_exclude is None:
        table = name_casedef()
    else:
        table = f"{name_casedef()}_{include_exclude}"
    sql = filetool.load_template(f'{table}.sql')
    return filetool.save_athena_view(table, sql)

########################################################################################################
# case definition "aspects"
##########################################################################################################
def make_cohort_aspects() -> list[Path]:
    """
    Make cohort for casdef [dx, rx, lab, proc]
    """
    return [filetool.copy_template(f'cohort_casedef_{aspect}.sql')
            for aspect in ['dx', 'rx', 'lab', 'proc']]

########################################################################################################
# make samples
##########################################################################################################
def make_samples() -> list[Path]:
    """
    Make note samples for each casedef temporality [pre, per, peri_post, post]
    """
    samples = [filetool.copy_template('sample_casedef.sql')]

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
    :return: path to Atehna SQL
    """
    table_name = template_name.replace('temporality', temporality)

    if limit:
        limit = str(limit)
        table_name = f'{table_name}_{limit}'
    else:
        limit = ''

    replacements = {'$temporality': temporality, '$limit': limit}
    text = filetool.load_template(f'{template_name}.sql', replacements)
    target_table = fhir2sql.name_prefix(table_name)
    target_file = filetool.path_athena(f'{target_table}.sql')
    return Path(filetool.write_text(text, target_file))

########################################################################################################
# make
##########################################################################################################
def make() -> List[Path]:
    """
    Case Definition processing steps
    1. Load custom CSV file containing metatadata into Athena SQL

    2. Process SQL table with include/exclude rules.

    3. Create cohort of patients matching case definition

    4. "Exclude" (flag) patients matching the case definition for whome exclusion criteria was found.
    For example, patients who had a transplant *outcome* before a kidney transplant diagnosis or surgery.

    5. "Include" (flag) patients matching the case definition for whome exclusion criteria was found.
    The include cohort is the set of patients MINUS the exclude patients from previous step.

    6. CTAS "peri": first encounter matching the case definition.
    This is the index date (medical research term not SQL index).

    7. CTAS "Pre" encounters before index date for patients matching the case definition.
    This is the patient longitudinal history.

    8. CTAS "Post" encounters after index date for patients matching the case definition.
    This is the patient treatment and outcome cohort.

    9. "Timeline" is a simple unified view of pre/index/post tables with a column designating "period".

    10. "samples" of documented encounters are selected at varying sizes for each "period" .
    * "index"   samples (All, 10 patients, and 100 patients)
    * "pre"     samples (All, 10 patients, and 100 patients)
    * "post"    samples (All, 10 patients, and 100 patients)

    :return: List of SQL table cohorts selected before and after the case definition +timeline +samples
    """
    return [make_casedef_custom_csv(),
            make_casedef_custom(),
            make_cohort('candidate'),
            make_cohort('exclude'),
            make_cohort('include'),
            make_cohort()] + make_cohort_aspects() + make_samples()