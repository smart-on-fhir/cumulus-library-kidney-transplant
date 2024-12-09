import os
from kidney_transplant import fhir2sql, common

def filepath(filename: str) -> str:
    pwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(pwd, filename)

def as_sql(female=True, male=True, other=True, unknown=True) -> str:
    """
    :param female: Default True (include)
    :param male: Default True (include)
    :param other: Default True (include)
    :param unknown: Default True (include)
    :return: str SQL statement for create view $studyname__demographic_gender
    """
    _sql = common.read_text(filepath(__file__.replace('.py', '.sql')))

    _sql = _sql.replace('$female', str(female))
    _sql = _sql.replace('$male', str(male))
    _sql = _sql.replace('$other', str(other))
    _sql = _sql.replace('$unknown', str(unknown))
    return _sql
