import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_local_import.plugin import (
    BuiltinModulesDisallowedPluginError,
    ExternalPackagesDisallowedPluginError,
    LocalImportBeginningMethodBodyPluginError,
    LocalImportPluginConfig, LocalImportPluginVisitor
)


@pytest.mark.parametrize('code', [
    pytest.param(
        """
        def func():
            statement
        
            from some_package.module import A
        """,
        id='Import from after statement'
    ),
    pytest.param(
        """
        def func():
            statement
    
            import some_package
        """,
        id='Import after statement'
    ),
    pytest.param(
        """
        def func():
            statement
        
            if a > 1:
                from some_package.module import A
        """,
        id='Import from inside statement'
    ),
    pytest.param(
        """
        def func():
            statement
        
            if a > 1:
                import some_package
        """,
        id='Import inside statement'
    )
])
def test_code_with_error(code: str):
    assert_error(
        LocalImportPluginVisitor,
        code,
        LocalImportBeginningMethodBodyPluginError,
        config=LocalImportPluginConfig(application_import_names=['some_package'])
    )


code_without_error = """
def func():
    from some_package import A
    
    statement
"""


def test_code_without_error():
    assert_not_error(
        LocalImportPluginVisitor,
        code_without_error,
        config=LocalImportPluginConfig(application_import_names=['some_package'])
    )


@pytest.mark.parametrize('code', [
    pytest.param(
        """
        def func():
            from external_package.module import A
        """,
        id='Import from external package'
    ),
    pytest.param(
        """
        def func():
            import external_package
        """,
        id='Import external package'
    )
])
def test_code_external_packages_disallowed(code: str):
    assert_error(
        LocalImportPluginVisitor,
        code,
        ExternalPackagesDisallowedPluginError,
        config=LocalImportPluginConfig(application_import_names=['some_package'])
    )


@pytest.mark.parametrize('code', [
    pytest.param(
        """
        def func():
            from sys import float_info
        """,
        id='Import from builtin module'
    ),
    pytest.param(
        """
        def func():
            import os
        """,
        id='Import builtin module'
    )
])
def test_code_builtin_modules_disallowed(code: str):
    assert_error(
        LocalImportPluginVisitor,
        code,
        BuiltinModulesDisallowedPluginError,
        config=LocalImportPluginConfig(application_import_names=['some_package'])
    )
