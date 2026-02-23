import argparse
import csv
import re
from pathlib import Path
from typing import Iterable

def parse_keyword_tsv(tsv_path: Path) -> tuple[dict[str, dict], list[str]]:
    """
    Parse a keyword-mapping TSV 
    returns the keyword lookup dict and the variables of interest 
    """
    tsv_path = Path(tsv_path)
    tsv = tsv_path.open()
    reader = csv.reader(tsv, delimiter="\t")
    rows = list(reader)

    if not rows:
        return {}, []

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

    return lookup, variable_names


def file_friendly_variable_name(variable: str) -> str:
    """
    Variables as file-friendly slugs
    """
    return variable.strip().lower().replace(" ", "-").replace("_", "-")


def space_friendly_variable_name(variable: str) -> str:
    """
    Variable names as human-readable strings
    """
    return variable.strip().replace("-", " ").replace("_", " ")


def get_keywords_for_variable(lookup: dict, variable_name: str) -> list[str]:
    """
    Extract all keywords for a variable from our lookup
    """
    keywords = []
    for group in lookup.values():
        if variable_name in group["relevant variables"]:
            keywords.extend(group["keywords"])
    return keywords


def generate_select_by_keyword_lines(keywords: Iterable[str]) -> str:
    """
    Generate the --select-by-word and --select-by-regex based on keywords
    """
    keyword_lines = []
    if not keywords:
        return ""
    for kw in keywords:
        if kw.startswith('REGEX:'):
            regex_pattern = re.compile(kw.split('REGEX:')[1].strip()).pattern
            keyword_lines.append(f'--select-by-regex "{regex_pattern}" \\')
        else:
            keyword_lines.append(f'--select-by-word "{kw}" \\')

    return "\n  ".join(keyword_lines)


def get_keyword_patterns(keyword_set: Iterable[str]) -> list[str]:
    """
    Given a set of keywords, some of which may be regexes (marked with "REGEX:"),
    return a list of patterns where regexes are compiled and keywords are escaped.
    """
    # Parse Regex patterns as regexes, but escape all other keywords 
    patterns = []
    for kw in keyword_set:
        if kw.startswith('REGEX:'):
            patterns.append(re.compile(kw.split('REGEX:')[1].strip()).pattern)
        else:
            patterns.append(re.escape(kw))
    return patterns


def generate_exclusion_regex(patterns: list[str]) -> re.Pattern:
    """
    Combines multiple keywords/regexes into a single regex that 
    only matches if NONE of the patterns are present.
    """
    # Join patterns with a logical OR (|)
    edge = r"\b"
    patterns.sort()
    combined_patterns = "|".join(f"{edge}{p}{edge}" for p in patterns)

    # Combine with negative lookahead 
    # using .*$ at the end causes a catastrophic backtracking problem
    return re.compile(rf"^(?!.*(?:{combined_patterns}))")


def make_negation_regex(keyword_lookup: dict[str, dict]) -> re.Pattern:
    """
    Generate a single regex pattern that matches only if none of the keywords (or regexes) 
    are matched
    """
    keyword_set = set()
    for keyword_group in keyword_lookup.values(): 
        keyword_set.update(set(keyword_group['keywords']))
    
    keyword_patterns = get_keyword_patterns(keyword_set)
    return generate_exclusion_regex(keyword_patterns)


def render_sample_script(variable: str, keywords: list[str], source_table: str) -> str:
  """
  For a given variable and its related keywords, render a sample command script that uses those keywords in the --select-by-word and --select-by-regex flags. 

  TODO: Make things like seed, count, etc configurable 
  """
  human_readable_var = space_friendly_variable_name(variable)
  file_variable = file_friendly_variable_name(variable)
  select_by_lines = generate_select_by_keyword_lines(keywords)
  return f'''#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# {human_readable_var}
echo "{human_readable_var}"
docker compose run --rm -it \\
  cumulus-etl sample \\
  $SAMPLE_INPUT_FOLDER \\
  --output ./samples/{file_variable}.csv\\
  --export-to ./samples/{file_variable}/\\
  --count 30 \\
  --seed 07201869 \\
  --columns "note,subject,encounter" \\
  --phi-dir $SAMPLE_PHI_DIR \\
  --athena-database $SAMPLE_ATHENA_DB  \\
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \\
  --athena-region $SAMPLE_ATHENA_REGION \\
  {select_by_lines}
  --select-by-athena-table {source_table} \\
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
'''

def define_parser(): 
    """
    Set up our parser for generating sample commands based on a keyword TSV. 
    """
    parser = argparse.ArgumentParser(
        description="Generate cumulus-etl sample shell scripts from a keyword TSV."
    )
    parser.add_argument(
        "--variable_keyword_path",
        type=Path,
        default=Path(__file__).parent / "keywords.tsv",
        help="Path to the variable-keyword mapping TSV (default: %(default)s)",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path(__file__).parent / "../../docs/variable_sample_commands",
        help="Directory to write sample shell scripts into (default: %(default)s)",
    )
    parser.add_argument(
        "--source_table",
        default="irae__sample_casedef_peri",
        help="Athena source table passed to --select-by-athena-table (default: %(default)s)",
    )
    parser.add_argument(
        "--include-unmatched",
        action="store_true",
        default=False,
        help="Also write a script for notes that match none of the keywords (default: %(default)s)",
    )
    return parser

def main():
    parser = define_parser()
    args = parser.parse_args()

    variable_keyword_path = args.variable_keyword_path
    output_dir = args.output_dir
    source_table = args.source_table
    include_unmatched = args.include_unmatched

    keyword_lookup, variables = parse_keyword_tsv(variable_keyword_path)
    for variable in variables:
        keywords = get_keywords_for_variable(keyword_lookup, variable)
        script = render_sample_script(variable, keywords, source_table)
        slug = file_friendly_variable_name(variable)
        (output_dir / f"sample-{slug}.sh").write_text(script)
    if include_unmatched:
        # uses the full keyword set → negation regex
        negation_regex = f"REGEX: {make_negation_regex(keyword_lookup).pattern}"
        unmatched_variable = 'Other Notes'
        unmatched_script = render_sample_script(unmatched_variable, [negation_regex], source_table)
        slug = file_friendly_variable_name(unmatched_variable)
        (output_dir / f"sample-{slug}.sh").write_text(unmatched_script)



if __name__ == "__main__":
    main()