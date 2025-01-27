WITH merged as
(
    select filename,ade,occurred from mike__irea_output_results_atg_short_list_v1           UNION
    select filename,ade,occurred from mike__irea_output_results_azathioprine_short_list_v1  UNION
    select filename,ade,occurred from mike__irea_output_results_cyclosporin_short_list_v1   UNION
    select filename,ade,occurred from mike__irea_output_results_mycophenolate_short_list_v1 UNION
    select filename,ade,occurred from mike__irea_output_results_sirolimus_short_list_v1     UNION
    select filename,ade,occurred from mike__irea_output_results_tacrolimus_short_list_v1
)
select
    SPLIT_PART(filename, '.', 1) AS subject_ref,
    SPLIT_PART(filename, '.', 2) AS doc_ref,
    ade,
    occurred
from merged
where occurred = True
