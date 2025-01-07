create table irae__cohort_lab_sirolimus as 
select * from 
 irae__cohort_study_population_lab , 
irae__lab_sirolimus
WHERE
irae__cohort_study_population_lab.lab_observation_code = irae__lab_sirolimus.code and 
irae__cohort_study_population_lab.lab_observation_system = irae__lab_sirolimus.system