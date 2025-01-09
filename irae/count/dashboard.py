from typing import List
from enum import Enum
from irae import manifest, filetool, fhir2sql
from cumulus_library.builders.counts import CountsBuilder
from irae.count.columns import (
    Table,
    Demographic,
    CountDistinct
)

PREFIX = manifest.get_study_prefix()

class Cube:
    table: str = None
    cohort: str = None
    col_list: List[str] = None
    builder = CountsBuilder(manifest.get_study_prefix())

    def __init__(self, view: str, cohort: str, col_list: List[str]):
        """
        :param view: name of the table in the CTAS statement (create `table` as )
        :param cohort: source table to compile the cube counts
        :param col_list: list of columns to include in the cube output
        """
        self.table = view
        self.cohort = cohort
        self.col_list = col_list

    def count_encounter(self):
        return filetool.save_athena_view(
            view_name=self.table,
            contents=self.builder.count_encounter(self.table, self.cohort, self.col_list))

    def count_patient(self):
        return filetool.save_athena_view(
            view_name=self.table,
            contents=self.builder.count_patient(self.table, self.cohort, self.col_list))


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
    :param x: x-axis variable, if None, x-axis is the "cnt"
    :param y: y-axis variable, if None, y-axis is the "cnt"
    """
    type: GraphType = None
    alias: str = None
    tablename: str = None
    cnt = None
    stratifier = None
    x = None
    y = None

    def as_json(self):
        out = {'type': str(self.type),
               'alias': self.alias,
               'tablename': self.tablename,
               'stratifier': str(self.stratifier),
               'cnt': str(self.cnt),
               'x': str(self.x),
               'y': str(self.y)}
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
        graph_cohort_cases_cnt_patient_by_gender_race(prefix),
        graph_cohort_cases_cnt_encounter_by_gender_age(prefix)
    ]

def graph_population_cnt_patient_by_gender_race(tablename=None) -> Graph:
    """
    :param prefix: prefix name of study
    :param tablename: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not tablename:
        tablename = Table.study_population.name

    graph = Graph()
    graph.alias = 'Number of patients in study population stratified by gender and race'
    graph.tablename = tablename
    graph.type = GraphType.column
    graph.cnt = CountDistinct.subject_ref
    graph.x = Demographic.gender
    graph.stratifier = Demographic.race

    return graph

def graph_population_cnt_encounter_by_gender_age(prefix=None, tablename=None) -> Graph:
    """
    :param prefix: prefix name of study
    :param tablename: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not tablename:
        tablename = Table.study_population.name

    graph = Graph()
    graph.alias = 'Number of encounters in study population stratified by age at visit and gender'
    graph.tablename = tablename
    graph.type = GraphType.column
    graph.cnt = CountDistinct.encounter_ref
    graph.x = Encounter.age_at_visit
    graph.stratifier = Demographic.gender

    return graph

def graph_cohort_cases_cnt_patient_by_gender_race(prefix=None, tablename=None) -> Graph:
    """
    :param prefix: prefix name of study
    :param tablename: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not tablename:
        tablename = Table.cohort.name

    graph = Graph()
    graph.alias = 'Number of patient cases stratified by gender and race'
    graph.tablename = tablename
    graph.type = GraphType.column
    graph.cnt = CountDistinct.subject_ref
    graph.x = Demographic.gender
    graph.stratifier = Demographic.race

    return graph

def graph_cohort_cases_cnt_encounter_by_gender_age(prefix=None, tablename=None) -> Graph:
    """
    :param prefix: prefix name of study
    :param tablename: default = "$prefix__study_population"
    :return: Graph defaults
    """
    if not tablename:
        tablename = Table.casedef.name

    graph = Graph()
    graph.alias = 'Number of encounters for cases stratified by age at visit and gender'
    graph.tablename = tablename
    graph.type = GraphType.column
    graph.cnt = CountDistinct.encounter_ref
    graph.x = Encounter.age_at_visit
    graph.stratifier = Demographic.gender

    return graph
