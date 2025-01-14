create or replace view irae__lab_azathioprine as select * from (values
('http://loinc.org', 'LOINC_NUM', 'COMPONENT')
,('http://loinc.org', '16419-4', 'azaTHIOprine')
,('http://loinc.org', '43924-0', 'azaTHIOprine')
) AS t (system, code, display) ;