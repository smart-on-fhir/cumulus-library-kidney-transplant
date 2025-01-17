create or replace view irae__lab_interpretation_high as select * from (values
('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', '>', 'Off scale high')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'H', 'High')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'H>', 'Significantly high')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'HH', 'Critical high')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'HU', 'Significantly high')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'HX', 'above high threshold')
) AS t (system, code, display) ;