from enum import Enum
from typing import List, Dict, Any, Iterable, Generator
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.coding import Coding

###############################################################################
#
# Type Check (yes/no)
#
###############################################################################
def is_enum(obj) -> bool:
    return isinstance(obj, Enum)

def is_list(obj) -> bool:
    return isinstance(obj, list)

def is_list_type(obj, type) -> bool:
    if isinstance(obj, list) and all(isinstance(item, type) for item in obj):
        return True
    return False

###############################################################################
#
# Guard input types, fail fast
#
###############################################################################
def guard_list(obj) -> list:
    if isinstance(obj, list):
        return obj
    return [obj]

def guard_range(obj) -> range:
    print(f'guard_range : {obj}')
    if isinstance(obj, list):
        return range(obj[0], obj[1])
    if isinstance(obj, tuple):
        return range(obj[0], obj[1])
    if isinstance(obj, range):
        return obj

    Exception(f'guard_range failed for {obj}')

def guard_range_or_none(obj) -> range:
    if not obj:
        return None
    return guard_range(obj)

def guard_list_coding(obj) -> List[Coding]:
    obj = guard_list(obj)

    if is_list_type(obj, Coding):
        return obj

    return [as_coding(c) for c in list(enum_type)]

def as_coding(obj) -> Coding:
    c = Coding()
    src = obj.__dict__
    c.code = src.get('code')
    c.display = src.get('display')
    c.system = src.get('system')
    return c

###############################################################################
#
# Collection safety
#
###############################################################################
def uniq(unsorted: Iterable) -> List:
    """
    :param unsorted: list of header names
    :return: sorted list of unique header names
    """
    return sorted(list(set(unsorted)))