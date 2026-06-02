create table irae__cohort_lab_hdl as 
select distinct * from 
 irae__cohort_study_population_lab , 
irae__valueset_lab_hdl
WHERE
irae__cohort_study_population_lab.lab_observation_code = irae__valueset_lab_hdl.code and 
irae__cohort_study_population_lab.lab_observation_system = irae__valueset_lab_hdl.system