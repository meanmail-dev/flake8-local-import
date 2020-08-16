from _ast import Import, Name
from typing import Any

from flake8_plugin_utils import Error, Plugin, Visitor


class LocalImportBeginningMethodBodyPluginError(Error):
    code = 'LI100'
    message = 'Local import must be at the beginning of the method body'


class LocalImportPluginVisitor(Visitor):
    def visit_Import(self, node: Import) -> Any:
        if (isinstance(node.func, Name) and
            node.func.id == 'super' and
            node.args):
            self.error_from_node(LocalImportBeginningMethodBodyPluginError, node)

        return self.generic_visit(node)


class LocalImportPlugin(Plugin):
    name = 'flake8_local_import'
    version = '1.0.0'
    visitors = [LocalImportPluginVisitor]
