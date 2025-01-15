from typing import List
from enum import Enum
from cumulus_library_kidney_transplant.study_prefix import PREFIX
from cumulus_library_kidney_transplant.schema import (
    Table,
    Demographic,
    Encounter,
    CountDistinct
)

class GraphType(Enum):
    """
    These are the only types we need to support through templates.
    Start with just "column" type as it is the easiest
    """
    column = 'column'
    bar = 'bar'
    line = 'line'

class Graph:
    """
    Graph minimal template
    :param type: defines [column|bar|line]
    :param alias: human readable name for the user
    :param tablename: source of the count table
    :param cnt: count column source, typically [cnt_subject|cnt_encounter]
    :param statifier: optionally stratify count into a percentage (count/stratifier)
    :param x_axis: x-axis variable, if None, x-axis is the "cnt"
    :param y_axis: y-axis variable, if None, y-axis is the "cnt"
    """
    type: GraphType = None
    alias: str = None
    table: str = None
    cols: List[str] = None
    cnt = None
    stratifier = None
    x_axis = None
    y_axis = None

    def __init__(self,
                 type: GraphType = None,
                 alias=None,
                 table: str | Table = None,
                 cnt: str | CountDistinct = None,
                 statifier=None,
                 x_axis=None,
                 y_axis=None):

        self.type = type
        self.alias = alias
        self.table = table
        self.cnt = cnt
        self.stratifier = statifier
        self.x_axis = x_axis
        self.y_axis = y_axis

    def as_json(self):
        out = {'type': str(self.type),
               'alias': self.alias,
               'table': self.table,
               'stratifier': str(self.stratifier),
               'cnt': str(self.cnt),
               'x_axis': str(self.x_axis),
               'y_axis': str(self.y_axis)}
        return out

def graph_list(prefix=PREFIX) -> List[Graph]:
    """
    Default list of Dashboard graphs for a study
    :param prefix: alias for the study, such as "suicide_icd10"
    :return: List of supported dashboard.Graph
    """
    return [
        graph_population_cnt_patient_by_gender_race(prefix),
        graph_population_cnt_encounter_by_gender_age(prefix),
        graph_cohort_casedef_cnt_patient_by_gender_race(prefix),
        graph_cohort_casedef_cnt_encounter_by_age_gender(prefix)
    ]

def graph_population_cnt_patient_by_gender_race(table=None) -> Graph:
    """
    :param prefix: prefix name of study
    :param table: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not table:
        table = Table.study_population.name

    graph = Graph()
    graph.alias = 'Number of patients in study population stratified by gender and race'
    graph.table = table
    graph.type = GraphType.column
    graph.cnt = CountDistinct.subject_ref
    graph.x_axis = Demographic.gender
    graph.stratifier = Demographic.race

    return graph

def graph_population_cnt_encounter_by_gender_age(table=None) -> Graph:
    """
    :param table: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not table:
        table = Table.study_population.name

    graph = Graph()
    graph.alias = 'Number of encounters in study population stratified by age at visit and gender'
    graph.table = table
    graph.type = GraphType.column
    graph.cnt = CountDistinct.encounter_ref
    graph.x_axis = Encounter.age_at_visit
    graph.stratifier = Demographic.gender

    return graph

def graph_cohort_casedef_cnt_patient_by_gender_race(table=None) -> Graph:
    """
    :param table: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not table:
        table = Table.cohort.name

    graph = Graph()
    graph.alias = 'Number of patient cases stratified by gender and race'
    graph.table = table
    graph.type = GraphType.column
    graph.cnt = CountDistinct.subject_ref
    graph.x_axis = Demographic.gender
    graph.stratifier = Demographic.race

    return graph

def graph_cohort_casedef_cnt_encounter_by_age_gender(table=None) -> Graph:
    """
    :param table: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not table:
        table = Table.casedef.name

    graph = Graph()
    graph.alias = 'Number of encounters for cases stratified by age at visit and gender'
    graph.table = table
    graph.type = GraphType.column
    graph.cnt = CountDistinct.encounter_ref
    graph.x_axis = Encounter.age_at_visit
    graph.stratifier = Demographic.gender

    return graph
