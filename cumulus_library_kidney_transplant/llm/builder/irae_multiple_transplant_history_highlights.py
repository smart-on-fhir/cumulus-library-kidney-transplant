import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_highlights_mixin import IraeHighlightsMixin


class IraeNlpMultipleTransplantHistoryHighlightsBuilder(
    IraeHighlightsMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Multiple Transplant History",
    task_tabular_display="multiple_transplant_history",
):
    pass
