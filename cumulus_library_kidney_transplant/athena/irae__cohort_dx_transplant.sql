create table irae__cohort_dx_transplant as 
select distinct * from 
 irae__cohort_study_population_dx , 
irae__valueset_dx_transplant
WHERE
irae__cohort_study_population_dx.dx_code = irae__valueset_dx_transplant.code and 
irae__cohort_study_population_dx.dx_system = irae__valueset_dx_transplant.system