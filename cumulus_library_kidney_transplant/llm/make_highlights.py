from pathlib import Path
from cumulus_library_kidney_transplant.tools import filetool

def make() -> list[Path]:
    """
    :return: list of target Paths to append to `manifest.toml`
    """
    return [
        filetool.path_llm_builder('irae_highlights_immunosuppressive_medications.py'),
        filetool.path_llm_builder('irae_highlights_multiple_transplant_history.py'),
        filetool.path_llm_builder('irae_highlights_donor.py'),
        filetool.path_llm_builder('irae_highlights_longitudinal.py'),
    ]

if __name__ == "__main__":
    for path in make():
        print(f"Created {path.relative_to(Path.cwd())}")
