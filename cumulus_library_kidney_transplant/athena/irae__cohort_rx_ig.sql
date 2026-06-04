create table irae__cohort_rx_ig as 
select distinct * from 
 irae__cohort_study_population_rx , 
irae__valueset_rx_ig
WHERE
irae__cohort_study_population_rx.rx_code = irae__valueset_rx_ig.code and 
irae__cohort_study_population_rx.rx_system = irae__valueset_rx_ig.system