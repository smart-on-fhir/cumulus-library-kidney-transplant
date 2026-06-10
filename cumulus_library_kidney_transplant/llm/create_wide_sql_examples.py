from pathlib import Path

import cumulus_library

from cumulus_library_ibd_cds.tools import filetool
from cumulus_library_ibd_cds.llm.builder import (
    IbdNlpDiagnosisFlattenedBuilder,
    IbdNlpTreatmentFlattenedBuilder,
    IbdNlpSurgeryFlattenedBuilder,
    IbdNlpParisClassificationFlattenedBuilder,
    IbdNlpDocumentTypeFlattenedBuilder,
    IbdNlpTopicRelevanceFlattenedBuilder,
)

def make(builder: cumulus_library.BaseTableBuilder, nlp_model='gpt_oss_120b') -> Path:
    """
    :param builder: IBD Wide Table Builder
    :return: Path to SQL
    """
    print('Creating example SQL for:', builder.dest_table)
    nlp_origin = f"{builder.src_table_prefix}_{nlp_model}"
    query = builder._make_query_with_tables(tables=[nlp_origin])

    return filetool.save_llm_athena(f"{builder.dest_table}.sql", query)

def make_all():
    return [
        make(IbdNlpDiagnosisFlattenedBuilder()),
        make(IbdNlpTreatmentFlattenedBuilder()),
        make(IbdNlpSurgeryFlattenedBuilder()),
        make(IbdNlpParisClassificationFlattenedBuilder()),
        make(IbdNlpDocumentTypeFlattenedBuilder()),
        make(IbdNlpTopicRelevanceFlattenedBuilder()),
    ]

if __name__ == "__main__":
    make_all()
