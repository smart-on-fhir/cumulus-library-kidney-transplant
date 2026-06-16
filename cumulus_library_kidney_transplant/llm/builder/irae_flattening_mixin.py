from cumulus_library_kidney_transplant.llm.builder.irae_base_mixin import IraeLLMBaseMixin


class IraeFlatteningMixin(IraeLLMBaseMixin):
    """Mixin providing shared flattening logic for IRAE wide-table builders.

    Combine with cumulus_library.BaseTableBuilder to create a concrete builder:

        class MyBuilder(
            cumulus_library.BaseTableBuilder,
            IraeFlatteningMixin,
            task_display="My Task",
            task_tabular_display="my_task",
        ):
            def _make_empty_query(self, config):
                ...
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(task_table_suffix='wide', **kwargs)