import re
import tempfile
import unittest
from pathlib import Path

from cumulus_library_kidney_transplant.sample_command_generation import (
    file_friendly_variable_name,
    generate_exclusion_regex,
    generate_select_by_keyword_lines,
    get_keyword_patterns,
    get_keywords_for_variable,
    make_negation_regex,
    parse_keyword_tsv,
    render_sample_script,
    space_friendly_variable_name,
)

#################################################
# SHARED FIXTURES

# Raw strings for regex keywords avoid SyntaxWarning on Python 3.12+
_NOW_DAY_RE = r"REGEX: now day\s*\+?\d+"
_TRANSPLANT_DATE_RE = r"REGEX: transplant\s*\(?\d+\s*/\s*\d+\)?"

FIXTURE_TSV = (
    "Link to Variables\tTransplant Date\tDonor Status\tDonor Relationship\n"
    f'"Transplant Date \ntransplanted on\nPOD\ntransplant on \n{_NOW_DAY_RE}\n{_TRANSPLANT_DATE_RE}"\tX\t\t\n'
    '"Living Donor\nLiving Kidney\nLDRT"\t\tX\t\n'
    '"LURD\nliving unrelated donor"\t\tX\tX\n'
)

# Expected parse results derived from FIXTURE_TSV
EXPECTED_VARIABLES = ["Transplant Date", "Donor Status", "Donor Relationship"]
EXPECTED_LOOKUP = {
    "Transplant Date": {
        "keywords": ["Transplant Date", "transplanted on", "POD", "transplant on", _NOW_DAY_RE, _TRANSPLANT_DATE_RE],
        "relevant variables": ["Transplant Date"],
    },
    "Living Donor": {
        "keywords": ["Living Donor", "Living Kidney", "LDRT"],
        "relevant variables": ["Donor Status"],
    },
    "LURD": {
        "keywords": ["LURD", "living unrelated donor"],
        "relevant variables": ["Donor Status", "Donor Relationship"],
    },
}

DEFAULT_SOURCE_TABLE = "irae__sample_casedef_peri"


def write_fixture_tsv(content: str) -> Path:
    """
    Write content to a named temp file and return its Path.
    """
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False)
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


#################################################
# parse_keyword_tsv
# 
class TestParseKeywordTsv(unittest.TestCase):
    def setUp(self):
        self.tsv_path = write_fixture_tsv(FIXTURE_TSV)
        self.lookup, self.variables = parse_keyword_tsv(self.tsv_path)

    def tearDown(self):
        self.tsv_path.unlink(missing_ok=True)

    def test_variable_names_returned(self):
        self.assertEqual(self.variables, EXPECTED_VARIABLES)

    def test_lookup_keys_are_first_keyword_of_each_group(self):
        self.assertEqual(
            set(self.lookup.keys()),
            {"Transplant Date", "Living Donor", "LURD"},
        )

    def test_multi_line_transplant_date_keywords(self):
        self.assertEqual(
            self.lookup["Transplant Date"]["keywords"],
            ["Transplant Date", "transplanted on", "POD", "transplant on", _NOW_DAY_RE, _TRANSPLANT_DATE_RE],
        )

    def test_multi_line_living_donor_keywords(self):
        self.assertEqual(
            self.lookup["Living Donor"]["keywords"],
            ["Living Donor", "Living Kidney", "LDRT"],
        )

    def test_multi_line_lurd_keywords(self):
        self.assertEqual(
            self.lookup["LURD"]["keywords"],
            ["LURD", "living unrelated donor"],
        )

    def test_regex_keywords_in_transplant_date_lookup(self):
        keywords = self.lookup["Transplant Date"]["keywords"]
        regex_keywords = [k for k in keywords if k.startswith("REGEX:")]
        self.assertEqual(len(regex_keywords), 2)
        self.assertIn(_NOW_DAY_RE, regex_keywords)
        self.assertIn(_TRANSPLANT_DATE_RE, regex_keywords)

    def test_transplant_date_keywords_relevant_only_to_transplant_date(self):
        self.assertEqual(
            self.lookup["Transplant Date"]["relevant variables"],
            ["Transplant Date"],
        )

    def test_living_donor_relevant_only_to_donor_status(self):
        self.assertEqual(
            self.lookup["Living Donor"]["relevant variables"],
            ["Donor Status"],
        )

    def test_lurd_keywords_relevant_to_donor_status_and_relationship(self):
        self.assertEqual(
            self.lookup["LURD"]["relevant variables"],
            ["Donor Status", "Donor Relationship"],
        )

    def test_blank_keyword_rows_are_skipped(self):
        # A row with no keyword cell (just tabs) should not produce a lookup entry
        tsv_with_blank = FIXTURE_TSV + "\t\t\t\n"
        path = write_fixture_tsv(tsv_with_blank)
        lookup, _ = parse_keyword_tsv(path)
        self.assertNotIn("", lookup)
        path.unlink(missing_ok=True)

    def test_empty_tsv_returns_empty_dict(self):
        path = write_fixture_tsv("")
        result, _ = parse_keyword_tsv(path)
        self.assertEqual(result, {})
        path.unlink(missing_ok=True)


