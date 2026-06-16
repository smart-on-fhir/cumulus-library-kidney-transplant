import pytest
import sqlglot
from unittest import mock
import cumulus_library

from cumulus_library_kidney_transplant.llm.builder import irae_donor_wide as builder_module

EXPECTED_COLS = [
    'note_ref',
    'subject_ref',
    'generated_on',
    'task_version',
    'system_fingerprint',
    'origin',
    'donor_transplant_date',
    'donor_type',
    'donor_relationship',
    'donor_hla_match_quality',
    'donor_hla_mismatch_count',
    'donor_serostatus',
    'donor_serostatus_cmv',
    'donor_serostatus_ebv',
    'recipient_serostatus',
    'recipient_serostatus_cmv',
    'recipient_serostatus_ebv',
]


@pytest.fixture()
def builder():
    return builder_module.IraeNlpDonorFlattenedBuilder()


@mock.patch.object(builder_module.IraeNlpDonorFlattenedBuilder, "_get_valid_irae_nlp_tables", return_value=set())
def test_empty_query_has_expected_columns(mock_tables, database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")
    builder.prepare_queries(config=config)

    assert len(builder.queries) == 1
    parsed = sqlglot.parse_one(builder.queries[0])
    table_alias = parsed.find(sqlglot.exp.TableAlias)
    col_names = [c.name for c in table_alias.args.get("columns", [])]
    assert col_names == EXPECTED_COLS
