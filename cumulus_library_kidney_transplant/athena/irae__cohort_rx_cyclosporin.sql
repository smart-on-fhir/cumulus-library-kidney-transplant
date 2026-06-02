create table irae__cohort_rx_cyclosporin as 
select distinct * from 
 irae__cohort_study_population_rx , 
irae__valueset_rx_cyclosporin
WHERE
irae__cohort_study_population_rx.rx_code = irae__valueset_rx_cyclosporin.code and 
irae__cohort_study_population_rx.rx_system = irae__valueset_rx_cyclosporin.system