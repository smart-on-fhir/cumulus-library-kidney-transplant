import cumulus_library

from cumulus_library_kidney_transplant.llm.builder.irae_flattening_mixin import IraeFlatteningMixin


class IraeNlpImmunosuppressiveMedicationsFlattenedBuilder(
    IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display="Immunosuppressive Medications",
    task_tabular_display="immunosuppressive_medications",
):
    pass
