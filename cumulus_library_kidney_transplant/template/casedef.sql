create or replace view $prefix__casedef as
select distinct
    system,
    replace(code, '@', '')  as code,
    display,
    likely      = 'true'    as likely,
    preop       = 'true'    as preop,
    transplant  = 'true'    as transplant,
    rejection   = 'true'    as rejection,
    failure     = 'true'    as failure,
    outcome     = 'true'    as outcome,
    lab         = 'true'    as lab,
    imaging     = 'true'    as imaging
from $prefix__casedef_custom_csv;
