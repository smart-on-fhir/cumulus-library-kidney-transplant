from irae import resources
from typing import List
from pathlib import Path
from irae.variable.custom_variables import RX_LIST

######################################################################
# Constants
######################################################################
ADE = 'Adverse Drug Events'
IRAE = 'Immunosuppresive Related Adverse Events'
RX_CLASS = ['immunosuppresive', 'corticosteroids', 'antibiotics', 'plasmapheresis']

######################################################################
# GPT responses are manually entered via https://chatgpt.com/
######################################################################
GPT_ENTRY = dict()
######################################################################
# Prompts
######################################################################
def prompt_common(problem: str) -> str:
    if problem == 'diagnosis':
        plural = 'diagnoses'
    else:
        plural = f'{problem}s'
    return f'What are the {plural} associated with IRAE ({IRAE})?'

def prompt_list(entry: str):
    return f'Respond with a List where each [entry] is a {entry}.'

def prompt_json(key: str, value: str):
    return f'Respond with a JSON dictionary where each {{key:value}} is {{{key}:{value}}}.'

def prompt_rx_synonyms(drug_name: str) -> str:
    question = f'What are all generic, brand, and ingredient names for "{drug_name}" ? \n'
    respond = prompt_json('ingredient', 'drug name')
    return question + respond

def prompt_rx_ade(drug_name: str) -> str:
    return f'What are the side effects or ADEs ({ADE}) for "{drug_name}" ?\n'

def prompt_problem(problem: str, explain: str) -> str:
    return prompt_common(problem) + '\n' + prompt_json(problem, explain)

######################################################################
# File Helpers
######################################################################
def file_path(filename: Path | str) -> Path:
    return resources.path_prompt(filename)

def file_exists(filename: Path | str) -> bool:
    return file_path(filename).exists()

def file_empty(filename: Path | str) -> bool:
    if not file_exists(filename):
        return True
    elif str(filename).endswith('json'):
        return 0 == len(resources.load_prompt_json(filename).items())
    else:
        return file_path(filename).stat().st_size == 0

def manifest(file_list: List[Path]) -> str:
    return '\n'.join([str(f) for f in file_list])

######################################################################
# Make targets
######################################################################

def make_llm_persona() -> Path:
    # drugs = ', '.join(RX_CLASS + RX_LIST)
    # task = f'I will now prompt you to answer IRAE questions for the following drug list [{drugs}].\n'
    who = f'You are a helpful assistant performing chart review of ADEs ({ADE}).\n'
    task = f'Your task is to provide chart review criteria for IRAE ({IRAE}).\n\n'
    next = f'I will now prompt you to suggest chart review criteria for immunosuppressive drugs.\n'
    return resources.save_prompt_text('01_llm_persona.txt', who + task + next)

def make_llm_drugs() -> List[Path]:
    file_list = list()
    for drug_name in RX_CLASS + RX_LIST:
        file_ade_text = f'03_rx_{drug_name}_ade.txt'
        file_ade_json = f'03_rx_{drug_name}_ade.json'
        file_syn_text = f'03_rx_{drug_name}_synonyms.txt'
        file_syn_json = f'03_rx_{drug_name}_synonyms.json'

        if file_empty(file_ade_text):
            file_list.append(
                resources.save_prompt_text(file_ade_text, prompt_rx_ade(drug_name)))

        if file_empty(file_ade_json):
            file_list.append(
                resources.save_prompt_json(file_ade_json, GPT_ENTRY))

        if file_empty(file_syn_text):
            file_list.append(
                resources.save_prompt_text(file_syn_text, prompt_rx_synonyms(drug_name)))

        if file_empty(file_syn_json):
            file_list.append(
                resources.save_prompt_json(file_syn_json, GPT_ENTRY))

    return file_list

def make_llm_problems() -> List[Path]:
    file_list = list()
    for explain in ['description', 'reason']:
        for problem in ['diagnosis', 'symptom', 'sign', 'finding']:
            file_text = f'02_problem_{problem}_{explain}.txt'
            file_json = f'02_problem_{problem}_{explain}.json'

            if file_empty(file_text):
                file_list.append(
                    resources.save_prompt_text(file_text, prompt_problem(problem, explain)))

            if file_empty(file_json):
                gpt_manually = dict()
                file_list.append(
                    resources.save_prompt_json(file_json, gpt_manually))
    return file_list

def prompt_labs(reason: str) -> str:
    which = f'Which laboratory tests may report abnormal results due to "{reason}" drug(s)?\n'
    return which + prompt_json('TestName', 'AbnormalResult')

def make_llm_labs() -> List[Path]:
    file_list = list()
    reason_list = RX_CLASS + RX_LIST
    for reason in reason_list:
        file_text = f'04_lab_{reason}.txt'
        file_json = f'04_lab_{reason}.json'

        if file_empty(file_text):
            file_list.append(
                resources.save_prompt_text(file_text, prompt_labs(reason)))

        if file_empty(file_json):
            file_list.append(
                resources.save_prompt_json(file_json, GPT_ENTRY))
    return file_list


######################################################################
# Make() command line
######################################################################
def make() -> List[Path]:
    return [make_llm_persona()] + make_llm_problems() + make_llm_drugs() + make_llm_labs()


if __name__ == "__main__":
    file_list = make()
    print(manifest(file_list))
