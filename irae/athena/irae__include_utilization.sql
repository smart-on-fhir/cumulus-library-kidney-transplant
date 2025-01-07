create or replace view irae__include_utilization as 
select * from (values
(3,1000,90,36500)
) AS t (enc_min,enc_max,days_min,days_max) ;