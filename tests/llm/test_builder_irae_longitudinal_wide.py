import pytest
import sqlglot
from unittest import mock
import cumulus_library

from cumulus_library_kidney_transplant.llm.builder import irae_longitudinal_wide as builder_module

EXPECTED_COLS = [
    'note_ref',
    'subject_ref',
    'generated_on',
    'task_version',
    'system_fingerprint',
    'origin',
    'rx_therapeutic_status',
    'rx_compliance',
    'dsa_history',
    'dsa',
    'infection_history',
    'infection',
    'viral_infection_history',
    'viral_infection',
    'bacterial_infection_history',
    'bacterial_infection',
    'fungal_infection_history',
    'fungal_infection',
    'graft_rejection_history',
    'graft_rejection',
    'graft_failure_history',
    'graft_failure',
    'ptld_history',
    'ptld',
    'cancer_history',
    'cancer',
    'deceased',
    'deceased_date',
]


@pytest.fixture()
def builder():
    return builder_module.IraeNlpLongitudinalFlattenedBuilder()


@mock.patch.object(builder_module.IraeNlpLongitudinalFlattenedBuilder, "_get_valid_irae_nlp_tables", return_value=set())
def test_empty_query_has_expected_columns(mock_tables, database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")
    builder.prepare_queries(config=config)

    assert len(builder.queries) == 1
    parsed = sqlglot.parse_one(builder.queries[0])
    table_alias = parsed.find(sqlglot.exp.TableAlias)
    col_names = [c.name for c in table_alias.args.get("columns", [])]
    assert col_names == EXPECTED_COLS
