from pathlib import Path
from typing import List
from cumulus_library_kidney_transplant import fhir2sql, filetool

########################################################################################################
# CASE DEFINITION
#
# A special variable "case definition" defines who is "positive" for the disease of interest.
# For this IRAE kidney transplant study, the "case definition" are patients who receive immunosuppressive
# drugs following a kidney transplant.
#
# Note that all participating sites (except BCH) are loading (via cumulus-etl) only patients who have
# recieved a kidney transplant. We then refine the selection to include only patients on immunosuppresive
# drugs.
#
# TODO: importantly, BCH Athena includes patients with and without transplant.
# Note that in BCH data case_definition currently means the patient has a FHIR MedicationRequest for one of
# `rx_custom` medications. Be aware that BCH data 'case definition' includes patients without a kideny transplant.
# For example, patient may have had a heart transplant, or other reason for immunosuppresive medication.
#
##########################################################################################################
def name_casedef() -> str:
    """
    :return: Tablename of casedef like irae__cohort_casedef
    """
    return fhir2sql.name_join('cohort', 'casedef')

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

def make_samples(size: int = None, suffix: str = 'post') -> Path:
    """
    This method is for sampling Documents for LLM/ChartReview.
    This is not used to generate CUBE data.

    See `template/sample_casedef*`

    :param size: number of FHIR DocumentReference samples to select from casedef
    :param suffix: "pre" or "post", samples from before or after first record of case definition variale.
    :return: Path to SQL file with case definition samples.
    """
    table = fhir2sql.name_join('sample', 'casedef')
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
        variable = fhir2sql.name_join('cohort', 'rx_custom')

    return [make_index_date(variable, 'index', '='),
            make_index_date(variable, 'pre', '<'),
            make_index_date(variable, 'post', '>'),
            make_timeline(),
            make_samples(None, 'pre'),
            make_samples(100, 'pre'),
            make_samples(1000, 'pre'),
            make_samples(None, 'post'),
            make_samples(100, 'post'),
            make_samples(1000, 'post')]
