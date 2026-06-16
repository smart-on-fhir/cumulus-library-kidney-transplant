import pytest
import sqlglot
from unittest import mock
import cumulus_library

from cumulus_library_kidney_transplant.llm.builder import irae_highlights_mixin as mixin_module

TASK_DISPLAY = 'Test Task'
TASK_DISPLAY_LOWER = 'test_task'


class ConcreteIraeHighlightsBuilder(
    mixin_module.IraeHighlightsMixin,
    cumulus_library.BaseTableBuilder,
    task_display=TASK_DISPLAY,
    task_tabular_display=TASK_DISPLAY_LOWER,
):
    pass


@pytest.fixture()
def builder():
    return ConcreteIraeHighlightsBuilder()


def test_dest_table_has_highlights_suffix(builder):
    assert builder.dest_table == f"irae__llm_{TASK_DISPLAY_LOWER}_highlights"


def test_make_empty_query_produces_valid_sql(database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")

    with mock.patch.object(builder, "_get_valid_irae_nlp_tables", return_value=set()):
        builder.prepare_queries(config=config)

    assert len(builder.queries) == 1
    table = str(sqlglot.parse_one(builder.queries[0]).find(sqlglot.exp.Table))
    assert table is not None
