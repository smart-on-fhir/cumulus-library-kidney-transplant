create or replace view irae__lab_interpretation_low as select * from (values
('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', '<', 'Off scale low')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'L', 'Low')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'L<', 'Significantly low')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'LL', 'Critical low')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'LU', 'Significantly low')
,('http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation', 'LX', 'below low threshold')
) AS t (system, code, display) ;