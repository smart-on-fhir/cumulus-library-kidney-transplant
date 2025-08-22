create or replace view irae__dx_transplant_complication as select * from (values
('http://hl7.org/fhir/sid/icd-10-cm', 'T86.1', 'Complications of kidney transplant')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T86.10', 'Unspecified complication of kidney transplant')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T86.11', 'Kidney transplant rejection')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T86.12', 'Kidney transplant failure')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T86.13', 'Kidney transplant infection')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T86.19', 'Other complication of kidney transplant')
) AS t (system, code, display) ;