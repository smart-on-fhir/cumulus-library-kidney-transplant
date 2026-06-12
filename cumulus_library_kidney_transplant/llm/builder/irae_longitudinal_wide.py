import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin
from cumulus_library_kidney_transplant.llm.builder.irae_highlights_mixin import get_ctas_empty_query


class IraeNlpLongitudinalFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Longitudinal",
    task_tabular_display="longitudinal",
):
    def _make_empty_query(self, config: cumulus_library.StudyConfig):
        """
        Creates an empty query for the highlights table.
        Since all highlights tables have a common flat format, 
        we can use common series of table_cols to create the empty query.
        """
        return get_ctas_empty_query(
            schema_name=config.schema,
            table_name=self.dest_table,
            table_cols=[
                'note_ref',
                'subject_ref',
                'generated_on',
                'task_version',
                'system_fingerprint',
                'origin',
                # Longitudinal-variable-specific columns
                'rx_therapeutic_status',
                'rx_compliance',
                'dsa_history',
                'dsa',
                'infection_history',
                'infection',
                'viral_infection_history',
                'viral_infection',
                'bacterial_infection_history',
                'bacterial_infection',
                'fungal_infection_history',
                'fungal_infection',
                'graft_rejection_history',
                'graft_rejection',
                'graft_failure_history',
                'graft_failure',
                'ptld_history',
                'ptld',
                'cancer_history',
                'cancer',
                'deceased',
                'deceased_date',
            ],
        )