create or replace view irae__dx_autoimmune as 
 select 'dx_autoimmune_inflammatory' as subtype, system, code, display from 
 irae__dx_autoimmune_inflammatory
 UNION select 'dx_autoimmune_ibd' as subtype, system, code, display from 
 irae__dx_autoimmune_ibd
 UNION select 'dx_autoimmune_crohns' as subtype, system, code, display from 
 irae__dx_autoimmune_crohns
 UNION select 'dx_autoimmune_arthritis_ra' as subtype, system, code, display from 
 irae__dx_autoimmune_arthritis_ra
 UNION select 'dx_autoimmune_arthritis_disorders' as subtype, system, code, display from 
 irae__dx_autoimmune_arthritis_disorders
 UNION select 'dx_autoimmune_lupus' as subtype, system, code, display from 
 irae__dx_autoimmune_lupus