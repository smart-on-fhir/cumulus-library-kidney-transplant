create or replace view irae__dx_infection_cmv_icd10 as select * from (values
('http://hl7.org/fhir/sid/icd-10-cm', 'B25.0', 'Cytomegaloviral pneumonitis')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B25.1', 'Cytomegaloviral hepatitis')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B25.2', 'Cytomegaloviral pancreatitis')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B25.8', 'Other cytomegaloviral diseases')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B25.9', 'Cytomegaloviral disease, unspecified')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B27.10', 'Cytomegaloviral mononucleosis without complications')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B27.11', 'Cytomegaloviral mononucleosis with polyneuropathy')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B27.12', 'Cytomegaloviral mononucleosis with meningitis')
,('http://hl7.org/fhir/sid/icd-10-cm', 'B27.19', 'Cytomegaloviral mononucleosis with other complication')
,('http://hl7.org/fhir/sid/icd-10-cm', 'P35.1', 'Congenital cytomegalovirus infection')
) AS t (system, code, display) ;