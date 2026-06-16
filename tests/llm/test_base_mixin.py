import pytest
from unittest import mock
import cumulus_library

from cumulus_library_kidney_transplant.tools import filetool
from cumulus_library_kidney_transplant.llm.builder import irae_base_mixin as base_module

# Minimal concrete subclass for testing IraeLLMBaseMixin directly.
TASK_DISPLAY = 'Test Task'
TASK_DISPLAY_LOWER = 'test_task'


class ConcreteIraeLLMBuilder(
    base_module.IraeLLMBaseMixin,
    cumulus_library.BaseTableBuilder,
    task_display=TASK_DISPLAY,
    task_tabular_display=TASK_DISPLAY_LOWER,
    task_table_suffix='test',
):
    def _make_empty_query(self, config: cumulus_library.StudyConfig):
        return "SELECT 1"


@pytest.fixture()
def builder():
    return ConcreteIraeLLMBuilder()


@pytest.fixture()
def source_tables():
    return [
        f"irae__nlp_{TASK_DISPLAY_LOWER}_claude_sonnet45",
        f"irae__nlp_{TASK_DISPLAY_LOWER}_gpt51",
        f"irae__nlp_{TASK_DISPLAY_LOWER}_gpt_oss_120b",
    ]


def test_is_table_valid_delegates_to_sql_utils(database, builder):
    with mock.patch.object(
        base_module.sql_utils, "is_field_present", return_value=True
    ) as mock_is_field_present:
        result = builder._is_table_valid(database, "ANY_TABLE")

    assert result
    mock_is_field_present.assert_called_once_with(
        database=database,
        source_table="ANY_TABLE",
        source_col="result",
        expected={},
    )


def test_get_valid_tables_checks_expected_tables(database, builder, source_tables):
    with mock.patch.object(
        builder, "_is_table_valid", return_value=True
    ) as mock_is_table_valid:
        valid_tables = builder._get_valid_irae_nlp_tables(database)

    assert valid_tables == set(source_tables)
    assert [call.args for call in mock_is_table_valid.call_args_list] == [
        (database, table_name) for table_name in source_tables
    ]


def test_get_valid_tables_no_available_tables(database, builder, source_tables):
    with mock.patch.object(
        builder, "_is_table_valid", return_value=False
    ) as mock_is_table_valid:
        valid_tables = builder._get_valid_irae_nlp_tables(database)

    assert valid_tables == set()
    assert [call.args for call in mock_is_table_valid.call_args_list] == [
        (database, table_name) for table_name in source_tables
    ]


def test_get_valid_tables_available_but_not_in_source(database, builder, source_tables):
    def is_table_valid(_, table_name):
        return table_name in {"some_other_table"}

    with mock.patch.object(
        builder, "_is_table_valid", side_effect=is_table_valid
    ) as mock_is_table_valid:
        valid_tables = builder._get_valid_irae_nlp_tables(database)

    assert valid_tables == set()
    assert [call.args for call in mock_is_table_valid.call_args_list] == [
        (database, table_name) for table_name in source_tables
    ]


def test_get_valid_tables_filters_to_available_sources(database, builder, source_tables):
    available_tables = {source_tables[0], source_tables[2]}

    def is_table_valid(_, table_name):
        return table_name in available_tables

    with mock.patch.object(
        builder, "_is_table_valid", side_effect=is_table_valid
    ) as mock_is_table_valid:
        valid_tables = builder._get_valid_irae_nlp_tables(database)

    assert valid_tables == available_tables
    assert [call.args for call in mock_is_table_valid.call_args_list] == [
        (database, table_name) for table_name in source_tables
    ]


def test_prepare_queries_appends_template_from_valid_tables(database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")
    one_valid_table = {f"irae__nlp_{TASK_DISPLAY_LOWER}_gpt_oss_120b"}
    rendered_query = f"select * from irae__nlp_{TASK_DISPLAY_LOWER}_gpt_oss_120b"

    with mock.patch.object(
        builder, "_get_valid_irae_nlp_tables", return_value=one_valid_table
    ) as mock_get_valid_tables, mock.patch.object(
        base_module.cumulus_library, "get_template", return_value=rendered_query
    ) as mock_get_template:
        builder.prepare_queries(config=config)

    mock_get_valid_tables.assert_called_once_with(config.db)
    mock_get_template.assert_called_once_with(
        f"irae__llm_{TASK_DISPLAY_LOWER}_test",
        filetool.path_llm_template(),
        table_names=one_valid_table,
    )
    assert builder.queries == [rendered_query]


def test_prepare_queries_falls_back_to_empty_query_when_no_tables(database, builder):
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")

    with mock.patch.object(builder, "_get_valid_irae_nlp_tables", return_value=set()):
        builder.prepare_queries(config=config)

    assert builder.queries == ["SELECT 1"]


def test_prepare_queries_raises_without_template_when_tables_present(database, builder):
    """Confirm that a missing Jinja template raises FileNotFoundError."""
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")
    one_valid_table = {f"irae__nlp_{TASK_DISPLAY_LOWER}_gpt_oss_120b"}

    with mock.patch.object(
        builder, "_get_valid_irae_nlp_tables", return_value=one_valid_table
    ):
        with pytest.raises(FileNotFoundError):
            builder.prepare_queries(config=config)