#################################################
# All Variable-name helpers
#
class TestNameHelpers(unittest.TestCase):
    ####################
    # file_friendly_variable_name 
    def test_file_friendly_donor_status(self):
        self.assertEqual(file_friendly_variable_name("Donor Status"), "donor-status")

    def test_file_friendly_underscores_to_hyphens(self):
        self.assertEqual(file_friendly_variable_name("donor_status"), "donor-status")

    def test_file_friendly_lowercases(self):
        self.assertEqual(file_friendly_variable_name("DSA"), "dsa")

    ####################
    # space_friendly_variable_name
    def test_space_friendly_donor_status_hyphen_to_spaces(self):
        self.assertEqual(space_friendly_variable_name("donor-status"), "donor status")

    def test_space_friendly_underscores_to_spaces(self):
        self.assertEqual(space_friendly_variable_name("donor_status"), "donor status")

    def test_space_friendly_unchanged_if_already_spaced(self):
        self.assertEqual(space_friendly_variable_name("donor status"), "donor status")

    def test_space_friendly_caps_unchanged(self):
        self.assertEqual(space_friendly_variable_name("HLA Mismatch"), "HLA Mismatch")


#################################################
# get_keywords_for_variable
#
class TestGetKeywordsForVariable(unittest.TestCase):
    def setUp(self):
        self.lookup = EXPECTED_LOOKUP

    def test_transplant_date_includes_all_transplant_terms(self):
        keywords = get_keywords_for_variable(self.lookup, "Transplant Date")
        self.assertIn("Transplant Date", keywords)
        self.assertIn("transplanted on", keywords)
        self.assertIn("POD", keywords)
        self.assertIn("transplant on", keywords)

    def test_transplant_date_includes_both_regex_patterns(self):
        keywords = get_keywords_for_variable(self.lookup, "Transplant Date")
        self.assertIn(_NOW_DAY_RE, keywords)
        self.assertIn(_TRANSPLANT_DATE_RE, keywords)

    def test_transplant_date_excludes_donor_terms(self):
        keywords = get_keywords_for_variable(self.lookup, "Transplant Date")
        self.assertNotIn("Living Donor", keywords)
        self.assertNotIn("LDRT", keywords)
        self.assertNotIn("LURD", keywords)
        self.assertNotIn("living unrelated donor", keywords)

    def test_unknown_variable_returns_empty_list(self):
        self.assertEqual(get_keywords_for_variable(self.lookup, "Any Rejection"), [])


