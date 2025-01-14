create or replace view irae__lab_diabetes as 
 select 'lab_diabetes_screening' as subtype, system, code, display from 
 irae__lab_diabetes_screening
 UNION select 'lab_diabetes_glucose_test' as subtype, system, code, display from 
 irae__lab_diabetes_glucose_test