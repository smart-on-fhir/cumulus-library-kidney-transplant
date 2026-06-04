create table irae__cohort_rx_ivig as 
select distinct * from 
 irae__cohort_study_population_rx , 
irae__valueset_rx_ivig
WHERE
irae__cohort_study_population_rx.rx_code = irae__valueset_rx_ivig.code and 
irae__cohort_study_population_rx.rx_system = irae__valueset_rx_ivig.system