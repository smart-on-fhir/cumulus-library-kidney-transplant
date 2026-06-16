import pytest
import sqlglot
from unittest import mock
import cumulus_library

from cumulus_library_kidney_transplant.llm.builder import irae_immunosuppressive_medications_wide as builder_module

EXPECTED_COLS = [
    'note_ref',
    'subject_ref',
    'generated_on',
    'task_version',
    'system_fingerprint',
    'origin',
    'drug_class',
    'ingredient',
    'status',
    'category',
    'route',
    'phase',
    'frequency',
    'quantity_value',
    'quantity_unit',
    'start_date',
    'end_date',
    'expected_supply_days',
    'number_of_repeats_allowed',
]


@pytest.fixture()
def builder():
    return builder_module.IraeNlpImmunosuppressiveMedicationsFlattenedBuilder()


@mock.patch.object(builder_module.IraeNlpImmunosuppressiveMedicationsFlattenedBuilder, "_get_valid_irae_nlp_tables", return_value=set())
def test_empty_query_has_expected_columns(mock_tables, database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")
    builder.prepare_queries(config=config)

    assert len(builder.queries) == 1
    parsed = sqlglot.parse_one(builder.queries[0])
    table_alias = parsed.find(sqlglot.exp.TableAlias)
    col_names = [c.name for c in table_alias.args.get("columns", [])]
    assert col_names == EXPECTED_COLS
