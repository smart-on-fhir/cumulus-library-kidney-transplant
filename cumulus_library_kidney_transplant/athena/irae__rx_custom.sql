create or replace view irae__rx_custom as 
 select 'rx_sirolimus' as subtype, system, code, display from 
 irae__rx_sirolimus
 UNION select 'rx_belatacept' as subtype, system, code, display from 
 irae__rx_belatacept
 UNION select 'rx_atg' as subtype, system, code, display from 
 irae__rx_atg
 UNION select 'rx_tacrolimus' as subtype, system, code, display from 
 irae__rx_tacrolimus
 UNION select 'rx_cyclosporin' as subtype, system, code, display from 
 irae__rx_cyclosporin
 UNION select 'rx_mycophenolate' as subtype, system, code, display from 
 irae__rx_mycophenolate
 UNION select 'rx_azathioprine' as subtype, system, code, display from 
 irae__rx_azathioprine