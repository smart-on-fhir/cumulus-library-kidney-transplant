import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin


class IraeNlpMultipleTransplantHistoryFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Multiple Transplant History",
    task_tabular_display="multiple_transplant_history",
):
    pass
