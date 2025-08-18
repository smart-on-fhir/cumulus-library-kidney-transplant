create or replace view irae__rx_custom as 
 select 'rx_sirolimus' as valueset, system, code, display from 
 irae__rx_sirolimus
 UNION select 'rx_methylprednisolone' as valueset, system, code, display from 
 irae__rx_methylprednisolone
 UNION select 'rx_everolimus' as valueset, system, code, display from 
 irae__rx_everolimus
 UNION select 'rx_azathioprine' as valueset, system, code, display from 
 irae__rx_azathioprine
 UNION select 'rx_atg' as valueset, system, code, display from 
 irae__rx_atg
 UNION select 'rx_cytogam' as valueset, system, code, display from 
 irae__rx_cytogam
 UNION select 'rx_prednisolone' as valueset, system, code, display from 
 irae__rx_prednisolone
 UNION select 'rx_belatacept' as valueset, system, code, display from 
 irae__rx_belatacept
 UNION select 'rx_ig' as valueset, system, code, display from 
 irae__rx_ig
 UNION select 'rx_tacrolimus' as valueset, system, code, display from 
 irae__rx_tacrolimus
 UNION select 'rx_basiliximab' as valueset, system, code, display from 
 irae__rx_basiliximab
 UNION select 'rx_mycophenolate' as valueset, system, code, display from 
 irae__rx_mycophenolate
 UNION select 'rx_rituximab' as valueset, system, code, display from 
 irae__rx_rituximab
 UNION select 'rx_alemtuzumab' as valueset, system, code, display from 
 irae__rx_alemtuzumab
 UNION select 'rx_cyclosporin' as valueset, system, code, display from 
 irae__rx_cyclosporin
 UNION select 'rx_prednisone' as valueset, system, code, display from 
 irae__rx_prednisone
 UNION select 'rx_ivig' as valueset, system, code, display from 
 irae__rx_ivig