create or replace view irae__proc_transplant as 
 select 'proc_transplant_kidney' as valueset, system, code, display from 
 irae__proc_transplant_kidney
 UNION select 'proc_transplant_solid_organ' as valueset, system, code, display from 
 irae__proc_transplant_solid_organ
 UNION select 'proc_transplant_recipient' as valueset, system, code, display from 
 irae__proc_transplant_recipient