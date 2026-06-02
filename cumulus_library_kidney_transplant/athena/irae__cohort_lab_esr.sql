create table irae__cohort_lab_esr as 
select distinct * from 
 irae__cohort_study_population_lab , 
irae__valueset_lab_esr
WHERE
irae__cohort_study_population_lab.lab_observation_code = irae__valueset_lab_esr.code and 
irae__cohort_study_population_lab.lab_observation_system = irae__valueset_lab_esr.system