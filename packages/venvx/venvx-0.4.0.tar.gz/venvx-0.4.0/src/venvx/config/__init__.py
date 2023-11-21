
'''
Venvx's configuration/setings class.
'''

from dataclasses import dataclass
from pathlib import Path

from . import toml


@dataclass
class Config:
    '''
    Loads configuration settings from TOML files.
    '''
    fix_new_venvs: bool = False
    upgrade_pip: bool = False
    venv_prefix: str = None
    append_version: bool = False
    config_path: Path = None

    def __post_init__(self):
        '''
        Initialize the default settings from the TOML file defaults.toml.
        '''
        self.config_path = Path(__file__).parent.resolve() / 'defaults.toml'

        self.load_config(self.config_path)
        self.merge_configs()

    def load_config(self, path: Path):
        '''
        Load the configuration settings from the named TOML file.
        '''
        config = toml.load(path)
        table = config.get('tool')
        config = table.get('venvx') if table else None
        if not config:
            return
        append_version = config.get('append-version')
        fix_new_venvs = config.get('fix-new-venvs')
        upgrade_pip = config.get('upgrade-pip')
        if append_version is not None:
            self.append_version = append_version
        if fix_new_venvs is not None:
            self.fix_new_venvs = fix_new_venvs
        if upgrade_pip is not None:
            self.upgrade_pip = upgrade_pip
        if venv_prefix := config.get('venv-prefix'):
            self.venv_prefix = venv_prefix

    def merge_configs(self):
        home_toml = Path.home().resolve() / '.config' / 'venvx.toml'
        proj_toml = Path('pyproject.toml')
        for path in [home_toml, proj_toml]:
            if not path.exists():
                continue
            self.load_config(path)
