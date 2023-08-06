# PySoAL
### Solver abstraction layer for optimization problems

## Installation
You can install the module...
- from pip (`pip install py_soal`)

:warning: You will need to provide an additional index url for the `gurobipy` package required by `PySoAL`:

`pip install --extra-index-url=https://pypi.gurobi.com PySoAL`

### Gurobi
Gurobi can be installed via pip starting at version 9.1, which is compatible with Python 3.7+. It is included in the requirements-file and does not require any special installation-instructions anymore.

You will need a license file. For academic use you can request an academic license from the gurobi-website or use the RWTH-ITC's floating license by configuring a license-file (`gurobi.lic` in your home-directory, or in the root-directory of your project).
In order to use the floating license you need to be connected to the RWTH network (either by VPN or directly).

## Usage

In order to run the test cases you will need the pytest module (`pip install pytest`). If using pytest in PyCharm, you can set-up pytest as the default test runner in `Settings > Tools > Python Integrated Tools > Testing`.
