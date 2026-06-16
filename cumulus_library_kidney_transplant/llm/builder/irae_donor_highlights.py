import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_highlights_mixin import IraeHighlightsMixin


class IraeNlpDonorHighlightsBuilder(
    IraeHighlightsMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Donor",
    task_tabular_display="donor",
):
    pass