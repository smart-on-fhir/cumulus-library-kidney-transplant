import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin


class IraeNlpLongitudinalFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Longitudinal",
    task_tabular_display="longitudinal",
):
    pass