#################################################
# generate_select_by_keyword_lines
#
class TestGenerateSelectByKeywordLines(unittest.TestCase):
    def test_empty_keywords_returns_empty_string(self):
        self.assertEqual(generate_select_by_keyword_lines([]), "")

    def test_transplant_date_produces_select_by_word(self):
        result = generate_select_by_keyword_lines(["Transplant Date"])
        self.assertIn('--select-by-word "Transplant Date"', result)

    def test_transplant_date_regex_produces_select_by_regex(self):
        result = generate_select_by_keyword_lines(["REGEX: transplant\\s*(\\d+/\\d+)"])
        self.assertIn("--select-by-regex", result)
        self.assertNotIn("--select-by-word", result)

    def test_regex_prefix_stripped_from_output(self):
        result = generate_select_by_keyword_lines(["REGEX: transplant\\s*(\\d+/\\d+)"])
        self.assertNotIn("REGEX:", result)
        self.assertIn("transplant\\s*(\\d+/\\d+)", result)

    def test_mixed_transplant_date_and_regex_produce_both_flag_types(self):
        result = generate_select_by_keyword_lines(
            ["Transplant Date", "REGEX: transplant\\s*(\\d+/\\d+)"]
        )
        self.assertIn("--select-by-word", result)
        self.assertIn("--select-by-regex", result)

    def test_lines_joined_with_shell_continuation(self):
        result = generate_select_by_keyword_lines(["Transplant Date", "POD"])
        lines = result.split("\n")
        for line in lines[:-1]:
            self.assertTrue(
                line.rstrip().endswith("\\"),
                f"Expected continuation backslash on: {line!r}",
            )


#################################################
# get_keyword_patterns
#
class TestGetKeywordPatterns(unittest.TestCase):
    def test_plain_transplant_date_keyword_is_regex_escaped(self):
        patterns = get_keyword_patterns(["Transplant Date"])
        self.assertEqual(patterns, [re.escape("Transplant Date")])

    def test_keyword_with_special_chars_is_escaped(self):
        # "D+" (donor serostatus notation) contains a literal plus sign
        patterns = get_keyword_patterns(["D+"])
        self.assertEqual(patterns, [re.escape("D+")])
        self.assertIn("\\+", patterns[0])

    def test_transplant_date_regex_is_not_escaped(self):
        kw = "REGEX: transplant\\s*(\\d+/\\d+)"
        patterns = get_keyword_patterns([kw])
        self.assertEqual(patterns, ["transplant\\s*(\\d+/\\d+)"])

    def test_mixed_plain_and_regex_keywords(self):
        patterns = get_keyword_patterns(["Transplant Date", "REGEX: transplant\\s*(\\d+/\\d+)"])
        self.assertEqual(patterns[0], re.escape("Transplant Date"))
        self.assertEqual(patterns[1], "transplant\\s*(\\d+/\\d+)")


#################################################
# generate_exclusion_regex
#
class TestGenerateExclusionRegex(unittest.TestCase):
    def setUp(self):
        # Patterns derived from transplant-date keywords
        self.regex = generate_exclusion_regex(
            [re.escape("Transplant Date"), "transplant\\s*(\\d+/\\d+)"]
        )

    def test_returns_compiled_pattern(self):
        self.assertIsInstance(self.regex, re.Pattern)

    def test_matches_unrelated_clinical_note(self):
        self.assertIsNotNone(self.regex.match("routine post-op follow-up, no concerns"))

    def test_no_match_when_transplant_date_present(self):
        self.assertIsNone(self.regex.match("Transplant Date was noted"))

    def test_no_match_when_transplant_date_pattern_present(self):
        self.assertIsNone(self.regex.match("transplant 07/20 reviewed"))

    def test_word_boundary_respected_for_transplant_date(self):
        # "Transplant Date" as a whole word triggers exclusion; substring does not
        self.assertIsNone(self.regex.match("acute Transplant Date noted"))

    def test_empty_string_matches(self):
        self.assertIsNotNone(self.regex.match(""))


