from irae import fhir2sql, common, guard
from irae.fhir2sql import include, exclude
from irae.criteria.demographic import gender, race
from irae.criteria.encounter import study_period
from irae.criteria.encounter.encounter_class import EncounterClass


codes = guard.as_coding(EncounterClass.EMER)

_sql = include([codes], 'encounter_class')

print(_sql)



# from kidney_transplant.criteria.document import document
#
# _gender = gender.include_sex(female=True, male=True, other=True, unknown=False)
#
# # _gender = gender.sql_view(female=True, male=True, unknown=False, other=True)
# # # _race = race.sql_view(None)
# # _period = study_period.sql_view('2012-01-01')
# # _class = encounter_class.sql_view_from_enum([encounter_class.EncounterClass.EMER])
# # _doctype = document.sql_view_document_type()
# # print(_class)
#
#
#
# _class = encounter_class.sql_view_from_enum([encounter_class.EncounterClass.EMER])
#
# # include_valueset(