#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# Decompiler for Macal VM instructionset.

from __future__ import annotations

from .ast_nodetype import AstNodetype
from .macal_conversions import convertToHexAddr
from .macal_instructions import MacalInstruction, MacalInstructionList

import pyximport; pyximport.install()
from .cmacal_vm import MacalVm


class MacalDecompiler:
    def __init__(self, filename: str, verbose: bool = False) -> MacalDecompiler:
        self.vm: MacalVm = MacalVm(filename)
        self.vm.rip.value = 0
        self.instructions: MacalInstructionList = MacalInstructionList()
        self.metadata: dict = {}
        self.labels: list = []
        self.verbose: bool = verbose
        if filename is not None:
            lm = len(self.vm.memory) - 1
            data = []
            if self.vm.memory[lm][0] == 77:
                data = self.vm.memory[lm]
            elif self.vm.memory[lm - 1][0] == 77:
                data = self.vm.memory[lm - 1]
            if data != []:
                self.metadata = data[1]
                self.labels = self.metadata["LABELS"]

    def __PrintLabels(self, addr: int) -> None:
        flag = False
        for label in self.labels:
            if label[1] == addr:
                print(f"{label[0]}:", end=" ")
                flag = True
        if flag is True:
            print()

    def Decompile(self):
        addr = 0
        print()
        print(f"Decompiling: {self.vm.filename}")
        print()
        print("Address       Instruction")
        self.vm.rsp.value = 0
        self.vm.rbp.value = 0
        while addr < len(self.vm.memory):
            self.__PrintLabels(addr)
            opcode = self.vm.memory[addr]
            op: MacalInstruction = self.instructions.fromOpcode(opcode[0])
            output = f"{convertToHexAddr(addr)}    {op.Name:<6} "
            n = 1
            for operand in op.Operands:
                if n > 1:
                    output += ", "
                if operand == "addr":
                    output += convertToHexAddr(opcode[n])
                elif operand == "[addr]":
                    output += f"[{convertToHexAddr(opcode[n])}]"
                elif operand.startswith("reg"):
                    output +=  f"{self.vm.opcode_to_register_map[opcode[n]].name}"
                elif operand == "imm":
                    if opcode[0] != 80:
                        value = f"{opcode[n+1]}"
                        if opcode[n] == AstNodetype.STRING:
                            value = value.replace("\n", "\\n")  # escape newlines
                            value = value.replace("\r", "\\r")  # escape cr
                            value = f'"{value}"'
                        output +=  f"{opcode[n].name} {value.strip()}"
                    else:
                        output +=  f"{opcode[n]}"
                    n += 1
                elif (
                    operand == "errmsg"
                    or operand == "module"
                    or operand == "function"
                    or operand == "paramcount"
                    or operand == "offset"
                ):
                    output += f"{opcode[n]}"
                elif operand == "metadata":
                    output += "METADATA"
                elif operand == "type":
                    output += opcode[n].name
                elif operand == "str":
                    output += f'"{opcode[n]}"'
                else:
                    raise Exception(f"Unknown operand: {operand}")
                n += 1
            output = output.ljust(40)
            if op.Name == "XOR" and opcode[1] == opcode[2]:
                reg = self.vm.opcode_to_register_map[opcode[1]]
                reg.value = 0
            if op.Name == "MOVRI":
                reg = self.vm.opcode_to_register_map[opcode[1]]
                reg.value = opcode[3]
            if op.Name == "MOVRR":
                reg1 = self.vm.opcode_to_register_map[opcode[1]]
                reg2 = self.vm.opcode_to_register_map[opcode[2]]
                reg1.value = reg2.value
                if reg1.name == "RSP" or reg1.name == "RBP":
                    output += f" ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
            if op.Name == "PUSH":
                self.vm.rsp.value += 1
                reg = self.vm.opcode_to_register_map[opcode[1]]
                self.vm.stack.append(reg.value)
                output += f" (stack[{self.vm.rsp.value-1}] << {reg.name} = {reg.value}) ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
            if op.Name == "POP":
                if not isinstance(self.vm.rsp.value, int):
                    output += 'ERROR: rsp not an int\n'
                else:
                    while len(self.vm.stack) >= self.vm.rsp.value:
                        if len(self.vm.stack) == 0:
                            break
                        self.vm.stack.pop()
                    self.vm.rsp.value -= 1
                    reg = self.vm.opcode_to_register_map[opcode[1]]
                    if len(self.vm.stack) > 0:
                        reg.value = self.vm.stack.pop()
                output += f" (stack[{self.vm.rsp.value}] >> {reg.name} = {reg.value}) ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
            if op.Name == "STORR":
                reg1 = self.vm.opcode_to_register_map[opcode[1]]
                offs = opcode[2]
                reg2 = self.vm.opcode_to_register_map[opcode[3]]
                value = f"<invalid offset> ({reg1.value} + {offs})"
                if reg1.value is not None and reg1.value + offs >= 0 and reg1.value + offs < len(self.vm.stack):
                    self.vm.stack[reg1.value + offs] = reg2.value
                    value = reg1.value + offs
                    output += f" (stack[{reg1.value + offs}] << {reg2.name} = {reg2.value}) ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
                else:
                    output += f" (stack[{value}] << {reg2.name} = {reg2.value}) ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
            if op.Name == "LOADR":
                reg1 = self.vm.opcode_to_register_map[opcode[1]]
                reg2 = self.vm.opcode_to_register_map[opcode[2]]
                offs = opcode[3]
                value = ""
                pof = f"<invalid offset {reg2.value} + {offs}>"
                if isinstance(reg2.value, int):
                    if reg2.value + offs > 0 and reg2.value + offs < len(self.vm.stack):
                        value = self.vm.stack[reg2.value + offs]
                        reg1.value = value
                        pof = reg2.value + offs
                output += f" (stack[{pof}] >> {reg1.name} = {value}) ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
            if op.Name == "LEN":
                reg1 = self.vm.opcode_to_register_map[opcode[1]]
                if isinstance(reg1.value, list) or isinstance(reg1.value, str) or isinstance(reg1.value, dict):
                    output += f" {reg1.name} ({reg1.value})  << {len(reg1.value)}"
                    reg1.value = len(reg1.value)
                else:
                    output += f" {reg1.name} ({reg1.value})  << len(<invalid type>)"
            elif op.Name == "FEINDEX":
                if isinstance(self.vm.rax.value, dict):
                    output += f" RAX  << {list(self.vm.rax.value.keys())[self.vm.rbx.value]}"
                    self.vm.rax.value = list(self.vm.rax.value.keys())[self.vm.rbx.value]
                else:
                    if not (isinstance(self.vm.rax.value, list) or isinstance(self.vm.rax.value, str)):
                        output += f" RAX << RAX[<invalid type>]"
                    elif self.vm.rbx.value < 0 or self.vm.rbx.value >= len(self.vm.rax.value):
                        output+= f"RAX << <invalid index {self.vm.rbx.value}> (0..{len(self.vm.rax.value)-1})"
                    else:
                        output += f" RAX << {self.vm.rax.value[self.vm.rbx.value]}"
                        self.vm.rax.value = self.vm.rax.value[self.vm.rbx.value]
            elif op.Name == "RESERVE":
                self.vm.rsp.value += opcode[1]
                self.vm.stack.extend([None] * opcode[1])
                output += f" ; RSP = {self.vm.rsp.value} ; RBP = {self.vm.rbp.value} ; stacksize = {len(self.vm.stack)}"
            print(output)
            addr += 1
        print()
        print(f"Finished decompiling: {self.vm.filename}")
        print()
