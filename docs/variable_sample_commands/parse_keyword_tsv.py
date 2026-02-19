import csv
import json
import re
import sys
from pathlib import Path


def parse_keyword_tsv(tsv_path: str | Path) -> dict[str, dict]:
    """
    Parse a keyword-mapping TSV and return the variable-lookup dict
    """
    tsv_path = Path(tsv_path)
    tsv = tsv_path.open()
    reader = csv.reader(tsv, delimiter="\t")
    rows = list(reader)

    if not rows:
        return {}

    # Row 0: column headers (but skip the first cell "Link to Variables")
    variable_names = rows[0][1:]

    lookup = {}

    # Each row is a conceptual group of keywords, marking which variables these keywords 
    # are related to
    for row in rows[1:]:
        # safety in case we have a blank row or no keywords for this row
        if not row or not row[0].strip():
            continue

        # First cell in a row describes all the relevant keywords for this group
        keyword_cell = row[0]
        relevance_cells = row[1:]

        # Each line in the first cell is one keyword (strip surrounding space; None otherwise)
        keywords = [
            kw.strip() 
            for kw in keyword_cell.splitlines() 
            if kw.strip()
        ]
        if not keywords:
            continue

        # Track which variables are relevant for this 
        relevant_vars = [
            variable_names[i] 
            for i, cell in enumerate(relevance_cells)
            if i < len(variable_names) and cell.strip().upper() == "X"
        ]

        lookup[keywords[0]] = {
            "keywords": keywords,
            "relevant variables": relevant_vars,
        }

    return lookup


if __name__ == "__main__":
    default_tsv = Path(__file__).parent / "keywords.tsv"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_tsv
    print(json.dumps(parse_keyword_tsv(path), indent=2))
