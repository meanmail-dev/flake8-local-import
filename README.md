# flake8-local-import
[![Downloads](https://pepy.tech/badge/flake8-local-import/month)](https://pepy.tech/project/flake8-local-import/month)
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

You will want to set the `application-import-names` option to a comma separated
list of names that should be considered local to your application. Note that
relative imports are always considered local.


# Example

```python3
#  Error
def func():
    statement

    from app_package import A   # LI100 Local import must be at the beginning of the method body


#  Error
def func():
    statement

    from app_package import A   # LI100 Local import must be at the beginning of the method body


# Good
def func():
    from app_package import A

    statement

```


# Error codes

|code|description|
|---|---|
|LI100|Local import must be at the beginning of the method body|
|LI101|Packages from external modules should not be imported locally|
|LI102|Packages from standard modules should not be imported locally|


# Links

https://github.com/meanmail-dev/flake8-local-import

https://meanmail.dev/
