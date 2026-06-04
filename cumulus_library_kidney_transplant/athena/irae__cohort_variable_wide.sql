CREATE TABLE irae__cohort_variable_wide AS
with
select_wide_bool AS
(
    SELECT
            	IF(variable='lab_albumin', True) AS lab_albumin,
		IF(variable='lab_crp', True) AS lab_crp,
		IF(variable='lab_drug_level_azathioprine', True) AS lab_drug_level_azathioprine,
		IF(variable='lab_drug_level_cyclosporin', True) AS lab_drug_level_cyclosporin,
		IF(variable='lab_drug_level_mycophenolate', True) AS lab_drug_level_mycophenolate,
		IF(variable='lab_drug_level_sirolimus', True) AS lab_drug_level_sirolimus,
		IF(variable='lab_drug_level_tacrolimus', True) AS lab_drug_level_tacrolimus,
		IF(variable='lab_esr', True) AS lab_esr,
		IF(variable='lab_gfr_custom', True) AS lab_gfr_custom,
		IF(variable='lab_hla', True) AS lab_hla,
		IF(variable='lab_infection_viral_cmv', True) AS lab_infection_viral_cmv,
		IF(variable='lab_iron_ferritin', True) AS lab_iron_ferritin,
		IF(variable='lab_tpmt_gene', True) AS lab_tpmt_gene,
		IF(variable='rx_alemtuzumab', True) AS rx_alemtuzumab,
		IF(variable='rx_atg', True) AS rx_atg,
		IF(variable='rx_azathioprine', True) AS rx_azathioprine,
		IF(variable='rx_basiliximab', True) AS rx_basiliximab,
		IF(variable='rx_belatacept', True) AS rx_belatacept,
		IF(variable='rx_cyclosporin', True) AS rx_cyclosporin,
		IF(variable='rx_cytogam', True) AS rx_cytogam,
		IF(variable='rx_everolimus', True) AS rx_everolimus,
		IF(variable='rx_ig', True) AS rx_ig,
		IF(variable='rx_ivig', True) AS rx_ivig,
		IF(variable='rx_methylprednisolone', True) AS rx_methylprednisolone,
		IF(variable='rx_mycophenolate', True) AS rx_mycophenolate,
		IF(variable='rx_prednisolone', True) AS rx_prednisolone,
		IF(variable='rx_prednisone', True) AS rx_prednisone,
		IF(variable='rx_rituximab', True) AS rx_rituximab,
		IF(variable='rx_sirolimus', True) AS rx_sirolimus,
		IF(variable='rx_tacrolimus', True) AS rx_tacrolimus,
            encounter_ref
    FROM    irae__cohort_variable_union
),
select_wide_any AS
(
    SELECT
            	arbitrary(lab_albumin) FILTER (where lab_albumin ) as lab_albumin,
		arbitrary(lab_crp) FILTER (where lab_crp ) as lab_crp,
		arbitrary(lab_drug_level_azathioprine) FILTER (where lab_drug_level_azathioprine ) as lab_drug_level_azathioprine,
		arbitrary(lab_drug_level_cyclosporin) FILTER (where lab_drug_level_cyclosporin ) as lab_drug_level_cyclosporin,
		arbitrary(lab_drug_level_mycophenolate) FILTER (where lab_drug_level_mycophenolate ) as lab_drug_level_mycophenolate,
		arbitrary(lab_drug_level_sirolimus) FILTER (where lab_drug_level_sirolimus ) as lab_drug_level_sirolimus,
		arbitrary(lab_drug_level_tacrolimus) FILTER (where lab_drug_level_tacrolimus ) as lab_drug_level_tacrolimus,
		arbitrary(lab_esr) FILTER (where lab_esr ) as lab_esr,
		arbitrary(lab_gfr_custom) FILTER (where lab_gfr_custom ) as lab_gfr_custom,
		arbitrary(lab_hla) FILTER (where lab_hla ) as lab_hla,
		arbitrary(lab_infection_viral_cmv) FILTER (where lab_infection_viral_cmv ) as lab_infection_viral_cmv,
		arbitrary(lab_iron_ferritin) FILTER (where lab_iron_ferritin ) as lab_iron_ferritin,
		arbitrary(lab_tpmt_gene) FILTER (where lab_tpmt_gene ) as lab_tpmt_gene,
		arbitrary(rx_alemtuzumab) FILTER (where rx_alemtuzumab ) as rx_alemtuzumab,
		arbitrary(rx_atg) FILTER (where rx_atg ) as rx_atg,
		arbitrary(rx_azathioprine) FILTER (where rx_azathioprine ) as rx_azathioprine,
		arbitrary(rx_basiliximab) FILTER (where rx_basiliximab ) as rx_basiliximab,
		arbitrary(rx_belatacept) FILTER (where rx_belatacept ) as rx_belatacept,
		arbitrary(rx_cyclosporin) FILTER (where rx_cyclosporin ) as rx_cyclosporin,
		arbitrary(rx_cytogam) FILTER (where rx_cytogam ) as rx_cytogam,
		arbitrary(rx_everolimus) FILTER (where rx_everolimus ) as rx_everolimus,
		arbitrary(rx_ig) FILTER (where rx_ig ) as rx_ig,
		arbitrary(rx_ivig) FILTER (where rx_ivig ) as rx_ivig,
		arbitrary(rx_methylprednisolone) FILTER (where rx_methylprednisolone ) as rx_methylprednisolone,
		arbitrary(rx_mycophenolate) FILTER (where rx_mycophenolate ) as rx_mycophenolate,
		arbitrary(rx_prednisolone) FILTER (where rx_prednisolone ) as rx_prednisolone,
		arbitrary(rx_prednisone) FILTER (where rx_prednisone ) as rx_prednisone,
		arbitrary(rx_rituximab) FILTER (where rx_rituximab ) as rx_rituximab,
		arbitrary(rx_sirolimus) FILTER (where rx_sirolimus ) as rx_sirolimus,
		arbitrary(rx_tacrolimus) FILTER (where rx_tacrolimus ) as rx_tacrolimus,
            encounter_ref
    FROM    select_wide_bool
    GROUP BY encounter_ref
)
SELECT  DISTINCT
        select_wide_any.*
FROM    select_wide_any
;