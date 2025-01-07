create table irae__cohort_rx_cyclosporin as 
select * from 
 irae__cohort_study_population_rx , 
irae__rx_cyclosporin
WHERE
irae__cohort_study_population_rx.rx_code = irae__rx_cyclosporin.code and 
irae__cohort_study_population_rx.rx_system = irae__rx_cyclosporin.system