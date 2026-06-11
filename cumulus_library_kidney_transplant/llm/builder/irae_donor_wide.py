import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin


class IraeNlpDonorFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Donor",
    task_tabular_display="donor",
):
    pass