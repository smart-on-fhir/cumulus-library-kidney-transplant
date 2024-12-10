create or replace view kidney_transplant__include_demographic_sex as select * from (values
('http://hl7.org/fhir/ValueSet/administrative-gender', 'female', 'female')
,('http://hl7.org/fhir/ValueSet/administrative-gender', 'male', 'male')
,('http://hl7.org/fhir/ValueSet/administrative-gender', 'other', 'other')
) AS t (system, code, display) ;