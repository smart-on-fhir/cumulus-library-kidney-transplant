create or replace view irae__lab_interpretation as 
 select 'lab_interpretation_any' as valueset, system, code, display from 
 irae__lab_interpretation_any
 UNION select 'lab_interpretation_abnormal' as valueset, system, code, display from 
 irae__lab_interpretation_abnormal
 UNION select 'lab_interpretation_low' as valueset, system, code, display from 
 irae__lab_interpretation_low
 UNION select 'lab_interpretation_high' as valueset, system, code, display from 
 irae__lab_interpretation_high