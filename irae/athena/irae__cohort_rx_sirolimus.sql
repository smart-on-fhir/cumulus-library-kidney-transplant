create table irae__cohort_rx_sirolimus as 
select * from 
 irae__cohort_study_population_rx , 
irae__rx_sirolimus
WHERE
irae__cohort_study_population_rx.rx_code = irae__rx_sirolimus.code and 
irae__cohort_study_population_rx.rx_system = irae__rx_sirolimus.system