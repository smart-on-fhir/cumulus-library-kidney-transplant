import re
import json
from pathlib import Path

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

def make_negation_regex():
    keyword_lookup_path = Path(__file__).parent / 'keyword_lookup.json'
    keyword_lookup = json.load(keyword_lookup_path.open())
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
    make_negation_regex()
