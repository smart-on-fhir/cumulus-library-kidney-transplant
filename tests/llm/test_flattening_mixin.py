import pytest
from unittest import mock
import cumulus_library

from cumulus_library_kidney_transplant.llm.builder import irae_flattening_mixin as mixin_module

TASK_DISPLAY = 'Test Task'
TASK_DISPLAY_LOWER = 'test_task'


class ConcreteIraeFlatteningBuilder(
    mixin_module.IraeFlatteningMixin,
    cumulus_library.BaseTableBuilder,
    task_display=TASK_DISPLAY,
    task_tabular_display=TASK_DISPLAY_LOWER,
):
    pass  # _make_empty_query intentionally not implemented


@pytest.fixture()
def builder():
    return ConcreteIraeFlatteningBuilder()


def test_dest_table_has_wide_suffix(builder):
    assert builder.dest_table == f"irae__llm_{TASK_DISPLAY_LOWER}_wide"


def test_make_empty_query_raises_not_implemented(database, builder):
    """Flattening subclasses must implement _make_empty_query; base raises if they don't."""
    config = cumulus_library.StudyConfig(db=database, schema="placeholder_schema")

    with mock.patch.object(builder, "_get_valid_irae_nlp_tables", return_value=set()):
        with pytest.raises(NotImplementedError):
            builder.prepare_queries(config=config)
