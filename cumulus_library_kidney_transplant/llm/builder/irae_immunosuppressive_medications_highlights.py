import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_highlights_mixin import IraeHighlightsMixin


class IraeNlpImmunosuppressiveMedicationsHighlightsBuilder(
    IraeHighlightsMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Immunosuppressive Medications",
    task_tabular_display="immunosuppressive_medications",
):
    pass
