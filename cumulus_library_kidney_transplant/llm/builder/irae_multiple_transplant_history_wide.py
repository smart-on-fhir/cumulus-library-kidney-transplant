import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_donor_wide import get_ctas_empty_query
from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin


class IraeNlpMultipleTransplantHistoryFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Multiple Transplant History",
    task_tabular_display="multiple_transplant_history",
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
                # Multiple Transplant History-specific columns
                'multiple_transplant_history',  
            ],
        )
