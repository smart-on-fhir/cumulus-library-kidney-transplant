from pathlib import Path
from cumulus_library_kidney_transplant.tools.tablespace import name_cube
from cumulus_library_kidney_transplant.tools.cube import (
    cube_patient,
    cube_encounter,
)

def make_llm() -> list[Path]:
    """
    TODO: requires modernizing with LLM but the overall columns and approach holds.
    :return: list of paths for LLM result cubes
    """
    return [
        cube_patient(source_table='irae__gpt4_donor',
                     table_cols=['donor_type_best',
                                 'donor_relationship_best',
                                 'doc_type_display',
                                 'donor_date_best_year',
                                 'donor_hla_quality',
                                 'age_at_visit', 'gender', 'race_display'],
                     table_name=name_cube('patient_llm_donor')),
    
        cube_encounter(source_table='irae__gpt4_compliance',
                       table_cols=['rx_compliance_status',
                                   'rx_therapeutic_level',
                                   'rx_therapeutic_sub',
                                   'rx_therapeutic_supra',
                                   'rx_compliance_level',
                                   'rx_compliance_partial',
                                   'rx_compliance_non',
                                   'age_at_visit'],
                       table_name=name_cube('encounter_llm_compliance')),
    
        cube_patient(source_table='irae__gpt4_infection',
                     table_cols=['infection_history',
                                 'infection_present',
                                 'confidence', 'present_type', 'present_type_any',
                                 'viral_present',
                                 'bacterial_present',
                                 'fungal_present',
                                 'age_at_visit', 'gender', 'race_display'],
                     table_name=name_cube('patient_llm_infection')),
    
        cube_patient(source_table='irae__gpt4_infection_outcome',
                     table_cols=['rx_compliance_status',
                                 'rx_therapeutic_supra',
                                 'infection_type',
                                 'infection_confidence',
                                 'rejection_patient',
                                 'failure_patient'],
                     table_name=name_cube('patient_infection_outcome')),
    
        cube_patient(source_table='irae__gpt4_rejection',
                     table_cols=['rejection_encounter',
                                 'rejection_patient',
                                 'failure_present',
                                 'failure_history',
                                 'age_at_visit',
                                 'gender',
                                 'race_display'],
                     table_name=name_cube('patient_llm_rejection')),
        ]
    
if __name__ == "__main__":
    llm_target_files = make_llm()
    print(llm_target_files)