#################################################
# make_negation_regex
#
class TestMakeNegationRegex(unittest.TestCase):
    def setUp(self):
        self.regex = make_negation_regex(EXPECTED_LOOKUP)

    def test_returns_compiled_pattern(self):
        self.assertIsInstance(self.regex, re.Pattern)

    def test_matches_note_with_no_relevant_keywords(self):
        self.assertIsNotNone(
            self.regex.match("patient presents for routine annual nephrology visit")
        )

    def test_no_match_when_transplant_date_term_present(self):
        self.assertIsNone(self.regex.match("Transplant Date was recorded in chart"))

    def test_no_match_when_transplanted_on_present(self):
        self.assertIsNone(self.regex.match("patient was transplanted on March 1st"))

    def test_no_match_when_living_donor_present(self):
        self.assertIsNone(self.regex.match("Living Donor nephrectomy performed"))

    def test_no_match_when_ldrt_abbreviation_present(self):
        self.assertIsNone(self.regex.match("LDRT scheduled for next month"))

    def test_no_match_when_lurd_present(self):
        self.assertIsNone(self.regex.match("LURD was the donor type"))

    def test_no_match_when_living_unrelated_donor_present(self):
        self.assertIsNone(self.regex.match("patient received a living unrelated donor kidney"))

    def test_no_match_when_transplant_date_regex_matches(self):
        self.assertIsNone(self.regex.match("transplant 11/15 reviewed in clinic"))

    def test_all_plain_keywords_trigger_exclusion(self):
        plain_keywords = [
            ("Transplant Date", "Transplant Date was recorded"),
            ("transplanted on", "patient was transplanted on day 0"),
            ("POD", "POD 3 post-transplant check-in"),
            ("transplant on", "scheduled to transplant on Monday"),
            ("Living Donor", "Living Donor consented"),
            ("Living Kidney", "Living Kidney transplant performed"),
            ("LDRT", "LDRT listed as donor type"),
            ("LURD", "LURD was selected as donor"),
            ("living unrelated donor", "patient received a living unrelated donor organ"),
        ]
        for kw, sentence in plain_keywords:
            with self.subTest(keyword=kw):
                self.assertIsNone(
                    self.regex.match(sentence),
                    f"Expected no match when '{kw}' is present in: {sentence!r}",
                )


#################################################
# render_sample_script
#
class TestRenderSampleScript(unittest.TestCase):
    SOURCE_TABLE = DEFAULT_SOURCE_TABLE

    def _render(self, variable="Living Donor", keywords=["Living Donor", "Living Kidney", "LDRT"]):
        return render_sample_script(variable, keywords, self.SOURCE_TABLE)

    def test_starts_with_shebang(self):
        script = self._render()
        self.assertTrue(script.strip().startswith("#!/bin/bash"))

    def test_contains_human_readable_variable_name(self):
        script = self._render(variable="Living Donor")
        self.assertIn("Living Donor", script)

    def test_output_path_uses_file_friendly_name(self):
        script = self._render(variable="Living Donor")
        self.assertIn("living-donor", script)

    def test_donor_status_variable_uses_correct_slug(self):
        script = self._render(variable="Donor Status", keywords=["Living Donor", "LDRT"])
        self.assertIn("donor-status", script)

    def test_source_table_present_in_script(self):
        script = self._render()
        self.assertIn(self.SOURCE_TABLE, script)

    def test_living_donor_keyword_rendered_as_select_by_word(self):
        script = self._render(keywords=["Living Donor"])
        self.assertIn('--select-by-word "Living Donor"', script)

    def test_transplant_date_regex_rendered_as_select_by_regex(self):
        script = self._render(keywords=["REGEX: transplant\\s*(\\d+/\\d+)"])
        self.assertIn("--select-by-regex", script)
        self.assertNotIn("REGEX:", script)

    def test_standard_flags_present(self):
        script = self._render()
        self.assertIn("--count 30", script)
        self.assertIn("--seed 07201869", script)
        self.assertIn("--allow-large-selection", script)
        self.assertIn("--select-by-athena-table", script)


