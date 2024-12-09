import os

def filepath(filename: str) -> str:
    pwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(pwd, filename)
