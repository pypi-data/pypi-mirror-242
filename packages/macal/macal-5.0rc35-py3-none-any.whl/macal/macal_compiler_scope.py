from __future__ import annotations
from typing import Optional

from .macal_variable import MacalVariable
from .ast_nodetype import AstNodetype

class NewScope:
    def __init__(self, name: str) -> NewScope:
        self.name = name
        self.parent: NewScope = None
        self.root: NewScope = self
        self.children = []
        self.variables = []
        self.function_aliasses = []
        self.labels = []
        self.jump_table = []
        self.switch_jump_tables = []
        self.functions = []
        self.is_function: bool = False
        self.is_extern_function_definition: bool = False
        self.function_definition: list = []
        self.libraries: list[str] = []
        self.is_library: bool = False

    def __str__(self) -> str:
        return f"{self.name}({self.parent.name if self.parent is not None else None}) {self.is_function} {self.is_function_definition}"

    def add_child(self, child: NewScope):
        self.children.append(child)
        child.parent = self
        child.root = self.root

    def new_child(self, name: str) -> NewScope:
        child = NewScope(name)
        self.add_child(child)
        return child
    
    def get_child(self, name: str) -> Optional[NewScope]:
        return next((child for child in self.children if child.name == name), None)

    def get_variable(self, name: str) -> Optional[MacalVariable]:
        var = next((var for var in self.variables if var.name == name), None)
        if var is not None:
            return var
        if not self.is_library:
            for lib in self.root.libraries:
                library = self.root.get_child(lib)
                var = library.get_variable(name)
                if var is not None:
                    return var
        if self.is_function or self.is_function:
            return None
        if self.parent is not None and not self.is_library:
            return self.parent.get_variable(name)
        return None
        
    def new_variable(self, name: str) -> MacalVariable:
        var = MacalVariable(name, self)
        var.value = AstNodetype.NIL
        self.variables.append(var)
        return var

    def discard_child(self, child: NewScope):
        self.children.remove(child)
        child.parent = None


