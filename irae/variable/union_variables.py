from irae import fhir2sql
from irae.variable import custom_variables, vsac_variables

def list_rx() -> list:
    drugs = custom_variables.RX_LIST

    for group in list(vsac_variables.GroupRx):
        for entry in list(group.value):
            drugs.append(entry.name)
    return drugs

def list_labs() -> list:
    labs = custom_variables.LAB_LIST

    for group in list(vsac_variables.GroupLab):
        for analyte in list(group.value):
            labs.append(analyte.name)

    for group in list(vsac_variables.GroupLabPanel):
        for component in list(group.value):
            labs.append(component.name)

    return labs

def union_aspect(aspect: str, aspect_entries: list, view_name: str) -> str:
    targets = [f'{fhir2sql.PREFIX}__{aspect}_{entry}' for entry in aspect_entries]
    return fhir2sql.union_view_list(targets, view_name)

def make():
    return union_aspect('lab', list_labs(), f'lab') + \
           union_aspect('rx', list_rx(), f'rx')


if __name__ == "__main__":
    print(list_labs())
