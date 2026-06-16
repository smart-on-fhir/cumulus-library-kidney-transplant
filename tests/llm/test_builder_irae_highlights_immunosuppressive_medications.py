import pytest
from unittest import mock
import sqlglot
import cumulus_library

from cumulus_library_kidney_transplant.llm.builder import (
    irae_immunosuppressive_medications_highlights as builder_module,
)


@pytest.fixture()
def builder():
    return builder_module.IraeNlpImmunosuppressiveMedicationsHighlightsBuilder()


def test_prepare_queries_appended_sql_is_valid(database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")
    valid_tables = {"irae__nlp_immunosuppressive_medications_gpt_oss_120b"}

    with mock.patch.object(builder, "_get_valid_irae_nlp_tables", return_value=valid_tables):
        builder.prepare_queries(config=config)

    for query in builder.queries:
        table = str(sqlglot.parse_one(query).find(sqlglot.exp.Table))
        assert table is not None
