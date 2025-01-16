create or replace view irae__dx_autoimmune as 
 select 'dx_autoimmune_inflammatory' as valueset, system, code, display from 
 irae__dx_autoimmune_inflammatory
 UNION select 'dx_autoimmune_ibd' as valueset, system, code, display from 
 irae__dx_autoimmune_ibd
 UNION select 'dx_autoimmune_crohns' as valueset, system, code, display from 
 irae__dx_autoimmune_crohns
 UNION select 'dx_autoimmune_arthritis_ra' as valueset, system, code, display from 
 irae__dx_autoimmune_arthritis_ra
 UNION select 'dx_autoimmune_arthritis_disorders' as valueset, system, code, display from 
 irae__dx_autoimmune_arthritis_disorders
 UNION select 'dx_autoimmune_lupus' as valueset, system, code, display from 
 irae__dx_autoimmune_lupus