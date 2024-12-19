from irae import common
from irae.fhir2sql import include
from irae.criteria import gender, race, document, study_period
from irae.criteria.encounter_class import EncounterClass
from irae.variable import vsac_variables, custom_variables, union_variables

def make_gender() -> str:
    codes = gender.sex2codelist(female=True, male=True, other=True, unknown=False)
    return include(codes, 'gender')

def make_race() -> str:
    codes = common.as_coding_list(list(race.Race))
    return include(codes, 'race')

def make_study_period() -> str:
    return study_period.include(
        period_start='2016-01-01',
        period_end='2025-01-01',
        include_history=True)

def make_encounter() -> str:
    codes = common.as_coding_list(EncounterClass.EMER)
    return include(codes, 'encounter_class')


def make_document_type() -> str:
    codes = document.get_valueset_doctype()
    return include(codes, 'document_type')


def make_document_facility() -> str:
    codes = document.get_valueset_facility()
    return include(codes, 'document_facility')


def make_document_practice() -> str:
    codes = document.get_valueset_practice()
    return include(codes, 'document_practice')


def make_variable_valuesets() -> str:
    pass


def make():
    criteria_sql = [
        make_study_period(),
        make_gender(),
        make_race(),
        make_encounter(),
        make_document_type(),
        make_document_facility(),
        make_document_practice()]

    variable_sql = [vsac_variables.make(),
                    custom_variables.make(),
                    union_variables.make()]


if __name__ == "__main__":
    make()
