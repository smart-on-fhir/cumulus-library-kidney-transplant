create table irae__cohort_lab_crp as 
select distinct * from 
 irae__cohort_study_population_lab , 
irae__valueset_lab_crp
WHERE
irae__cohort_study_population_lab.lab_observation_code = irae__valueset_lab_crp.code and 
irae__cohort_study_population_lab.lab_observation_system = irae__valueset_lab_crp.system