
import shutil

from pathlib import Path

from venvx.config import Config

from .decorators import isolate


data_dir = Path(__file__).parent / 'data'


@isolate
def test_defaults():
    '''Load and verify the default settings.'''
    config = Config()
    assert config.append_version is True
    assert config.fix_new_venvs is True
    assert config.upgrade_pip is True
    assert config.venv_prefix == '.venv'


@isolate
def test_dotconfig():
    '''
    Create .config/venvx.toml in our tmp test case folder wjich is
    also $HOME for the duration of this test. Verify that the settings
    in that TOML file overwrite those in the defaults.
    '''
    _create_dotconfig()
    config = Config()
    assert config.append_version is True
    assert config.fix_new_venvs is False
    assert config.upgrade_pip is False
    assert config.venv_prefix == 'myenv'


@isolate
def test_pyproject():
    '''
    Create a "project" with an empty pyproject.toml file. Verify that
    the settings are the same as before.
    '''
    _create_pyproject()
    config = Config()
    assert config.append_version is False
    assert config.fix_new_venvs is True
    assert config.upgrade_pip is True
    assert config.venv_prefix == 'venv'


@isolate
def test_dotconfig_and_pyproject():
    '''
    Create a "project" and a pyproject.toml file with some settings in it.
    Verify that these settings overwrite those in the default and ~/.config
    TOML files.
    '''
    _create_dotconfig()
    config1 = Config()
    _create_pyproject()
    config2 = Config()
    assert config1.append_version != config2.append_version
    assert config1.fix_new_venvs == config2.fix_new_venvs
    assert config1.upgrade_pip == config2.upgrade_pip
    assert config1.venv_prefix != config2.venv_prefix


def _create_dotconfig():
    configdir = Path('.config')
    configdir.mkdir()
    tomlfile = data_dir / 'venvx.toml'
    shutil.copy(tomlfile, configdir)


def _create_pyproject():
    projdir = Path('.')
    #projdir.mkdir()
    tomlfile = data_dir / 'pyproject.toml'
    shutil.copy(tomlfile, '.')
