create or replace view irae__lab_hemoglobin_a1c as select * from (values
('http://loinc.org', 'LOINC_NUM', 'COMPONENT')
,('http://loinc.org', '55454-3', 'Hemoglobin A1c')
,('http://loinc.org', '41995-2', 'Hemoglobin A1c')
,('http://loinc.org', '86910-7', 'Hemoglobin A1c/Hemoglobin.total goal')
,('http://loinc.org', '4548-4', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '71875-9', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '17855-8', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '96595-4', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '4549-2', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '17856-6', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '62388-4', 'Hemoglobin A1c/Hemoglobin.total')
,('http://loinc.org', '59261-8', 'Hemoglobin A1c/Hemoglobin.total')
) AS t (system, code, display) ;