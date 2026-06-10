from pathlib import Path
from cumulus_library_kidney_transplant import filetool

def make() -> list[Path]:
    """
    :return: list of target Paths to append to `manifest.toml`
    """
    highlights_dir = filetool.path_home() / 'nlp_result_to_highlights'
    return [
        highlights_dir / 'builder_irae_highlights_immunosuppressive_medications.py',
        highlights_dir / 'builder_irae_highlights_multiple_transplant_history.py',
        highlights_dir / 'builder_irae_highlights_donor.py',
        highlights_dir / 'builder_irae_highlights_longitudinal.py'
    ]