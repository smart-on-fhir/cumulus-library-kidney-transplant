from pathlib import Path
from cumulus_library_kidney_transplant.tools import tablespace
from cumulus_library_kidney_transplant.tools.cube import (
    cube_patient,
    cube_note
)

def make_llm() -> list[Path]:
    return []

if __name__ == "__main__":
    llm_target_files = make_llm()
    print(llm_target_files)
