create or replace view irae__dx_diabetes as 
 select 'dx_diabetes_disorder' as subtype, system, code, display from 
 irae__dx_diabetes_disorder
 UNION select 'dx_diabetes_preexisting' as subtype, system, code, display from 
 irae__dx_diabetes_preexisting
 UNION select 'dx_diabetes_complications' as subtype, system, code, display from 
 irae__dx_diabetes_complications
 UNION select 'dx_diabetes_td2_related_dx' as subtype, system, code, display from 
 irae__dx_diabetes_td2_related_dx
 UNION select 'dx_diabetes_diabetic_nephropathy' as subtype, system, code, display from 
 irae__dx_diabetes_diabetic_nephropathy
 UNION select 'dx_diabetes_diabetic_ckd' as subtype, system, code, display from 
 irae__dx_diabetes_diabetic_ckd