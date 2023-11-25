#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the runtime scope for the Macal virtual machine
#
# The primary function of this class is to provide a scope for the Macal virtual machine.
# It is used to store the values of the pre-defined variables, if there are any.

from __future__ import annotations

from typing import Any, List, Optional, Tuple

from .ast_nodetype import AstNodetype
from .macal_variable import MacalVariable
from .macal_conversions import typeFromValue


class RuntimeScope:
    def __init__(self) -> RuntimeScope:
        self.name: str = "runtime"
        self.variables: List[MacalVariable] = []
        self.do_break: bool = False
        self.do_continue: bool = False
        self.do_return: bool = False
        self.return_addr: int = 0
        self.continue_addr: int = 0
        self.break_addr: int = 0
        self.rbp_offset: int = 0
        self.child_count: int = 0
        self.return_value_rsp: int = -1
        self.return_address_rsp: int = -1
        self.arg_count: int = 0
        self.arg_rsp: int = -1
        self.children: List[RuntimeScope] = []
        self.parent: Optional[RuntimeScope] = None

    def DefineVariable(self, name: str, stack_index: int, stack_offset: int = 0) -> MacalVariable:
        var = MacalVariable(name, self)
        var.stack_index = stack_index
        var.stack_offset = stack_offset
        self.variables.append(var)
        return var

    def GetVariable(self, name: str) -> Optional[MacalVariable]:
        return next((var for var in self.variables if var.name == name), None)

    def SetVariable(self, name: str, value: Any) -> None:
        var = self.GetVariable(name)
        if var is None:
            raise Exception(f"Runtime Error: Variable {name} does not exist.")
        var.value = value
        var.node_type = typeFromValue(value)

    def CreateChild(self) -> RuntimeScope:
        child = RuntimeScope()
        child.name = f"{self.name}_child_{len(self.children)}"
        child.parent = self
        self.children.append(child)
        return child
    
    def DiscardChild(self, child: RuntimeScope) -> None:
        self.children.remove(child)
