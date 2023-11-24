#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the compile time function information.

from __future__ import annotations

from typing import List

from .ast_node_function_parameter import AstNodeFunctionParameter
from .macal_conversions import convertToHexAddr


class CTFunction:
    def __init__(self, start_address: int, name: str) -> CTFunction:
        self.start_address: int = start_address
        self.name: str = name
        self.return_type: str = ""
        self.external: bool = False
        self.module: str = ""
        self.function: str = ""
        self.rsp_offset: int = 0
        self.rbp_offset: int = 0
        self.parameters: List[AstNodeFunctionParameter] = []

    def __str__(self) -> str:
        return f"CTFunction({convertToHexAddr(self.start_address)}, {self.name}, {self.rsp_offset}, {self.rbp_offset}, {len(self.parameters)})"

    def __repr__(self) -> str:
        return self.__str__()

