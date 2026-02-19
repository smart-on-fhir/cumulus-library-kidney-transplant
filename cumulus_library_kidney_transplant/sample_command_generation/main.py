import csv
import re
import sys
from pathlib import Path

def parse_keyword_tsv(tsv_path: Path) -> dict[str, dict]:
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

def generate_exclusion_regex(patterns):
    """
    Combines multiple keywords/regexes into a single regex that 
    only matches if NONE of the patterns are present.
    """
    # Join patterns with a logical OR (|)
    edge = r"\b"
    combined_patterns = "|".join(f"{edge}{p}{edge}" for p in patterns)

    # Combine with negative lookahead 
    # using .*$ at the end causes a catastrophic backtracking problem
    return re.compile(rf"^(?!.*(?:{combined_patterns}))")

def get_exclusion_patterns(keyword_set: set):
    # Escape patterns 
    patterns = []
    for k in keyword_set:
        if k.startswith('REGEX:'):
            patterns.append(re.compile(k.split('REGEX:')[1].strip()).pattern)
        else:
            patterns.append(re.escape(k))
    return patterns

def make_negation_regex(keyword_path: Path):
    keyword_lookup = parse_keyword_tsv(keyword_path)
    keyword_set = set()
    for keyword_group in keyword_lookup.values(): 
        keyword_set.update(set(keyword_group['keywords']))
    
    # --- Example Usage ---
    keywords_and_regexes = get_exclusion_patterns(keyword_set)
    master_regex = generate_exclusion_regex(keywords_and_regexes)
    print(f"Generated Regex: {master_regex}\n")
    
    # Write the master_regex to a file in the same directory as this script
    script_dir = Path(__file__).parent
    output_file = script_dir / "negation_regex.txt"
    with open(output_file, "w") as f:
        f.write(master_regex.pattern)
    
    print(f"Regex written to {output_file}")

if __name__ == "__main__":
    keyword_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / 'keywords.tsv'
    make_negation_regex(keyword_path)
