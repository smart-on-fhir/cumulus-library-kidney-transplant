create table irae__cohort_study_population_rx as
select distinct
    RX.status               as rx_status,
    RX.category_code        as rx_category_code,
    RX.category_system      as rx_category_system,
    RX.medication_code      as rx_code,
    RX.medication_display   as rx_display,
    RX.medication_system    as rx_system,
    RX.medicationrequest_ref as medicationrequest_ref,
    study_population.*
from
    irae__cohort_study_population as study_population
left join core__medicationrequest as RX
    on RX.encounter_ref = study_population.encounter_ref
;
