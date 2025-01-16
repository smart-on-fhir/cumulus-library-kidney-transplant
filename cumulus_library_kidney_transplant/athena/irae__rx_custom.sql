create or replace view irae__rx_custom as 
 select 'rx_belatacept' as valueset, system, code, display from 
 irae__rx_belatacept
 UNION select 'rx_atg' as valueset, system, code, display from 
 irae__rx_atg
 UNION select 'rx_tacrolimus' as valueset, system, code, display from 
 irae__rx_tacrolimus
 UNION select 'rx_sirolimus' as valueset, system, code, display from 
 irae__rx_sirolimus
 UNION select 'rx_mycophenolate' as valueset, system, code, display from 
 irae__rx_mycophenolate
 UNION select 'rx_cyclosporin' as valueset, system, code, display from 
 irae__rx_cyclosporin
 UNION select 'rx_azathioprine' as valueset, system, code, display from 
 irae__rx_azathioprine