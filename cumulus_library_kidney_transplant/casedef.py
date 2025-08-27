from pathlib import Path
from typing import List
from cumulus_library_kidney_transplant import fhir2sql, filetool

########################################################################################################
# CASE DEFINITION
##########################################################################################################
def name_casedef() -> str:
    """
    :return: Tablename of casedef like irae__cohort_casedef
    """
    return fhir2sql.name_join('cohort', 'casedef')

def make_casedef_custom_csv() -> Path:
    file_csv = filetool.path_spreadsheet('casedef_custom.csv')
    view_name_csv = fhir2sql.name_prefix('casedef_custom_csv')
    return fhir2sql.csv2view(file_csv, view_name_csv)

def make_casedef_custom() -> Path:
    file_sql = filetool.load_template('casedef.sql')
    view_name = fhir2sql.name_prefix('casedef')
    return fhir2sql.save_athena_view(view_name, file_sql)

########################################################################################################
# Select cohorts matching casedef
##########################################################################################################
def make_cohort(include_exclude: str = None) -> Path:
    if include_exclude is None:
        table = name_casedef()
    else:
        table = f"{name_casedef()}_{include_exclude}"
    sql = filetool.load_template(f'{table}.sql')
    return filetool.save_athena_view(table, sql)

########################################################################################################
# Index first encounter matching case definition
##########################################################################################################

def make_index_date(variable, suffix, equality) -> Path:
    """
    Index date refers when the case definition criteria was first met.
    This means the first Encounter where $variable was recorded for each patient.

    `template/cohort_casedef_index.sql`

    :param variable: case definition variable table
    :param suffix:
        "pre"= select cohort BEFORE case definition first recorded;
        "post"= select cohort AFTER case definition first recorded
    :param equality: date comparison "=", "<", ">"

    :return: Path to SQL table containing cohort matching case definition
    """
    view = f'{name_casedef()}_{suffix}.sql'
    template = f'{name_casedef()}_index.sql'
    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql, variable)
    sql = sql.replace('$suffix', suffix)
    sql = sql.replace('$equality', equality)
    return filetool.save_athena(view, sql)

########################################################################################################
# Timeline (pre/index/post) view with `cohort_study_variables_wide`
##########################################################################################################

def make_timeline() -> Path:
    """
    Return a timeline of the case definition with respect to all study variables.
    see `template/cohort_casedef_timeline.sql`
    :return: SQL file of case definition cohort as a timeline sequence of events.
    """
    template = fhir2sql.name_join('cohort', 'casedef_timeline') + '.sql'
    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql)
    return filetool.save_athena(template, sql)

########################################################################################################
# Samples for Chart Review and QA
##########################################################################################################
def make_samples(size: int = None, suffix: str = 'post') -> Path:
    """
    This method is for sampling Documents for LLM/ChartReview.
    This is not used to generate CUBE data.

    See `template/sample_casedef*`

    :param size: number of FHIR DocumentReference samples to select from casedef
    :param suffix: "pre" or "post", samples from before or after first record of case definition variale.
    :return: Path to SQL file with case definition samples.
    """
    table = fhir2sql.name_sample('casedef')
    if size:
        template = f"{table}_size.sql"
        target = f"{table}_{suffix}_{size}.sql"
    else:
        template = f"{table}.sql"
        target = f"{table}_{suffix}.sql"

    sql = filetool.load_template(template)
    sql = filetool.inline_template(sql)
    sql = sql.replace('$size', str(size))
    sql = sql.replace('$suffix', suffix)
    return filetool.save_athena(target, sql)


def make(variable=None) -> List[Path]:
    """
    Case definition is the target variable, such as a diagnosis or an intervention (such as a drug).
    IRAE study uses immunosuppression as the study variable. See README at the top of this file.

    :param variable: cohort name to treat as the "case definition"
    :return: List of SQL table cohorts selected before and after the case definition +timeline +samples
    """
    if not variable:
        variable = fhir2sql.name_join('cohort', 'casedef')

    return [make_casedef_custom_csv(),
            make_casedef_custom(),
            make_cohort(),
            make_index_date(variable, 'index', '='),
            make_index_date(variable, 'pre', '<'),
            make_index_date(variable, 'post', '>'),
            make_cohort('exclude'),
            make_cohort('include'),
            make_timeline(),
            make_samples(None, 'index'),
            make_samples(10, 'index'),
            make_samples(100, 'index'),
            make_samples(None, 'pre'),
            make_samples(10, 'pre'),
            make_samples(100, 'pre'),
            make_samples(None, 'post'),
            make_samples(10, 'post'),
            make_samples(100, 'post')]
