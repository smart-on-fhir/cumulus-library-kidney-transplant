create or replace view irae__dx_cancer as 
 select 'dx_cancer_skin' as valueset, system, code, display from 
 irae__dx_cancer_skin
 UNION select 'dx_cancer_melanoma' as valueset, system, code, display from 
 irae__dx_cancer_melanoma
 UNION select 'dx_cancer_melanoma_malignant' as valueset, system, code, display from 
 irae__dx_cancer_melanoma_malignant
 UNION select 'dx_cancer_sarcoma' as valueset, system, code, display from 
 irae__dx_cancer_sarcoma
 UNION select 'dx_cancer_squamous' as valueset, system, code, display from 
 irae__dx_cancer_squamous