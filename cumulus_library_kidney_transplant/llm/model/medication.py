import json
import os
from enum import StrEnum

from pydantic import BaseModel, Field

from cumulus_library_kidney_transplant.llm.model.base import MedicationMention

##########################################################
#
#           Immunosuppression ** DRUG CLASS **
#
##########################################################

# ANTIMET: Anti-Metabolite (e.g., azathioprine, mycophenolate)
# CNI: Calcineurin Inhibitor (e.g., tacrolimus, cyclosporine)
# STEROID: Corticosteroid (e.g., prednisone, methylprednisolone)
# MTOR: mTOR Inhibitor (e.g., sirolimus, everolimus)
# COSTIM: Costimulation Blocker/blockade (e.g., belatacept)
# IVIG: Immunoglobulin (e.g., IVIG, Cytogam)
# POLYCLONAL: Polyclonal antibody (e.g., ATG, ALG)
# MONOCLONAL: Monoclonal antibody (mAb, e.g., basiliximab, rituximab)
# OTHER: Other immunosuppressive drug
# NONE: None of the above
class RxClassImmunosuppression(StrEnum):
    """
    Immunosuppressive drug class or therapy modality.
    """
    ANTIMET = "ANTIMET"
    CNI = "CNI"
    STEROID = "STEROID"
    MTOR = "MTOR"
    COSTIM = "COSTIM"
    IVIG = "IVIG"
    POLYCLONAL = "POLYCLONAL"
    MONOCLONAL = "MONOCLONAL"
    OTHER = "OTHER"
    NONE = "NONE"



# ANTIMET group: AZA=Azathioprine, MMF=Mycophenolate Mofetil, ANTIMET_OTHER=Other anti-metabolite
# CNI group: CYA=Cyclosporine, TAC=Tacrolimus, CNI_OTHER=Other calcineurin inhibitor
# STEROID group: MEDROL=Methylprednisolone, PDL=Prednisolone, PRED=Prednisone, STEROID_OTHER=Other corticosteroid
# COSTIM group: BEL=Belatacept, ABA=Abatacept, COSTIM_OTHER=Other costimulation blocker
# IVIG group: IVIG=Intravenous Immunoglobulin, CYTOGAM=Cytogam (CMV-specific hyperimmune globulin), IVIG_OTHER=Other immunoglobulin
# MTOR group: EVE=Everolimus, SRL=Sirolimus, MTOR_OTHER=Other mTOR inhibitor
# MONOCLONAL group: ALEM=Alemtuzumab, BASI=Basiliximab, DAC=Daclizumab, RTX=Rituximab, MONOCLONAL_OTHER=Other monoclonal antibody
# POLYCLONAL group: ATG=Antithymocyte Globulin, POLYCLONAL_OTHER=Other polyclonal antibody
# NONE: None of the above
class RxIngredientImmunosuppression(StrEnum):
    """
    The specific immunosuppressive drug ingredient.
    """

    # ANTIMET Types
    AZA = "AZA"
    MMF = "MMF"
    ANTIMET_OTHER = "ANTIMET_OTHER"
    # CNI Types
    CYA = "CYA"
    TAC = "TAC"
    CNI_OTHER = "CNI_OTHER"
    # STEROID Types
    MEDROL = "MEDROL"
    PDL = "PDL"
    PRED = "PRED"
    STEROID_OTHER = "STEROID_OTHER"
    # COSTIM Types
    BEL = "BEL"
    ABA = "ABA"
    COSTIM_OTHER = "COSTIM_OTHER"
    # IVIG Types
    IVIG = "IVIG"
    CYTOGAM = "CYTOGAM"
    IVIG_OTHER = "IVIG_OTHER"
    # MTOR Types
    EVE = "EVE"
    SRL = "SRL"
    MTOR_OTHER = "MTOR_OTHER"
    # MONOCLONAL Types
    ALEM = "ALEM"
    BASI = "BASI"
    DAC = "DAC"
    RTX = "RTX"
    MONOCLONAL_OTHER = "MONOCLONAL_OTHER"
    # POLYCLONAL Types
    ATG = "ATG"
    POLYCLONAL_OTHER = "POLYCLONAL_OTHER"
    NONE = "NONE"



class ImmunosuppressiveMedicationMention(MedicationMention):
    """
    Mentions of ImmunosuppressiveMedications for this given chart.
    """

    drug_class: RxClassImmunosuppression = Field(
        default=RxClassImmunosuppression.NONE,
        description=(
            "Extract the Immunosuppressive drug class or therapy modality documented for this medication, if present. "
            "ANTIMET: Anti-Metabolite (e.g., azathioprine, mycophenolate); "
            "CNI: Calcineurin Inhibitor (e.g., tacrolimus, cyclosporine); "
            "STEROID: Corticosteroid (e.g., prednisone, methylprednisolone); "
            "MTOR: mTOR Inhibitor (e.g., sirolimus, everolimus); "
            "COSTIM: Costimulation Blocker/blockade (e.g., belatacept); "
            "IVIG: Immunoglobulin (e.g., IVIG, Cytogam); "
            "POLYCLONAL: Polyclonal antibody (e.g., ATG, ALG); "
            "MONOCLONAL: Monoclonal antibody (e.g., basiliximab, rituximab); "
            "OTHER: Other immunosuppressive drug; "
            "NONE: None of the above"
        ),
    )

    ingredient: RxIngredientImmunosuppression = Field(
        default=RxIngredientImmunosuppression.NONE,
        description=(
            "Extract the specific immunosuppressive drug ingredient documented for this medication, if present. "
            "ANTIMET group: AZA=Azathioprine, MMF=Mycophenolate Mofetil, ANTIMET_OTHER=other anti-metabolite; "
            "CNI group: CYA=Cyclosporine, TAC=Tacrolimus, CNI_OTHER=other calcineurin inhibitor; "
            "STEROID group: MEDROL=Methylprednisolone, PDL=Prednisolone, PRED=Prednisone, STEROID_OTHER=other corticosteroid; "
            "COSTIM group: BEL=Belatacept, ABA=Abatacept, COSTIM_OTHER=other costimulation blocker; "
            "IVIG group: IVIG=Intravenous Immunoglobulin, CYTOGAM=Cytogam (CMV-specific hyperimmune globulin), IVIG_OTHER=other immunoglobulin; "
            "MTOR group: EVE=Everolimus, SRL=Sirolimus, MTOR_OTHER=other mTOR inhibitor; "
            "MONOCLONAL group: ALEM=Alemtuzumab, BASI=Basiliximab, DAC=Daclizumab, RTX=Rituximab, MONOCLONAL_OTHER=other monoclonal antibody; "
            "POLYCLONAL group: ATG=Antithymocyte Globulin, POLYCLONAL_OTHER=other polyclonal antibody; "
            "NONE: None of the above"
        ),
    )


##############################################################################
# Aggregated Annotation and Mention Classes
#
# This is the top-level structure for the pydantic models used in IRAE tasks.
###############################################################################


class ImmunosuppressiveMedicationsAnnotation(BaseModel):
    """
    All mentions of ImmunosuppressiveMedications for this given chart.
    """

    immunosuppressive_medication_mentions: list[ImmunosuppressiveMedicationMention] = Field(
        default_factory=list,
        description="All mentions of ImmunosuppressiveMedications for this given chart.",
    )
