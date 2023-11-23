# How to Build a Python Package and deploy to PyPI

## Pre requisite
- PyPI account
- pip3 install wheel
- pip3 install twine
- Get licence from https://choosealicense.com/

## Project structure
```text
base +
     |
     + LICENSE.txt
     + README.md
     + setup.py
     + app +
           |
           + trianz +
                    + __init__.py
                    + generator.py
```

## Package build
```shell
python3 setup.py bdist_wheel        # includes only binary
# OR
python3 setup.py sdist bdist_wheel  # includes source code and binary
```

## Local install
```shell
pip3 install .
```

## Check whether project is compatible to upload
```shell
twine check dist/*
```

## Test upload to TestPyPI repository
```shell
twine upload -r testpypi dist/*
```

## Upload to PyPI repository
```shell
twine upload dist/*
```
