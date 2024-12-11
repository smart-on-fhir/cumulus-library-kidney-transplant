from kidney_transplant import fhir2sql, common, guard
from kidney_transplant.fhir2sql import include, exclude
from kidney_transplant.criteria.demographic import gender, race
from kidney_transplant.criteria.encounter import study_period
from kidney_transplant.criteria.encounter.encounter_class import EncounterClass


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