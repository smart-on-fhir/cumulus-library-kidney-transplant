create or replace view irae__dx_transplant_status as select * from (values
('http://hl7.org/fhir/sid/icd-10', 'code', 'str')
,('http://hl7.org/fhir/sid/icd-10', 'Z94.0', 'Kidney transplant status')
,('http://hl7.org/fhir/sid/icd-10', 'Z48.22', ' "Encounter for aftercare following kidney transplant"')
) AS t (system, code, display) ;