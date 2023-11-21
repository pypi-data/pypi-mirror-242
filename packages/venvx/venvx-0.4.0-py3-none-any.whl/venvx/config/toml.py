
'''
This module provides a toml.load() method for all versions of Python.
'''

from pathlib import Path
try:
    from tomllib import load as load_toml
except ModuleNotFoundError:
    from tomli import load as load_toml


def load(path: Path) -> dict:
    content = None
    with open(path, 'rb') as fid:
        content = load_toml(fid)
    return content
