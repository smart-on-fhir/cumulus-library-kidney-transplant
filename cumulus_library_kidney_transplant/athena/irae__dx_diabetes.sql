create or replace view irae__dx_diabetes as 
 select 'dx_diabetes_disorder' as valueset, system, code, display from 
 irae__dx_diabetes_disorder
 UNION select 'dx_diabetes_preexisting' as valueset, system, code, display from 
 irae__dx_diabetes_preexisting
 UNION select 'dx_diabetes_complications' as valueset, system, code, display from 
 irae__dx_diabetes_complications
 UNION select 'dx_diabetes_t2d_related_dx' as valueset, system, code, display from 
 irae__dx_diabetes_t2d_related_dx
 UNION select 'dx_diabetes_diabetic_nephropathy' as valueset, system, code, display from 
 irae__dx_diabetes_diabetic_nephropathy
 UNION select 'dx_diabetes_diabetic_ckd' as valueset, system, code, display from 
 irae__dx_diabetes_diabetic_ckd