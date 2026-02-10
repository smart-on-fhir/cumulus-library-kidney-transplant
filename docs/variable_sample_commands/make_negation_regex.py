import re
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

def get_exclusion_patterns():
    keywords = [
        ###################
        # Donor Relationship 
        "KDIGO",
        "Related Donor",
        "Familial donor",
        "Family donor",
        "Sibling donor",
        "Parent donor",
        "Mother donor",
        "Father donor",
        "Child donor",
        "Brother donor",
        "Sister donor",
        "Unrelated donor",
        "directed donor",
        "altruistic donor",
        "good samaritan donor",
        "anonymous donor",
        "volunteer donor",
        "NDD",
        "non directed donor",
        "non-directed donor",
        "nondirected donor",
        "LRD",
        "LRRT",
        "living related donor",
        "living relative",
        "LURD",
        "living unrelated donor",
        ###################
        # Donor Sero CMV 
        "Recipient",
        "Transplant",
        "Donor",
        "Donation",
        "Organ",
        "donor serostatus",
        "D+",
        "D +",
        "D(+)",
        "D (+)",
        "D-pos",
        "Donor pos",
        "Donor+",
        "Donor +",
        "Donor(+)",
        "Donor (+)",
        "Donor reactive",
        "Donor-positive",
        "D-",
        "D -",
        "D(-)",
        "D (-)",
        "D-neg",
        "Donor neg",
        "Donor-",
        "Donor -",
        "Donor(-)",
        "Donor (-)",
        "Donor nonreactive",
        "Donor-negative",
        "serostatus",
        "seropositive",
        "seropositivity",
        "IgG positive",
        "reactive",
        "antibody detected",
        "seronegative",
        "seronegativity",
        "IgG negative",
        "non-reactive",
        "no antibodies detected",
        "serology",
        "viral status",
        "titer",
        "screen",
        "NAT",
        "nucleic acid test",
        "PCR",
        "viral load",
        "Ig markers",
        "IgG",
        "IgM",
        "Total Ab",
        "Antibody",
        "Ab",
        "Cytomegalovirus",
        "CMV",
        "CMV+",
        "CMV-",
        ###################
        # Unique Donor Serostatus EBV
        "Epstein-Barr",
        "Epstein",
        "EBV",
        "EBV+",
        ###################
        # Unique Donor Status
        "Living Donor",
        "Living Kidney",
        "Living Renal",
        "Live Donor",
        "Live Renal",
        "Live Kidney",
        "LDRT",
        "Deceased Donor",
        "Deceased Kidney",
        "Deceased Renal",
        "Deceased Organ",
        "Heart beating",
        "Beating heart",
        "Brain dead",
        "Brain-dead",
        "Cadaveric",
        "cadaver",
        "DD donor",
        "DD kidney",
        "DD renal",
        "Renal DD",
        "Kidney DD",
        ###################
        # Unique HLA Mismatch
        "HLA",
        "human leukocyte antigen",
        "antigen matched",
        "antigen matches",
        "antigen match",
        "mismatch",
        "mismatches",
        "mismatched",
        "well matched",
        "good match",
        "excellent match",
        "excellently matched",
        "favorable match",
        "favorably matched",
        "close match",
        "closely matched",
        "fully matched",
        "fully matches",
        "full match",
        "complete match",
        "completely matched",
        "perfect match",
        "perfectly matched",
        "identical match",
        "identically matched",
        "moderately matched",
        "moderate match",
        "partial match",
        "partially match",
        "intermediate match",
        "acceptable match",
        "acceptably matched",
        "suitable match",
        "compatible match",
        "poorly matched",
        "poor match",
        "weak match",
        "weakly matched",
        "high mismatch",
        "highly mismatched",
        "unfavorable match",
        "unfavorably matched",
        "DSA",
        "DSAs",
        "Donor specific",
        ###################
        # Unique HLA Mismatch
        "HLA Quality",
        "Highly Sensitized",
        "Alloimmunized",
        "Desensitization",
        "Desensitized",
        ###################
        # Unique Recipient Serostatus
        "recipient serostatus",
        "R+",
        "R +",
        "R(+)",
        "R (+)",
        "R-pos",
        "Recip pos",
        "Recip+",
        "Recip +",
        "Recip(+)",
        "Recip (+)",
        "Recipient reactive",
        "Recip-positive",
        "R-",
        "R -",
        "R(-)",
        "R (-)",
        "R-neg",
        "Recip neg",
        "Recip-",
        "Recip -",
        "Recip(-)",
        "Recip (-)",
        "Recipient nonreactive",
        "Recip-negative",
        ###################
        # Unique Transplant Date
        "Transplant Date" ,
        "transplanted on",
        "POD",
        "transplant on" ,
        re.compile(r"now day\s*\+?\d+"),
        re.compile(r"transplant\s*\(?\d+\s*/\s*\d+\)?"),
        ###################
        # Avoid Noise from 
        # Unprocessed Note Text 
        "OperationOutcome",
    ]
    
    # Escape patterns 
    patterns = []
    for k in keywords:
        if isinstance(k, re.Pattern):
            patterns.append(k.pattern)
        else:
            patterns.append(re.escape(k))
    return patterns

def make_negation_regex():
    # --- Example Usage ---
    keywords_and_regexes = get_exclusion_patterns()
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
