create or replace view irae__lab_sirolimus as select * from (values
('http://loinc.org', 'LOINC_NUM', 'COMPONENT')
,('http://loinc.org', '49737-0', 'Sirolimus')
,('http://loinc.org', '29247-4', 'Sirolimus')
,('http://loinc.org', '80548-1', 'Sirolimus')
,('http://loinc.org', '72676-0', 'Sirolimus^trough')
,('http://loinc.org', '96462-7', 'Sirolimus')
) AS t (system, code, display) ;