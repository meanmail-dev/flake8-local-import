import argparse
import ast
from functools import cached_property
from typing import Any, List, Optional, Union

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Error, Plugin, Visitor
from flake8_plugin_utils.plugin import TConfig

from flake8_local_import.constants import BUILTIN_MODULE_NAMES


class LocalImportBeginningMethodBodyPluginError(Error):
    code = 'LI100'
    message = 'Local import must be at the beginning of the method body'


class ExternalPackagesDisallowedPluginError(Error):
    code = 'LI101'
    message = 'Packages from external modules should not be imported locally'


class BuiltinModulesDisallowedPluginError(Error):
    code = 'LI102'
    message = 'Packages from standard modules should not be imported locally'


class LocalImportPluginVisitor(Visitor):
    @cached_property
    def app_import_names(self) -> List[str]:
        return self.config.app_import_names

    def visit(self, node: ast.AST) -> Any:
        previous = None
        for child in ast.iter_child_nodes(node):
            child.parent = node
            child.previous = previous
            previous = child

        return super().visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for name in node.names:
            self.assert_external_module(node, name.name or '')

        return self.visit_import(node)

    def assert_external_module(self, node: ast.stmt, module: str) -> None:
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.Module):
            return

        module_prefix = module + '.'

        is_app_module = getattr(node, 'level', 0) != 0 or any(
            module_prefix.startswith(app_module + '.')
            for app_module in self.app_import_names
        )
        is_builtin_module = module.split('.')[0] in BUILTIN_MODULE_NAMES

        if is_app_module:
            return

        if not is_builtin_module:
            self.error_from_node(
                ExternalPackagesDisallowedPluginError, node
            )
        else:
            self.error_from_node(
                BuiltinModulesDisallowedPluginError, node
            )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        self.assert_external_module(node, node.module or '')

        return self.visit_import(node)

    def visit_import(self, node: Union[ast.Import, ast.ImportFrom]) -> Any:
        parent = getattr(node, 'parent', None)
        if isinstance(parent, ast.Module):
            return self.generic_visit(node)

        previous = getattr(node, 'previous', None)

        if (not isinstance(parent, ast.FunctionDef) or
            not isinstance(previous, (ast.Import, ast.ImportFrom, ast.arguments))):
            self.error_from_node(LocalImportBeginningMethodBodyPluginError, node)

        return self.generic_visit(node)


class LocalImportPluginConfig:
    def __init__(self, app_import_names: List[str]):
        self.app_import_names = app_import_names


class LocalImportPlugin(Plugin):
    name = 'flake8_local_import'
    version = '1.0.3'
    visitors = [LocalImportPluginVisitor]

    @classmethod
    def add_options(cls, options_manager: OptionManager):
        options_manager.add_option(
            '--app-import-names',
            default='',
            type=str,
            comma_separated_list=True,
            parse_from_config=True
        )

    @classmethod
    def parse_options_to_config(cls, option_manager: OptionManager,
                                options: argparse.Namespace,
                                args: List[str]) -> Optional[TConfig]:
        return LocalImportPluginConfig(
            app_import_names=options.app_import_names
        )
