create or replace view irae__doc_biopsy as 
 select 'doc_biopsy_kidney' as valueset, system, code, display from 
 irae__doc_biopsy_kidney
 UNION select 'doc_biopsy_skin' as valueset, system, code, display from 
 irae__doc_biopsy_skin
 UNION select 'doc_biopsy_lung' as valueset, system, code, display from 
 irae__doc_biopsy_lung
 UNION select 'doc_biopsy_bone' as valueset, system, code, display from 
 irae__doc_biopsy_bone
 UNION select 'doc_biopsy_muscle' as valueset, system, code, display from 
 irae__doc_biopsy_muscle