create or replace view irae__lab_cbc as 
 select 'lab_cbc_with_diff' as subtype, system, code, display from 
 irae__lab_cbc_with_diff