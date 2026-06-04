create table irae__cohort_rx_basiliximab as 
select distinct * from 
 irae__cohort_study_population_rx , 
irae__valueset_rx_basiliximab
WHERE
irae__cohort_study_population_rx.rx_code = irae__valueset_rx_basiliximab.code and 
irae__cohort_study_population_rx.rx_system = irae__valueset_rx_basiliximab.system