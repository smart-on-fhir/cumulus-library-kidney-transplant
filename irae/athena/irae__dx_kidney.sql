create or replace view irae__dx_kidney as 
 select 'dx_kidney_condition' as subtype, system, code, display from 
 irae__dx_kidney_condition
 UNION select 'dx_kidney_renal_disease' as subtype, system, code, display from 
 irae__dx_kidney_renal_disease
 UNION select 'dx_kidney_esrd' as subtype, system, code, display from 
 irae__dx_kidney_esrd
 UNION select 'dx_kidney_ckd' as subtype, system, code, display from 
 irae__dx_kidney_ckd
 UNION select 'dx_kidney_dialysis' as subtype, system, code, display from 
 irae__dx_kidney_dialysis
 UNION select 'dx_kidney_nephrotic_syndrome' as subtype, system, code, display from 
 irae__dx_kidney_nephrotic_syndrome