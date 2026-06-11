import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_highlights_mixin import IraeHighlightsMixin


class IraeNlpLongitudinalHighlightsBuilder(
    IraeHighlightsMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Longitudinal",
    task_tabular_display="longitudinal",
):
    pass
