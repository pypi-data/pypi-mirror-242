# venvx

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/venvx/0.3.0)](https://pypi.org/project/venvx/)
[![PyPI version](https://badge.fury.io/py/venvx.svg)](https://badge.fury.io/py/venvx)

Create and use virtual environments with ease

## Installation

Install the venvx package with pip

```sh
python -m pip install --user venvx
```

or your favorite Python package manager. To install the `venv` shell extension, enter

```sh
venvx shellext > ~/.venvx.sh
```

Review the content of the file and source it into your bash or zsh profile.

## Usage

Assuming the current directory contains two virtual enviroments called .venv3.10 and .venv3.11:

```sh
% ls -a
./         ../        .venv3.10/ .venv3.11/
```

The command `venv use` activates, and switches between, virtual environments.

```sh
% venv use .venv3.10
(.venv3.10) % which pip
/path/to/.venv3.10/bin/pip
```

If the venv name begins with .venv, it suffices to specify the remainder of the name. For instance, in order to switch to another virtual enviroment:

```sh
(.venv3.10) % venv use 3.11
(.venv3.11) % which pip
/path/to/.venv3.11/bin/pip
```

To quickly run a command in a virtual environment, use the run command.

```sh
(.venv3.11) % venv run 3.10 which python
/path/to/.venv3.10/bin/python
(.venv3.11) %
```

Since venv always activates the virtual environment internally, venv commands may be run within another virtual environment as shown above, or outside:

```sh
(.venv3.11) % venv off
% venv run 3.10 pytest -v tests
%
```

New virtual environments can be created with `venv create`. If the name of the virtual environment is omitted, ".venv" will be used:

```sh
% venv create
```

or use a different name e.g.

```sh
% venv create pyenv
```

The Python version to use within the new virtual environment may be specified with the -v (a.k.a. --versions) option.

```sh
% mkdir newdir && cd newdir
% venv create -v 3.8 3.9
% venv create pyenv -v 3.8 3.9
% ls -a
./        ../       .venv3.8/ .venv3.9/ pyenv3.8/ pyenv3.9/
```

The new virtual environments have already been upgraded to the most recent version of the `pip` package. The command

```sh
% venv upgrade-pip existing_env
```
upgrades the pip module of an existing virtual environment. Obviously, this works in an activated virtual enviroment as well.

```sh
% venv use 3.9
(.venv3.9) % venv upgrade-pip
```

In Git Bash on Windows, the Scripts/activate script defines a VIRTUAL_ENV path that contains both "/" and "\\" path separators. `venv fix [path]` corrects that.

When a virtual environment is copied to a different location, the activate script's VIRTUAL_ENV setting, as well as the shebangs in the various scripts within the venv's bin/ folder, all still refer to the original virtual environment. `venv fix [path]` performs the necessary updates. Example (Darwin or Linux):

```sh
% mv .venv3.9 .venv39
% venv fix 39
Checking if any scripts require patches - yes (6)
Fixing the shebang in pip3 - done
Fixing the shebang in pip - done
Fixing the shebang in pip3.9 - done
Fixing the VIRTUAL_ENV setting in activate.fish - done
Fixing the VIRTUAL_ENV setting in activate - done
Fixing the VIRTUAL_ENV setting in activate.csh - done
```

Enter `venv help` and `venvx -h` for more information on usage.
