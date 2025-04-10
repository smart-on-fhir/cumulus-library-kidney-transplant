create or replace view irae__dx_transplant_donor as select * from (values
('http://hl7.org/fhir/sid/icd-10', 'code', 'str')
,('http://hl7.org/fhir/sid/icd-10', 'Z52.4', 'Kidney donor')
) AS t (system, code, display) ;