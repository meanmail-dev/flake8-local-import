# flake8-local-import
[![Downloads](https://pepy.tech/badge/flake8-local-import/month)](https://pepy.tech/project/flake8-super/month)
![PyPI](https://img.shields.io/pypi/v/flake8-local-import)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-local-import)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/flake8-local-import)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/flake8-local-import)

Python 3 check local import for flake8

# Installation

```bash
pip install flake8-local-import
```

# Configuration

No configuration required


# Example

```python3
#  Error
def func():
    statement

    from some_package import A   # LI100 Local import must be at the beginning of the method body


# Good
def func():
    from some_package import A

    statement

```


# Error codes

|code|description|
|---|---|
|LI100|Local import must be at the beginning of the method body|


# Links

https://github.com/meanmail-dev/flake8-local-import

https://meanmail.dev/