import textwrap

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
        textwrap.dedent("""
        def func():
            statement
        
            from app_package.module import A
        """),
        id='Import from after statement'
    ),
    pytest.param(
        textwrap.dedent("""
        def func():
            statement
    
            import app_package
        """),
        id='Import after statement'
    ),
    pytest.param(
        textwrap.dedent("""
        def func():
            statement
        
            if a > 1:
                from app_package.module import A
        """),
        id='Import from inside statement'
    ),
    pytest.param(
        textwrap.dedent("""
        def func():
            statement
        
            if a > 1:
                import app_package
        """),
        id='Import inside statement'
    ),
    pytest.param(
        textwrap.dedent("""
    def func():
        statement

        from app_package.module import A
    """),
        id='Import from after statement'
    ),
    pytest.param(
        textwrap.dedent("""
    def func():
        statement

        import app_package
    """),
        id='Import after statement'
    ),
    pytest.param(
        textwrap.dedent("""
        def func():
            statement

            from .module import A
        """),
        id='Relative import from after statement'
    ),
    pytest.param(
        textwrap.dedent("""
    def func():
        statement

        if a > 1:
            from .module import A
    """),
        id='Relative import from inside statement'
    ),
])
def test_code_with_error(code: str):
    assert_error(
        LocalImportPluginVisitor,
        code,
        LocalImportBeginningMethodBodyPluginError,
        config=LocalImportPluginConfig(application_import_names=['app_package'])
    )


@pytest.mark.parametrize('code', [
    pytest.param(
        textwrap.dedent("""
        def func():
            from app_package import A
            
            statement
        """), id='Import from after statement'
    ),
    pytest.param(
        textwrap.dedent("""
    def func():
        from .. import A

        statement
    """), id='Import from after statement'
    )
])
def test_code_without_error(code: str):
    assert_not_error(
        LocalImportPluginVisitor,
        code,
        config=LocalImportPluginConfig(application_import_names=['app_package'])
    )


@pytest.mark.parametrize('code', [
    pytest.param(
        textwrap.dedent("""
        def func():
            from external_package.module import A
        """),
        id='Import from external package'
    ),
    pytest.param(
        textwrap.dedent("""
        def func():
            import external_package
        """),
        id='Import external package'
    )
])
def test_code_external_packages_disallowed(code: str):
    assert_error(
        LocalImportPluginVisitor,
        code,
        ExternalPackagesDisallowedPluginError,
        config=LocalImportPluginConfig(application_import_names=['app_package'])
    )


@pytest.mark.parametrize('code', [
    pytest.param(
        textwrap.dedent("""
        def func():
            from sys import float_info
        """),
        id='Import from builtin module'
    ),
    pytest.param(
        textwrap.dedent("""
        def func():
            import os
        """),
        id='Import builtin module'
    )
])
def test_code_builtin_modules_disallowed(code: str):
    assert_error(
        LocalImportPluginVisitor,
        code,
        BuiltinModulesDisallowedPluginError,
        config=LocalImportPluginConfig(application_import_names=['app_package'])
    )
