import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin
from cumulus_library_kidney_transplant.llm.builder.irae_highlights_mixin import get_ctas_empty_query


class IraeNlpDonorFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Donor",
    task_tabular_display="donor",
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
                # Donor-specific columns
                'donor_transplant_date',
                'donor_type',
                'donor_relationship',
                'donor_hla_match_quality',
                'donor_hla_mismatch_count',
                'donor_serostatus',
                'donor_serostatus_cmv',
                'donor_serostatus_ebv',
                'recipient_serostatus',
                'recipient_serostatus_cmv',
                'recipient_serostatus_ebv',
            ],
        )