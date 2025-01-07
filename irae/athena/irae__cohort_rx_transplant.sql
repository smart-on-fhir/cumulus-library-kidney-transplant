create table irae__cohort_rx_transplant as 
select * from 
 irae__cohort_study_population_rx , 
irae__rx_transplant
WHERE
irae__cohort_study_population_rx.rx_code = irae__rx_transplant.code and 
irae__cohort_study_population_rx.rx_system = irae__rx_transplant.system