create table irae__cohort_lab_gad as 
select distinct * from 
 irae__cohort_study_population_lab , 
irae__valueset_lab_gad
WHERE
irae__cohort_study_population_lab.lab_observation_code = irae__valueset_lab_gad.code and 
irae__cohort_study_population_lab.lab_observation_system = irae__valueset_lab_gad.system