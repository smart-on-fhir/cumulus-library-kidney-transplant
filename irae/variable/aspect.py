from enum import Enum
from typing import List, Dict
from irae import guard

class Valueset:
    def __init__(self, name: str, oid: str | None):
        self.name = name
        self.oid = oid

    def as_json(self):
        return {self.name: self.oid}

class Variable:
    def __init__(self, name: str, valuesets: List[Valueset] | Dict[str, str]):
        self.name = name.lower()
        self.valuesets = list()
        if valuesets:
            if guard.is_list_type(valuesets, Valueset):
                self.valuesets = valuesets
            elif guard.is_dict(valuesets):
                self.valuesets = list()
                for vs_name in valuesets.keys():
                    vs_name = vs_name.lower()
                    self.valuesets.append(Valueset(vs_name, valuesets.get(vs_name)))

    def as_json(self) -> dict:
        return {self.name: [vs.as_json() for vs in self.valuesets]}

class AspectKey(Enum):
    dx = 'diagnosis'
    rx = 'medication'
    lab = 'laboratory'
    proc = 'procedure'

    def as_json(self):
        return {self.name: self.value}

class Aspect:
    variable_list = list()
    key = AspectKey

    def __init__(self, variable_list: List[Variable] | Dict[str, Dict[str, str]]):
        self.variable_list = list()

        if guard.is_list_type(variable_list, Variable):
            self.variable_list = variable_list

        elif guard.is_dict(variable_list):
            for var_name in variable_list.keys():
                vs_list = [Valueset(key, val) for key, val in variable_list.get(var_name).items()]
                self.variable_list.append(Variable(var_name, vs_list))
        self._guard_var_key()

    def _guard_var_key(self):
        guard_list = list()
        for var in self.variable_list:
            var.name = var.name.lower()
            if not var.name.startswith(self.key.name):
                var.name = f'{self.key.name}_{var.name}'
            guard_list.append(var)
        self.variable_list = guard_list

    def as_json(self) -> dict:
        return {self.key.name: [v.as_json() for v in self.variable_list]}

class Dx(Aspect):
    key = AspectKey.dx

class Rx(Aspect):
    key = AspectKey.rx

class Lab(Aspect):
    key = AspectKey.lab

class Proc(Aspect):
    key = AspectKey.proc

class AspectMap:
    def __init__(self, diagnosis: Dx | None, medication: Rx | None, lab: Lab | None, procedure: Proc | None):
        self.diagnosis = diagnosis
        self.medication = medication
        self.lab = lab
        self.procedure = procedure

    def as_list(self) -> List[Aspect]:
        return [self.diagnosis, self.medication, self.lab, self.procedure]

    def as_json(self) -> dict:
        return self.diagnosis.as_json() | self.medication.as_json() | self.lab.as_json() | self.procedure.as_json()
