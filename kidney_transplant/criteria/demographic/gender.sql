create or replace view kidney_transplant__demographic_gender as select * from
(VALUES
     ('http://hl7.org/fhir/ValueSet/administrative-gender', 'Male', $male)
    ,('http://hl7.org/fhir/ValueSet/administrative-gender', 'Female', $female)
    ,('http://hl7.org/fhir/ValueSet/administrative-gender', 'Other', $male)
    ,('http://hl7.org/fhir/ValueSet/administrative-gender', 'Unknown', $male)
) AS t (system, gender, include);