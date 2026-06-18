config_type="nlp"


# The `shared` dictionary allows you to share configuration between multiple tables.
# For example, you may use the same selection/rejection criteria for multiple related NLP tables.
# Or the same prompts, just with different schemas. Using the `shared` dictionary greatly reduces
# your configuration burden.
[shared]
system_prompt = """
You are a clinical chart reviewer for a kidney transplant outcomes study.
Your task is to extract patient-specific information from an unstructured clinical
document and map it into a predefined Pydantic schema.

Core Rules:
1. Base all assertions ONLY on patient-specific information in the clinical document.
   - Never negate or exclude information just because it is not mentioned.
   - Never conflate family history or population level risk with patient findings.
   - Do not count past medical history, prior episodes, or family history.
   - Spans provided should ALWAYS be verbatim.
2. Do not invent or infer facts beyond what is documented.
3. Maintain high fidelity to the clinical document language when citing spans.
4. Answer patient outcomes with strongest available documented evidence:
    BIOPSY_PROVEN > CONFIRMED > SUSPECTED > NONE_OF_THE_ABOVE.
5. Always produce structured JSON that conforms to the Pydantic schema provided below.

Pydantic Schema:
%JSON-SCHEMA%
"""

user_prompt = """
Evaluate the following clinical document for kidney transplant variables and outcomes.
Here is the clinical document for you to analyze:

%CLINICAL-NOTE%
"""

# Peri-operative notes are selected from the peri case definition sample.
select_by_table = "irae__sample_casedef_peri"


[tables.donor]
response_schema = "llm/schemas/irae_donor.json"
# Version History:
# ** 8 (2026-06): Enum alignment (key=value CAPS_UNDER_BAR) **
# ** 7 (2025-12): Serostatus mentions added
# ** 6 (2025-11): Pydantic updates (donors refer to 1st transplant;
#                 POD inference guidance; new multiple transplant task) **
# ** 5 (2025-10): Update pydantic model (biological relation;
#                 Defaults for SpanAugmentedMention properties) **
# ** 4 (2025-10): Initial version**
version = 8


[tables.immunosuppressive_medications]
response_schema = "llm/schemas/irae_medications.json"
# Version History:
# ** 7 (2026-06): Enum alignment (key=value CAPS_UNDER_BAR) **
# ** 6 (2025-12): Initial version
version = 7


[tables.multiple_transplant_history]
response_schema = "llm/schemas/irae_multiple_transplant_history.json"
# Version History:
# ** 6 (2025-12): Initial version
version = 6
