create or replace view irae__lab_creatinine as 
 select 'lab_creatinine_serum_cr' as valueset, system, code, display from 
 irae__lab_creatinine_serum_cr
 UNION select 'lab_creatinine_urine_cr' as valueset, system, code, display from 
 irae__lab_creatinine_urine_cr
 UNION select 'lab_creatinine_urine_alb_cr_ratio' as valueset, system, code, display from 
 irae__lab_creatinine_urine_alb_cr_ratio
 UNION select 'lab_creatinine_urine_protein_cr_ratio' as valueset, system, code, display from 
 irae__lab_creatinine_urine_protein_cr_ratio
 UNION select 'lab_creatinine_blood_cr' as valueset, system, code, display from 
 irae__lab_creatinine_blood_cr