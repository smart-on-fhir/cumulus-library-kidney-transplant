create table irae__cohort_rx_tacrolimus as 
select distinct * from 
 irae__cohort_study_population_rx , 
irae__valueset_rx_tacrolimus
WHERE
irae__cohort_study_population_rx.rx_code = irae__valueset_rx_tacrolimus.code and 
irae__cohort_study_population_rx.rx_system = irae__valueset_rx_tacrolimus.system