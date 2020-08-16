from flake8_plugin_utils import assert_error, assert_not_error

from flake8_local_import.plugin import (
    LocalImportBeginningMethodBodyPluginError, LocalImportPluginVisitor
)

code_with_error = """
def func():
    statement

    from some_package import A

"""


def test_code_with_error():
    assert_error(
        LocalImportPluginVisitor,
        code_with_error,
        LocalImportBeginningMethodBodyPluginError
    )


code_without_error = """
def func():
    from some_package import A
    
    statement
"""


def test_code_without_error():
    assert_not_error(LocalImportPluginVisitor, code_without_error)
