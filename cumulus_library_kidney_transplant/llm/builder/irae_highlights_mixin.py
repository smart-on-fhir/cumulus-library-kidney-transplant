import cumulus_library
from cumulus_library.template_sql.base_templates import get_ctas_empty_query

from cumulus_library_kidney_transplant.llm.builder.irae_base_mixin import IraeLLMBaseMixin


class IraeHighlightsMixin(IraeLLMBaseMixin):
    """Mixin providing span-highlight creation logic for IRAE.

    Combine with cumulus_library.BaseTableBuilder to create a concrete builder:

        class MyBuilder(
            cumulus_library.BaseTableBuilder,
            IraeHighlightsMixin,
            task_display="My Task",
            task_tabular_display="my_task",
        ):
            pass
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(task_table_suffix='highlights', **kwargs)

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
                'label',
                'span',
                'sublabel_name',
                'sublabel_value'
            ],
        )
