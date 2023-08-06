![test](https://github.com/davips/packagit/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/packagit/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/packagit)

# packagit
Increment version, create and push tag for release on github and pypi

## Installation
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI
pip install packagit
```

## Setup
Write your first version number inside the setup.py of your project in the form:

```python
VERSION = "0.2101.0"  # major.YYMM.minor
```

Copy the workflow file (release.yml) to the .github/workflows folder of your project repository.
Copy an (empty?) changelog.txt to the root of your project repository.

## Usage
Run at the shell prompt

```bash
packagit 0  # 0 is the major version number, the minor number will be automatically incremented.
```

