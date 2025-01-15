create or replace view irae__dx_cancer as 
 select 'dx_cancer_skin' as subtype, system, code, display from 
 irae__dx_cancer_skin
 UNION select 'dx_cancer_sarcoma' as subtype, system, code, display from 
 irae__dx_cancer_sarcoma
 UNION select 'dx_cancer_squamous' as subtype, system, code, display from 
 irae__dx_cancer_squamous
 UNION select 'dx_cancer_melanoma' as subtype, system, code, display from 
 irae__dx_cancer_melanoma