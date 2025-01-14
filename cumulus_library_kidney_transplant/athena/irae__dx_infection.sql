create or replace view irae__dx_infection as 
 select 'dx_infection_bacterial' as subtype, system, code, display from 
 irae__dx_infection_bacterial
 UNION select 'dx_infection_pna' as subtype, system, code, display from 
 irae__dx_infection_pna
 UNION select 'dx_infection_cmv_icd10' as subtype, system, code, display from 
 irae__dx_infection_cmv_icd10
 UNION select 'dx_infection_cmv_sct' as subtype, system, code, display from 
 irae__dx_infection_cmv_sct
 UNION select 'dx_infection_rsv' as subtype, system, code, display from 
 irae__dx_infection_rsv
 UNION select 'dx_infection_influenza' as subtype, system, code, display from 
 irae__dx_infection_influenza
 UNION select 'dx_infection_shingles' as subtype, system, code, display from 
 irae__dx_infection_shingles
 UNION select 'dx_infection_hepatitis_b' as subtype, system, code, display from 
 irae__dx_infection_hepatitis_b
 UNION select 'dx_infection_hepatitis_c' as subtype, system, code, display from 
 irae__dx_infection_hepatitis_c