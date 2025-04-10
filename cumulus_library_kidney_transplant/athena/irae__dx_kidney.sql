create or replace view irae__dx_kidney as 
 select 'dx_kidney_condition' as valueset, system, code, display from 
 irae__dx_kidney_condition
 UNION select 'dx_kidney_renal_disease' as valueset, system, code, display from 
 irae__dx_kidney_renal_disease
 UNION select 'dx_kidney_esrd' as valueset, system, code, display from 
 irae__dx_kidney_esrd
 UNION select 'dx_kidney_ckd' as valueset, system, code, display from 
 irae__dx_kidney_ckd
 UNION select 'dx_kidney_akf' as valueset, system, code, display from 
 irae__dx_kidney_akf
 UNION select 'dx_kidney_dialysis' as valueset, system, code, display from 
 irae__dx_kidney_dialysis
 UNION select 'dx_kidney_nephrotic_syndrome' as valueset, system, code, display from 
 irae__dx_kidney_nephrotic_syndrome