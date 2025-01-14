create or replace view irae__proc_nephrectomy as 
 select 'proc_nephrectomy_sct' as subtype, system, code, display from 
 irae__proc_nephrectomy_sct
 UNION select 'proc_nephrectomy_icd10pcs' as subtype, system, code, display from 
 irae__proc_nephrectomy_icd10pcs