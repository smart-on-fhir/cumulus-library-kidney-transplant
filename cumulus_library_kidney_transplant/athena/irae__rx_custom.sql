create or replace view irae__rx_custom as 
 select 'rx_rx_alemtuzumab' as valueset, system, code, display from 
 irae__rx_rx_alemtuzumab
 UNION ALL
select 'rx_rx_atg' as valueset, system, code, display from 
 irae__rx_rx_atg
 UNION ALL
select 'rx_rx_azathioprine' as valueset, system, code, display from 
 irae__rx_rx_azathioprine
 UNION ALL
select 'rx_rx_basiliximab' as valueset, system, code, display from 
 irae__rx_rx_basiliximab
 UNION ALL
select 'rx_rx_belatacept' as valueset, system, code, display from 
 irae__rx_rx_belatacept
 UNION ALL
select 'rx_rx_cyclosporin' as valueset, system, code, display from 
 irae__rx_rx_cyclosporin
 UNION ALL
select 'rx_rx_cytogam' as valueset, system, code, display from 
 irae__rx_rx_cytogam
 UNION ALL
select 'rx_rx_everolimus' as valueset, system, code, display from 
 irae__rx_rx_everolimus
 UNION ALL
select 'rx_rx_ig' as valueset, system, code, display from 
 irae__rx_rx_ig
 UNION ALL
select 'rx_rx_ivig' as valueset, system, code, display from 
 irae__rx_rx_ivig
 UNION ALL
select 'rx_rx_methylprednisolone' as valueset, system, code, display from 
 irae__rx_rx_methylprednisolone
 UNION ALL
select 'rx_rx_mycophenolate' as valueset, system, code, display from 
 irae__rx_rx_mycophenolate
 UNION ALL
select 'rx_rx_prednisolone' as valueset, system, code, display from 
 irae__rx_rx_prednisolone
 UNION ALL
select 'rx_rx_prednisone' as valueset, system, code, display from 
 irae__rx_rx_prednisone
 UNION ALL
select 'rx_rx_rituximab' as valueset, system, code, display from 
 irae__rx_rx_rituximab
 UNION ALL
select 'rx_rx_sirolimus' as valueset, system, code, display from 
 irae__rx_rx_sirolimus
 UNION ALL
select 'rx_rx_tacrolimus' as valueset, system, code, display from 
 irae__rx_rx_tacrolimus