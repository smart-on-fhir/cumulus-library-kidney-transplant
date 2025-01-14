create or replace view irae__proc_surgery as 
 select 'proc_surgery_other_major' as subtype, system, code, display from 
 irae__proc_surgery_other_major