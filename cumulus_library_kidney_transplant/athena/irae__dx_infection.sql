create or replace view irae__dx_infection as 
 select 'dx_infection_bacterial' as valueset, system, code, display from 
 irae__dx_infection_bacterial
 UNION select 'dx_infection_pna' as valueset, system, code, display from 
 irae__dx_infection_pna
 UNION select 'dx_infection_cmv' as valueset, system, code, display from 
 irae__dx_infection_cmv
 UNION select 'dx_infection_rsv' as valueset, system, code, display from 
 irae__dx_infection_rsv
 UNION select 'dx_infection_hsv' as valueset, system, code, display from 
 irae__dx_infection_hsv
 UNION select 'dx_infection_influenza' as valueset, system, code, display from 
 irae__dx_infection_influenza
 UNION select 'dx_infection_shingles' as valueset, system, code, display from 
 irae__dx_infection_shingles
 UNION select 'dx_infection_hepatitis_b' as valueset, system, code, display from 
 irae__dx_infection_hepatitis_b
 UNION select 'dx_infection_hepatitis_c' as valueset, system, code, display from 
 irae__dx_infection_hepatitis_c