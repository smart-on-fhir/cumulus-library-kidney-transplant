create or replace view irae__dx_cancer as 
 select 'dx_cancer_malignant_melanoma_sct' as subtype, system, code, display from 
 irae__dx_cancer_malignant_melanoma_sct
 UNION select 'dx_cancer_malignant_melanoma_icd10' as subtype, system, code, display from 
 irae__dx_cancer_malignant_melanoma_icd10