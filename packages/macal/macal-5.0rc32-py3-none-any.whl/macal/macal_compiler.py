#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the bytcode compiler for Macal

from __future__ import annotations

import os
import sys
from typing import List, Optional

from .ast_node_assignment import AstNodeAssignmentStatement
from .ast_node_binary_expression import AstNodeBinaryExpression
from .ast_node_block import AstNodeBlock
from .ast_node_break_statement import AstNodeBreakStatement
from .ast_node_continue_statement import AstNodeContinueStatement
from .ast_node_elif_statement import AstNodeElifStatement
from .ast_node_else_statement import AstNodeElseStatement
from .ast_node_expression import AstNodeExpression
from .ast_node_foreach_statement import AstNodeForeachStatement
from .ast_node_function_call_expression import AstNodeFunctionCallExpression
from .ast_node_function_call_statement import AstNodeFunctionCallStatement
from .ast_node_function_definition import AstNodeFunctionDefinition
from .ast_node_function_parameter import AstNodeFunctionParameter
from .ast_node_halt_statement import AstNodeHaltStatement
from .ast_node_if_statement import AstNodeIfStatement
from .ast_node_include_statement import AstNodeIncludeStatement
from .ast_node_indexed_variable_expression import AstNodeIndexedVariableExpression
from .ast_node_istype import AstNodeIsType
from .ast_node_literal_expression import AstNodeLiteralExpression
from .ast_node_print_statement import AstNodePrintStatement
from .ast_node_program import AstNodeProgram
from .ast_node_register_expression import AstNodeRegisterExpression
from .ast_node_return_statement import AstNodeReturnStatement
from .ast_node_select_statement import AstNodeSelectStatement
from .ast_node_statement import AstNodeStatement
from .ast_node_type_statement import AstNodeTypeStatement
from .ast_node_unary_expression import AstNodeUnaryExpression
from .ast_node_variable_expression import AstNodeVariableExpression
from .ast_node_debug_variable_statement import AstNodeDebugVariableStatement
from .ast_node_variable_function_call_expression import (
    AstNodeVariableFunctionCallExpression,
)
from .ast_node_while_statement import AstNodeWhileStatement
from .ast_nodetype import AstNodetype
from .bytecode_optimizer import BytecodeOptimizer
from .bytecode_register import BytecodeRegister
from .compiler_scope import CompilerScope
from .config import SearchPath
from .ct_function import CTFunction
from .ct_variable import CTVariable
from .lex_token import LexToken
from .macal_instruction_emitter import MacalInstructionEmitter
from .macal_instructions import Opcode
from .macal_lexer import Lexer
from .macal_parser import Parser
from .switch_case_table import SwitchCaseTable

import pyximport; pyximport.install()
from .cmacal_vm import MacalVm

# Function stack layout:

# -6 PARAMETER 0
# -5 PARAMETER 1
# -4 PARAMCOUNT
# -3 RETURN VALUE
# -2 RETURN ADDRESS
# -1 RBP

FUNCTION_CALL_PARAMETER_STACK_OFFSET = -5
FUNCTION_CALL_PARAMETER_COUNT_STACK_OFFSET = -4
FUNCTION_CALL_RETURN_VALUE_STACK_OFFSET = -3
FUNCTION_CALL_RETURN_ADDRESS_STACK_OFFSET = -2
FUNCTION_CALL_PREVIOUS_RBP_STACK_OFFSET = -1


class MacalCompiler:
    def __init__(
        self,
        program: Optional[AstNodeProgram] = None,
        output_path: Optional[str] = None,
        verbose: bool = False,
        debug: bool = False,
        reserved_vars: List[str] = []
    ) -> MacalCompiler:
        self.program: Optional[AstNodeProgram] = program
        self.output_path: Optional[str] = output_path
        self.output_file: Optional[str] = None
        self.cs: MacalVm = MacalVm()  # Code segment
        self.emitter: MacalInstructionEmitter = MacalInstructionEmitter(self.cs.memory, self.cs.rip, self.cs.rsp, self.cs.rbp, self.cs.stack)
        self.scope: CompilerScope = None
        self.do_raise: bool = True
        self.debug = debug
        compiler_path = os.path.dirname(__file__)
        lib_path = os.path.join(compiler_path, "lib")
        if lib_path not in SearchPath:
            SearchPath.append(lib_path)
        if compiler_path not in SearchPath:
            SearchPath.append(compiler_path)
        self.reserved_vars = reserved_vars
        self.verbose: bool = verbose

    def error(self, message: str) -> None:
        msg = f"Compiler Error: {message} in file {self.program.filename}"
        if self.do_raise:
            raise Exception(msg)
        print(msg)
        sys.exit(1)

    def compile(self) -> None:
        self.cs.Reset()
        # we need to start at an offset of 2 because exit code
        # and return address zero are on the stack and not to be touched.
        self.emitter.XOR(self.cs.rax, self.cs.rax)  # xor rax, rax rax = 0, zero = true
        self.emitter.PUSH(self.cs.rax) # exit code
        self.emitter.PUSH(self.cs.rax) # return address 0 to halt execution.
        self.scope = self.emit_scope(None)
        self.compile_reserved_variables(self.scope)
        self.compile_program(self.program, self.scope)
        self.emit_scope_end(self.scope)
        self.emitter.RET()
        self.__resolve_jumps_and_labels__(self.scope)
        self.cs.memory = self.emitter.memory  # fix the memory problem...
        # opt = BytecodeOptimizer(self.cs, self.scope)
        # opt.process()
        if self.verbose:
            self.compile_datasegment(self.scope)
        if len(self.scope.variables) > 0:
            self.compile_reserved_segment()
        self.cs.Save(self.output_path, self.cs.rip.value)

    def compile_reserved_segment(self) -> None:
        pvars = []
        n = 0
        for var in self.reserved_vars:
            pvars.append((var, n))
            n += 1
        metadata = {"VARIABLES": [], "FUNCTIONS": [], "LIBRARIES": [], "LABELS": [], "JUMPS": [], "RESERVED": pvars}
        self.emitter.RESERVEDS(metadata)       

    def compile_interactive(self, ast: AstNodeProgram) -> None:
        self.compile_block(ast, self.scope)
        self.__resolve_jumps_and_labels__(self.scope)
        if self.verbose:
            self.compile_datasegment(self.scope)

    def compile_reserved_variables(self, scope: CompilerScope) -> None:
        """This adds pre-defined variables onto the stack."""
        if self.reserved_vars is None:
            return
        stack_index = self.cs.rsp.value
        for var in self.reserved_vars:
            scope.define_variable(var.strip(), stack_index)
            stack_index += 1
        self.emitter.RESERVE(len(self.reserved_vars)) # reserve space for variables.
        self.cs.rsp.value += len(self.reserved_vars)

    def __resolve_jumps_and_labels__(self, scope: CompilerScope) -> None:
        for jump in scope.jump_table:
            jaddr: int = jump.address
            laddr: int = scope.labels[jump.label].address
            op = self.emitter.memory[jaddr]
            new_op = (op[0], laddr)
            self.emitter.memory[jaddr] = new_op

        for switch_case_table in scope.switch_jump_tables:
            for case, label in switch_case_table.labels.items():
                laddr: int = scope.labels[label].address
                switch_case_table.labels[case] = laddr

            op = self.emitter.memory[switch_case_table.address]
            new_op = (op[0], op[1], op[2], switch_case_table.labels)
            self.emitter.memory[switch_case_table.address] = new_op

    def compile_program(self, program: AstNodeProgram, scope: CompilerScope) -> None:
        label_main = scope.get_new_label("main")
        label_exit = scope.get_new_label("exit")
        scope.set_label_address(label_main, self.cs.rip.value)
        self.compile_block(program, scope)
        scope.set_label_address(label_exit, self.cs.rip.value)

    def compile_block(self, block: AstNodeBlock, scope: CompilerScope) -> None:
        for statement in block.statements:
            self.compile_statement(statement, scope)

    def compile_statement(self, statement: AstNodeStatement, scope: CompilerScope) -> None:
        if statement.expr_type == AstNodetype.IF_STATEMENT:
            self.compile_if_statement(statement, scope)
        elif statement.expr_type == AstNodetype.FOREACH_STATEMENT:
            self.compile_foreach_statement(statement, scope)
        elif statement.expr_type == AstNodetype.WHILE_STATEMENT:
            self.compile_while_statement(statement, scope)
        elif statement.expr_type == AstNodetype.CONTINUE_STATEMENT:
            self.compile_continue_statement(statement, scope)
        elif statement.expr_type == AstNodetype.BREAK_STATEMENT:
            self.compile_break_statement(statement, scope)
        elif statement.expr_type == AstNodetype.RETURN_STATEMENT:
            self.compile_return_statement(statement, scope)
        elif statement.expr_type == AstNodetype.SELECT_STATEMENT:
            self.compile_select_statement(statement, scope)
        elif statement.expr_type == AstNodetype.HALT_STATEMENT:
            self.compile_halt_statement(statement, scope)
        elif statement.expr_type == AstNodetype.INCLUDE_STATEMENT:
            self.compile_include_statement(statement, scope)
        elif statement.expr_type == AstNodetype.PRINT_STATEMENT:
            self.compile_print_statement(statement, scope)
        elif statement.expr_type == AstNodetype.SWITCH_STATEMENT:
            self.compile_switch_statement(statement, scope)
        elif statement.expr_type == AstNodetype.ASSIGNMENT_STATEMENT:
            self.compile_assignment_statement(statement, scope)
        elif statement.expr_type == AstNodetype.FUNCTION_CALL:
            self.compile_function_call(statement, scope)
        elif statement.expr_type == AstNodetype.FUNCTION_DEFINITION:
            self.compile_function_definition(statement, scope)
        elif statement.expr_type == AstNodetype.FUNCTION_CALL_EXPRESSION:
            self.compile_function_call_expression(statement, scope)
        elif statement.expr_type == AstNodetype.DEBUG_VARIABLE_STATEMENT:
            self.compile_debug_variable_statment(statement, scope)
        elif statement.expr_type == AstNodetype.DEBUG_STACK_STATEMENT:
            self.emitter.STACK()
        elif statement.expr_type == AstNodetype.DEBUG_REGISTERS_STATEMENT:
            self.emitter.REGS()
        else:
            self.error(
                f"Unknown statement type {statement.expr_type} at {statement.line}:{statement.column} scope({scope.name})"
            )

    # code writing helpers.

    def emit_condition(self, label: int, conditional_jump: int, scope: CompilerScope) -> None:
        self.emitter.POP(self.cs.rax)  # pop rax
        self.emitter.CMPRI(self.cs.rax, AstNodetype.BOOLEAN, True)  # cmpir rax, True
        self.emit_jump(conditional_jump, label, scope)  # jmpnz label

    def emit_new_label(self, name: str, scope: CompilerScope) -> int:
        lbl = scope.root.get_new_label(name)
        scope.root.set_label_address(lbl, self.cs.rip.value)
        return lbl

    def emit_scope(self, scope: CompilerScope) -> CompilerScope:
        self.emitter.PUSH(self.cs.rbp)
        self.emitter.MOVRR(self.cs.rbp, self.cs.rsp)
        child: CompilerScope = None
        if scope is None:
            child = CompilerScope("root", None)
            child.rbp_offset = self.cs.rbp.value
        else:
            child = scope.new_child(f"scope", self.cs.rbp.value)
        return child

    def emit_scope_end(self, scope: CompilerScope) -> None:
        self.emitter.MOVRR(self.cs.rsp, self.cs.rbp)
        self.emitter.POP(self.cs.rbp)
        scope.discard()

    def emit_jump(self, opcode: int, label: int, scope: CompilerScope) -> None:
        if label is None:
            self.error(f"Label is None at RIP {self.cs.rip.value}")
        scope.root.new_jump(self.cs.rip.value, label)
        if opcode == Opcode.JMP:
            self.emitter.JMP(label)
        elif opcode == Opcode.JMPZ:
            self.emitter.JMPZ(label)
        elif opcode == Opcode.JMPNZ:
            self.emitter.JMPNZ(label)
        elif opcode == Opcode.JMPGT:
            self.emitter.JMPGT(label)
        elif opcode == Opcode.JMPGTE:
            self.emitter.JMPGTE(label)
        elif opcode == Opcode.JMPLT:
            self.emitter.JMPLT(label)
        elif opcode == Opcode.JMPLTE:
            self.emitter.JMPLTE(label)
        elif opcode == Opcode.DJNZ:
            self.emitter.DJNZ(label)
        else:
            self.error(f"Unknown jump opcode {opcode} at {self.cs.rip.value}")

    # expression helper functions.

    def var_to_stack(self, var: CTVariable, scope: CompilerScope) -> None:
        if var.arg:
            self.emitter.LOADR(self.cs.rax, self.cs.rbp, var.stack_index) # load rax, [rbp + stack_offset]
        else:
            self.emitter.LOAD(self.cs.rax, var.stack_index)  # load rax, stack[stack_index]
        self.emitter.PUSH(self.cs.rax)  # push rax

    # compiling statements

    def compile_if_statement(self, statement: AstNodeIfStatement, scope: CompilerScope) -> None:
        self.emit_new_label("if", scope)
        self.compile_expression(statement.condition, scope)
        label_at_the_very_end_of_if = scope.get_new_label("label_end")
        label_for_JMPNZ_in_if = scope.get_new_label("label_jnz")
        self.emit_condition(label_for_JMPNZ_in_if, Opcode.JMPNZ, scope)
        self.compile_block(statement.block, scope)
        self.emit_jump(Opcode.JMP, label_at_the_very_end_of_if, scope)
        scope.set_label_address(label_for_JMPNZ_in_if, self.cs.rip.value)
        if statement.elif_block_list is not None:
            count = len(statement.elif_block_list)
            if count > 0:
                for elif_statement in statement.elif_block_list:
                    self.compile_elif_statement(elif_statement, label_at_the_very_end_of_if, scope)
        if statement.else_block is not None and len(statement.else_block.statements) > 0:
            self.compile_else_statement(statement.else_block, scope)
        scope.set_label_address(label_at_the_very_end_of_if, self.cs.rip.value)

    def compile_elif_statement(self, statement: AstNodeElifStatement, lbl_end: int, scope: CompilerScope) -> None:
        self.emit_new_label("elif", scope)
        self.compile_expression(statement.condition, scope)
        label = scope.root.get_new_label("elif_jnz")
        self.emit_condition(label, Opcode.JMPNZ, scope)
        self.compile_block(statement.statements, scope)
        self.emit_jump(Opcode.JMP, lbl_end, scope)
        scope.set_label_address(label, self.cs.rip.value)
        self.emit_new_label("/elif", scope)

    def compile_else_statement(self, statement: AstNodeElseStatement, scope: CompilerScope) -> None:
        self.emit_new_label("else", scope)
        self.compile_block(statement, scope)
        self.emit_new_label("/else", scope)

    def compile_foreach_statement(self, statement: AstNodeForeachStatement, scope: CompilerScope) -> None:
        foreach_end_label = scope.get_new_label("foreach_loop_end")
        self.emit_new_label("foreach_start", scope)
        foreach_continue_label = scope.get_new_label("foreach_loop_continue")
        foreach_scope = self.emit_scope(scope)
        # get the variable we are iterating over
        self.compile_expression(statement.expr, foreach_scope)  # array is on stack [rbp + 0]
        array_register = self.cs.GetFreeRegister()
        length_register = self.cs.GetFreeRegister()
        index_register = self.cs.GetFreeRegister()
        self.emitter.POP(array_register)  # pop array_register
        self.emitter.LENR(length_register, array_register)
        self.emitter.XOR(index_register, index_register)  # xor rax, rax
        it = foreach_scope.define_variable("it", self.cs.rsp.value)
        it.node_type = AstNodetype.INTEGER
        it.value = 0
        self.emitter.XOR(self.cs.rax, self.cs.rax)  # xor rax, rax
        self.emitter.PUSH(self.cs.rax)  # push variable it  [rbp + 3]
        # preparation is done, we can start the loop:
        foreach_loop_start = self.emit_new_label("foreach_loop_start", scope)
        foreach_scope.continue_label = foreach_continue_label
        foreach_scope.break_label = foreach_end_label
        self.emitter.CMPRR(index_register, length_register)  # cmprr index, length
        # jmpz foreach_end_label if index == length (we are at the end of the array)
        self.emit_jump(Opcode.JMPZ, foreach_end_label, scope)
        self.emitter.MOVRR(self.cs.rax, array_register)  # rax is now the array
        self.emitter.MOVRR(self.cs.rbx, index_register)  # rbox is now the index
        self.emitter.FEINDEX()  # rax = rax[rbx]      # rax is now the value for the variable it
        self.emitter.STOR(it.stack_index, self.cs.rax)  # it is now the value of the array at the current index
        self.compile_block(statement.block, foreach_scope)  # compile the block of the foreach statement.
        scope.set_label_address(foreach_continue_label, self.cs.rip.value)
        self.emitter.INC(index_register)  # inc rax rax = rax + 1
        self.emit_jump(Opcode.JMP, foreach_loop_start, scope.root)  # jmp foreach_loop_start
        scope.set_label_address(foreach_end_label, self.cs.rip.value)
        self.emit_scope_end(foreach_scope)
        self.emit_new_label("foreach_end", scope)
        self.cs.ReleaseRegister(array_register)
        self.cs.ReleaseRegister(length_register)
        self.cs.ReleaseRegister(index_register)

    def compile_while_statement(self, statement: AstNodeWhileStatement, scope: CompilerScope) -> None:
        self.emit_new_label("while", scope)
        loop_start = scope.root.get_new_label("while_loop_start")
        loop_end = scope.root.get_new_label("while_loop_end")
        while_scope = self.emit_scope(scope)
        while_scope.continue_label = loop_start
        while_scope.break_label = loop_end
        scope.set_label_address(loop_start, self.cs.rip.value)
        self.compile_expression(statement.condition, scope)
        self.emit_condition(loop_end, Opcode.JMPNZ, scope)
        self.compile_block(statement.block, while_scope)
        self.emit_jump(Opcode.JMP, loop_start, scope)
        scope.set_label_address(loop_end, self.cs.rip.value)
        self.emit_scope_end(while_scope)

    def compile_continue_statement(self, statement: AstNodeContinueStatement, scope: CompilerScope) -> None:
        if scope.continue_label is None:
            self.error(f"Continue statement not allowed at {statement.line}:{statement.column}")
        self.emit_new_label("continue", scope)
        self.emit_jump(Opcode.JMP, scope.continue_label, scope)

    def compile_break_statement(self, statement: AstNodeBreakStatement, scope: CompilerScope) -> None:
        if scope.break_label is None:
            self.error(f"Break statement not allowed at {statement.line}:{statement.column}")
        self.emit_new_label("break", scope)
        self.emit_jump(Opcode.JMP, scope.break_label, scope)

    def compile_return_statement(self, statement: AstNodeReturnStatement, scope: CompilerScope) -> None:
        if scope.exit_label is None:
            self.error(f"Return statement not allowed at {statement.line}:{statement.column}")
        self.emit_new_label("return", scope)
        if statement.expr is not None:
            self.compile_expression(statement.expr, scope)
            # the function return value is reserved at [rbp - 2]
            self.emitter.POP(self.cs.rax)  # pop rax
            self.emitter.STORR(self.cs.rbp, FUNCTION_CALL_RETURN_VALUE_STACK_OFFSET, self.cs.rax)  # storr [rbp - 3], rax
        # jump to the exit label, the cleanup and the RET are executed there.
        self.emit_jump(Opcode.JMP, scope.exit_label, scope)

    def compile_halt_statement(self, statement: AstNodeHaltStatement, scope: CompilerScope) -> None:
        self.emit_new_label("halt", scope)
        self.compile_expression(statement.expr, scope)
        self.emitter.POP(self.cs.rax)  # pop rax
        self.emitter.STOR(0, self.cs.rax)  # stor stack[0], rax -> rax is the exit code
        self.emitter.HALT()
    
    def compile_debug_variable_statment(self, statement: AstNodeDebugVariableStatement, scope: CompilerScope) -> None:
        var: CTVariable = scope.get_variable(statement.expr.token_value)
        if var is None:
            self.error(f"Unknown variable {statement.expr.token_value} at {statement.line}:{statement.column} scope({scope.name})")        
        self.emitter.DBGVAR(name=statement.expr.token_value, stack_index=var.stack_index)

    def compile_print_statement(self, statement: AstNodePrintStatement, scope: CompilerScope) -> None:
        self.emit_new_label("print", scope)
        for expr in statement.args:
            self.compile_expression(expr, scope)
            self.emitter.POP(self.cs.rax)  # pop rax
            self.emitter.PRNT()
        self.emitter.MOVRI(self.cs.rax, AstNodetype.STRING, "\n")
        self.emitter.PRNT()

    def compile_switch_statement(self, statement: AstNodeStatement, scope: CompilerScope) -> None:
        # A switch statement is basically a jump table.
        # So we need to compile the expression and then jump to the correct label.
        # If there is no match, we jump to the default label.
        switch_end_label = scope.root.get_new_label("switch_end")
        default_label = scope.root.get_new_label("switch_default")

        self.emit_new_label("switch", scope)
        self.compile_expression(statement.expr, scope)
        # The expression result is on the stack now this is the value that we need to match

        # Against each of the case values.
        # So first we build the jump table:
        jump_table = {}
        for case in statement.cases:
            case_label = scope.root.get_new_label("case")
            jump_table[case.case_value()] = case_label

        # Now we can compile the jump table.
        scope.switch_jump_tables.append(SwitchCaseTable(self.cs.rip.value, jump_table))
        self.emitter.MOVRI(self.cs.rax, AstNodetype.RECORD, jump_table)

        # Now we calculate which jump to make.
        self.emitter.POP(self.cs.rbx)  # pop rbx # rbx is the value to match
        self.emitter.HASFLDRR(self.cs.rax, self.cs.rbx)  # hasfldrr rax, rbx. The ZF flag is set if the value is found.
        self.emit_jump(Opcode.JMPNZ, default_label, scope)  # jmpz default_label if the value is not found.
        self.emitter.INDEX()
        self.emitter.JMPR(self.cs.rax)  # jmp rax
        scope.set_label_address(default_label, self.cs.rip.value)
        if statement.default is not None:
            self.compile_block(statement.default.block, scope)
        self.emit_jump(Opcode.JMP, switch_end_label, scope)
        for case in statement.cases:
            scope.set_label_address(jump_table[case.case_value()], self.cs.rip.value)
            self.compile_block(case.block, scope)
            self.emit_jump(Opcode.JMP, switch_end_label, scope)
        scope.set_label_address(switch_end_label, self.cs.rip.value)

    def compile_is_type_statement(self, statement: AstNodeIsType, scope: CompilerScope) -> None:
        # This should cover all the IsXXXX type statements.
        self.emit_new_label("is_type", scope)
        self.compile_expression(statement.expr, scope)
        self.emitter.POP(self.cs.rax)  # pop rax
        self.emitter.CMPRTI(self.cs.rax, statement.TypeToCheck)
        self.emitter.SETZR(self.cs.rax)
        self.emitter.PUSH(self.cs.rax)  # push rax

    def compile_type_statement(self, statement: AstNodeTypeStatement, scope: CompilerScope) -> None:
        self.emit_new_label("Type", scope)
        self.compile_expression(statement.expr, scope)
        self.emitter.POP(self.cs.rax)  # pop rax
        self.emitter.TYPE(self.cs.rax)
        self.emitter.PUSH(self.cs.rax)  # push rax

    def compile_assignment_statement(self, statement: AstNodeAssignmentStatement, scope: CompilerScope) -> None:
        # Assignment works almost like a binary expression.
        # We are assured that the lhs is a variable.
        # The RHS can be anything.
        self.emit_new_label("assign", scope)
        var = scope.get_variable(statement.name)
        is_new_var = False
        if var is None:  # we go assign a new var.
            var = scope.define_variable(statement.name, self.cs.rsp.value)
            var.const = statement.const
            self.emitter.XOR(self.cs.rax, self.cs.rax)  # rax = 0, zero = true
            self.emitter.PUSH(self.cs.rax)              # push rax to reserve the variable on the stack.
            is_new_var = True
        if var.const and not is_new_var:
            self.error(f"Cannot assign to const {statement.name} at {statement.line}:{statement.column} scope({scope.name})")
        if not isinstance(var, CTVariable):
            self.error(f"Cannot assign to function {statement.name} at {statement.line}:{statement.column} scope({scope.name})")
        if statement.lhs.expr_type == AstNodetype.INDEXED_VARIABLE_EXPRESSION:
            if is_new_var:
                self.error(f"Variable unassigned, can't read index at {statement.line}:{statement.column} scope({scope.name})")
            self.compile_indexed_variable_assignment(statement, var, scope)
            return
        func = self.compile_expression(statement.rhs, scope)  # the value is on the stack now.
        if func is not None:
            scope.define_function_alias(statement.name, func.name)
        if statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT:
            if statement.append is True:
                reg = self.cs.GetFreeRegister()
                self.emitter.POP(reg)  # pop reg
                self.emitter.LOAD(self.cs.rax, var.stack_index)  # load rax, stack[stack_index] rax is now the variable.
                self.emitter.APPEND(self.cs.rax, reg)  # append rax, reg
                self.emitter.STOR(self.cs.rax, var.stack_index)  # stor [rbp + stack_offset], rax
                self.cs.ReleaseRegister(reg)
                return
            self.emitter.POP(self.cs.rax)  # pop rax
            self.emitter.STOR(var.stack_index, self.cs.rax)  # stor [rbp + stack_offset], rax
            return
        # if it's not straight up assign, we need to do a binary operation with the variable value as the lhs, so we get it:
        self.emitter.LOAD(self.cs.rax, var.stack_index)  # load rax, stack[stack_index] rax is now the variable.
        self.emitter.POP(self.cs.rbx)  # pop rbx
        if statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_INC:
            self.emitter.ADDRR(self.cs.rax, self.cs.rbx)  # addrr rax, rbx
        elif statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_DEC:
            self.emitter.SUBRR(self.cs.rax, self.cs.rbx)  # subrr rax, rbx
        elif statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_MUL:
            self.emitter.MULRR(self.cs.rax, self.cs.rbx)  # mulrr rax, rbx
        elif statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_DIV:
            self.emitter.DIVRR(self.cs.rax, self.cs.rbx)  # divrr rax, rbx
        elif statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_MOD:
            self.emitter.MODRR(self.cs.rax, self.cs.rbx)  # modrr rax, rbx
        elif statement.op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_POW:
            self.emitter.POWRR(self.cs.rax, self.cs.rbx)  # powrr rax, rbx
        self.emitter.STOR(var.stack_index, self.cs.rax)  # stor stack[stack_index], rax

    # this is a continuation from compile_assign_statement where the variable is indexed.
    def compile_indexed_variable_assignment(
        self, statement: AstNodeAssignmentStatement, var: CTVariable, scope: CompilerScope
    ) -> None:
        self.emit_new_label("assign_indexed", scope)
        if var.const:
            self.error(f"Cannot assign to const {statement.name} at {statement.line}:{statement.column} scope({scope.name})")
        self.var_to_stack(var, scope)
        n = len(statement.lhs.index)
        if n > 1:
            for i in range(n - 1):
                self.compile_expression(statement.lhs.index[i], scope)
                self.emitter.POP(self.cs.rbx)  # pop rbx
                self.emitter.POP(self.cs.rax)  # pop rax
                self.emitter.INDEX()  # rax = rax[rbx]
                self.emitter.PUSH(self.cs.rax)  # push rax
        # at this point there should be something on the top of the stack that is
        # working as a reference, so if we assign to that it'll change the original with it.
        self.compile_expression(statement.lhs.index[n - 1], scope)
        # on stack is now:
        # [0] = value
        # [1] = index
        # now we need to handle the right hand side of the assignment.
        self.compile_assign_indexed(statement.op, var, statement.rhs, scope)

    # this is a continuation from compile_indexed_variable_assignment, it handles the actual assignment.
    def compile_assign_indexed(self, op: LexToken, var: CTVariable, rhs: AstNodeExpression, scope: CompilerScope) -> None:
        if var.const:
            self.error(f"Cannot assign to const {var.name} at {rhs.line}:{rhs.column} scope({scope.name})")
        self.emit_new_label("assign_indexed_cnt", scope)
        func = self.compile_expression(rhs, scope)  # the value is on the stack now.
        if func is not None:
            scope.define_function_alias(var.name, func.name)
        reg: BytecodeRegister = self.cs.GetFreeRegister()
        if op.token_type == AstNodetype.OPERATOR_ASSIGNMENT:
            self.emitter.POP(reg)  # pop reg
            self.emitter.POP(self.cs.rbx)  # pop rbx [index]
            self.emitter.POP(self.cs.rax)  # pop rax [value]
            self.emitter.INDEXR(reg)  # indexr rax[rbx] = reg
            self.cs.ReleaseRegister(reg)
            return
        self.emitter.POP(reg)  # pop reg => value to assign
        self.emitter.POP(self.cs.rbx)  # pop rbx [index]
        self.emitter.POP(self.cs.rax)  # pop rax [value]
        # rax[rbx] = LHS
        # reg      = RHS
        # We need to put rax and rbx back on the stack, because we need them later on.
        self.emitter.PUSH(self.cs.rax)  # push rax
        self.emitter.PUSH(self.cs.rbx)  # push rbx
        # Now get the value, so we can do something with it:
        self.emitter.INDEX()  # pop rax = rax[rbx]
        self.emit_movrr(self.cs.rbx, reg)  # movrr rbx = reg
        if op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_INC:
            self.emitter.ADDRR(self.cs.rax, self.cs.rbx)  # addrr rax, rbx
        elif op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_DEC:
            self.emitter.SUBRR(self.cs.rax, self.cs.rbx)  # subrr rax, rbx
        elif op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_MUL:
            self.emitter.MULRR(self.cs.rax, self.cs.rbx)  # mulrr rax, rbx
        elif op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_DIV:
            self.emitter.DIVRR(self.cs.rax, self.cs.rbx)  # divrr rax, rbx
        elif op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_MOD:
            self.emitter.MODRR(self.cs.rax, self.cs.rbx)  # modrr rax, rbx
        elif op.token_type == AstNodetype.OPERATOR_ASSIGNMENT_POW:
            self.emitter.POWRR(self.cs.rax, self.cs.rbx)  # powrr rax, rbx
        self.emit_movrr(reg, self.cs.rax)  # movrr reg = rax
        # reg is the resulting value, that we need to write as if it was a normal assign.
        self.emitter.POP(self.cs.rbx)  # pop rbx [index]
        self.emitter.POP(self.cs.rax)  # pop rax [value]
        self.emitter.INDEXR(reg)  # indexr rax[rbx] = reg
        self.cs.ReleaseRegister(reg)
        self.emit_new_label("assign_indexed_cnt_end", scope)

    def has_params(self, params: List[AstNodeFunctionParameter]) -> bool:
        return any(param.node_type == AstNodetype.PARAMS for param in params)

    def compile_function_arguments(
        self, statement: AstNodeFunctionCallStatement, func: CTFunction, scope: CompilerScope
    ) -> None:
        self.emit_new_label("function_arguments", scope)
        if len(statement.args) != len(func.parameters) and not self.has_params(func.parameters):
            self.error(
                f"Function {statement.name} at {statement.line}:{statement.column} scope({scope.name}) requires {len(func.parameters)} arguments, {len(statement.args)} given"
            )
        for expr in statement.args:
            self.emit_new_label(f"function_argument: {expr}", scope)
            self.compile_expression(expr, scope)
        self.emitter.MOVRI(self.cs.rax, AstNodetype.INTEGER, len(statement.args))  # function arguments count is in rax
        self.emitter.PUSH(self.cs.rax)  # push rax

    def compile_clean_function_arguments(self, statement: AstNodeFunctionCallStatement) -> None:
        # gets the return value from the stack, puts it in a temp reg, then pops all the arguments
        # from the stack and puts the return value back on the stack.
        # but only if the function had any arguments.
        reg = self.cs.GetFreeRegister()
        self.emitter.POP(reg)  # get the return value from the stack.
        if len(statement.args) > 0:
            for _ in range(len(statement.args)):  # pop all the arguments from the stack.
                self.emitter.POP(self.cs.rax)
        self.emitter.POP(self.cs.rax)  # pop the number of arguments value from the stack.
        self.emitter.PUSH(reg)  # push the return value onto the stack again.
        self.cs.ReleaseRegister(reg)

    def compile_function_call(self, statement: AstNodeFunctionCallStatement, scope: CompilerScope) -> None:
        self.emit_new_label("function_call", scope)
        func = scope.get_function(statement.name)
        if func is None:
            var = scope.get_variable(statement.name)
            if var is not None:
                self.compile_variable_function_call(statement, var, scope)
                return
            self.error(f"Function {statement.name} not found at {statement.line}:{statement.column} scope({scope.name})")
        self.compile_function_arguments(statement, func, scope)
        self.emitter.CALL(func.start_address)
        self.compile_clean_function_arguments(statement)
        self.emitter.POP(self.cs.rax)  # pop rax -> RAX has function return value.

    # this is a continuation of compile_function_call where the identifier is a variable instead of a function.
    def compile_variable_function_call(
        self, statement: AstNodeFunctionCallStatement, var: CTVariable, scope: CompilerScope
    ) -> None:
        self.emit_new_label("variable_function_call", scope)
        # TODO: Make it so that it also works for indexed variable access.
        # It now only works based on the variable name, not on the index.
        # This bit is almost the same as it's the signature of the function call.
        # self.cs.write_string(var.name)
        func = scope.get_function_by_alias(var.name)
        if func is None:
            self.error(f"Function {statement.name} not found at {statement.line}:{statement.column} scope({scope.name})")
        self.compile_function_arguments(statement, func, scope)
        # So we are a variable, we need to figure out if we are a function pointer.
        self.emitter.LOAD(self.cs.rax, var.stack_index)  # load rax, [rbp + stack_offset] rax is now the variable.
        # rax is now the value of the variable.
        if statement.index is not None:  # ok, we sneaked in an indexed one under the radar :P
            var.index = statement.index
            self.emitter.PUSH(self.cs.rax)  # push rax
            for i in range(len(var.index)):
                self.compile_expression(var.index[i], scope)  # this pushes the result of the expression.
                self.emitter.POP(self.cs.rbx)  # pop rbx
                self.emitter.POP(self.cs.rax)  # pop rax
                self.emitter.INDEX()  # rax = rax[rbx]
                self.emitter.PUSH(self.cs.rax)  # push rax
            self.emitter.POP(self.cs.rax)  # pop rax
            self.cs.rax.value_type = AstNodetype.FUNCTION  # this is needed, because inside the array this information was lost.
            self.emitter.SETRTI(self.cs.rax, AstNodetype.FUNCTION)
        # validate if it is a function pointer.
        self.emitter.CMPRTI(self.cs.rax, AstNodetype.FUNCTION)  # compare register.type with immediate type
        self.emitter.ERRORNZ(
            f"Variable {var.name} is not a function pointer. Scope({scope.name})"
        )  # error out when zero flag is not set.
        # if we get here, we have a valid function pointer in RAX
        # so we can call it.
        # warning cannot use rax in callr, callr destroys rax.
        self.emitter.MOVRR(self.cs.rbx, self.cs.rax)
        self.emitter.CALLR(self.cs.rbx)  # callr rbx
        self.compile_clean_function_arguments(statement)
        # The downside of this is that we can't change the location in memory for a function.
        # Unless we do some very elaborate work with setting the value of the variable to the correct address before
        # this is ran. But that is a problem for later.

    def compile_function_definition(self, statement: AstNodeFunctionDefinition, scope: CompilerScope) -> None:
        func = scope.define_function(statement.name, self.cs.rip.value + 1)  # +9 for the jump instruction.
        if func is None:
            self.error(f"Function {statement.name} already defined at {statement.line}:{statement.column} scope({scope.name})")
        function_label = scope.get_new_label(func.name)
        function_call_exit_label = scope.root.get_new_label(f"{func.name}_exit")
        function_call_end_label = scope.root.get_new_label(f"{func.name}_end")
        self.emit_jump(
            Opcode.JMP, function_call_end_label, scope
        )  # functions go in between the other code, so we must jump over them.
        scope.set_label_address(function_label, self.cs.rip.value)
        # make function scope.
        function_scope = self.emit_scope(scope)
        function_scope.is_function_definition = True
        function_scope.can_search_parent = False
        param_count = len(statement.parameters)
        for i, param in enumerate(statement.parameters):
            func.parameters.append(param)
            offset = FUNCTION_CALL_PARAMETER_STACK_OFFSET - (param_count - 1) + i
            v = function_scope.define_variable(param.name, offset)
            v.arg = True
            v.node_type = param.node_type

        function_scope.exit_label = function_call_exit_label
        if statement.return_type is not None:
            func.return_type = statement.return_type
            rv = function_scope.define_variable("return_value", FUNCTION_CALL_RETURN_VALUE_STACK_OFFSET)
            rv.arg = True

        if statement.external:
            self.compile_external_function_definition(statement, func)
        else:
            self.compile_block(statement.body, function_scope)
        self.compile_function_definition_end(function_call_exit_label, function_call_end_label, function_scope)

    def compile_external_function_definition(self, statement: AstNodeFunctionDefinition, func: CTFunction) -> None:
        func.external = True
        func.module = statement.module
        func.function = statement.function
        self.emitter.CALLE(func.module, func.function, len(statement.parameters))
        self.emitter.STORR(self.cs.rbp, FUNCTION_CALL_RETURN_VALUE_STACK_OFFSET, self.cs.rax)  # storr [rbp - 3], rax

    def compile_function_definition_end(
        self, function_call_exit_label: int, function_call_end_label: int, scope: CompilerScope
    ) -> None:
        scope.set_label_address(function_call_exit_label, self.cs.rip.value)
        # exit label here.
        self.emit_scope_end(scope)
        self.emitter.RET()  # ret
        # because rbp is popped after resetting the stack pointer,
        # the return value of the function is now on top of the stack.
        scope.set_label_address(function_call_end_label, self.cs.rip.value)

    # Meta data compilation

    def compile_datasegment(self, scope: CompilerScope) -> None:
        metadata = {
            "VARIABLES": [var.name for var in scope.variables],
            "FUNCTIONS": [func.name for func in scope.functions],
            "LIBRARIES": [lib for lib in scope.libraries],
            "LABELS": [(label.name, label.address) for label in scope.labels],
            "JUMPS": [(jump.address, jump.label) for jump in scope.jump_table],
            "RESERVED": [],
        }
        self.emitter.DATASEG(metadata)

    # expression compilation

    def compile_expression(self, expression: AstNodeExpression, scope: CompilerScope) -> Optional[CTFunction]:
        self.emit_new_label("expression", scope)  # up for commenting out, it's too chatty.
        if expression.expr_type == AstNodetype.LITERAL_EXPRESSION:
            self.compile_literal_expression(expression, scope)
        elif expression.expr_type == AstNodetype.UNARY_EXPRESSION:
            self.compile_unary_expression(expression, scope)
        elif expression.expr_type == AstNodetype.BINARY_EXPRESSION:
            self.compile_binary_expression(expression, scope)
        elif expression.expr_type == AstNodetype.VARIABLE_EXPRESSION:
            return self.compile_variable_expression(expression, scope)
        elif expression.expr_type == AstNodetype.INDEXED_VARIABLE_EXPRESSION:
            self.compile_indexed_variable_expression(expression, scope)
        elif expression.expr_type == AstNodetype.FUNCTION_CALL_EXPRESSION:
            return self.compile_function_call_expression(expression, scope)
        elif expression.expr_type == AstNodetype.VARIABLE_FUNCTION_CALL_EXPRESSION:
            self.compile_variable_function_call_expression(expression, scope)
        elif expression.expr_type == AstNodetype.IS_TYPE_STATEMENT:
            self.compile_is_type_statement(expression, scope)
        elif expression.expr_type == AstNodetype.TYPE_STATEMENT:
            self.compile_type_statement(expression, scope)
        elif expression.expr_type == AstNodetype.REGISTER_EXPRESSION:
            self.compile_register_expression(expression, scope)
        else:
            self.error(f"Unknown expression type {expression.expr_type} at {expression.line}:{expression.column}")

    def compile_literal_expression(self, expression: AstNodeLiteralExpression, scope: CompilerScope) -> None:
        # A literal expression means a literal value gets written to the stack.
        self.emit_new_label("literal_expression", scope)
        if expression.value_type == AstNodetype.NEW_ARRAY:
            expression.value_type = AstNodetype.ARRAY
            expression.value = []
        self.emitter.MOVRI(self.cs.rax, expression.value_type, expression.value)
        self.emitter.PUSH(self.cs.rax)

    def compile_register_expression(self, expression: AstNodeRegisterExpression, scope: CompilerScope) -> None:
        self.emitter.PUSH(expression.register)

    def compile_unary_expression(self, expression: AstNodeUnaryExpression, scope: CompilerScope) -> None:
        self.emit_new_label("unary_expression", scope)
        self.compile_expression(expression.right, scope)
        self.emitter.POP(self.cs.rax)  # pop rax
        if expression.op.token_type == AstNodetype.OPERATOR_SUBTRACTION:
            self.emitter.NEG(self.cs.rax)
        elif expression.op.token_type == AstNodetype.NOT_STATEMENT:
            self.emitter.NOT(self.cs.rax)
        elif expression.op.token_type == AstNodetype.BITWISE_NOT:
            self.error(f"Bitwise not not implemented at {expression.line}:{expression.column}")
        self.emitter.PUSH(self.cs.rax)

    def compile_binary_expression(self, expression: AstNodeBinaryExpression, scope: CompilerScope) -> None:
        self.emit_new_label("binary_expression", scope)
        # binary expression is simple. First we compile the left and right side of the expression
        # and then we pop the values in RAX and RBX apply the operator and then push RAX back onto the stack.
        self.compile_expression(expression.left, scope)
        self.compile_expression(expression.right, scope)
        self.emitter.POP(self.cs.rbx)  # pop rbx rhs
        self.emitter.POP(self.cs.rax)  # pop rax lhs
        if expression.op.token_type == AstNodetype.OPERATOR_ADDITION:
            self.emitter.ADDRR(self.cs.rax, self.cs.rbx)  # addrr rax, rbx
        elif expression.op.token_type == AstNodetype.OPERATOR_SUBTRACTION:
            self.emitter.SUBRR(self.cs.rax, self.cs.rbx)  # subrr rax, rbx
        elif expression.op.token_type == AstNodetype.OPERATOR_MULTIPLICATION:
            self.emitter.MULRR(self.cs.rax, self.cs.rbx)  # mulrr rax, rbx
        elif expression.op.token_type == AstNodetype.OPERATOR_DIVISION:
            self.emitter.DIVRR(self.cs.rax, self.cs.rbx)  # divrr rax, rbx
        elif expression.op.token_type == AstNodetype.OPERATOR_POWER:
            self.emitter.POWRR(self.cs.rax, self.cs.rbx)  # powrr rax, rbx
        elif expression.op.token_type == AstNodetype.OPERATOR_MODULUS:
            self.emitter.MODRR(self.cs.rax, self.cs.rbx)  # modrr rax, rbx
        elif expression.op.token_type == AstNodetype.COMPARETOR_EQUAL:
            self.emitter.CMPRR(self.cs.rax, self.cs.rbx)
            self.emitter.SETZR(self.cs.rax)
        elif expression.op.token_type == AstNodetype.COMPARETOR_NOT_EQUAL:
            self.emitter.CMPRR(self.cs.rax, self.cs.rbx)
            self.emitter.SETNZR(self.cs.rax)
        elif expression.op.token_type == AstNodetype.COMPARETOR_LESS_THAN:
            self.emitter.CMPRR(self.cs.rax, self.cs.rbx)
            self.emitter.SETLR(self.cs.rax)
        elif expression.op.token_type == AstNodetype.COMPARETOR_LESS_THAN_EQUAL:
            self.emitter.CMPRR(self.cs.rax, self.cs.rbx)
            self.emitter.SETLER(self.cs.rax)
        elif expression.op.token_type == AstNodetype.COMPARETOR_GREATER_THAN:
            self.emitter.CMPRR(self.cs.rax, self.cs.rbx)
            self.emitter.SETGR(self.cs.rax)
        elif expression.op.token_type == AstNodetype.COMPARETOR_GREATER_THAN_EQUAL:
            self.emitter.CMPRR(self.cs.rax, self.cs.rbx)
            self.emitter.SETGER(self.cs.rax)
        elif expression.op.token_type == AstNodetype.AND_STATEMENT:
            self.emitter.ANDRR(self.cs.rax, self.cs.rbx)
        elif expression.op.token_type == AstNodetype.OR_STATEMENT:
            self.emitter.ORRR(self.cs.rax, self.cs.rbx)
        elif expression.op.token_type == AstNodetype.XOR_STATEMENT:
            self.emitter.XOR(self.cs.rax, self.cs.rbx)
        self.emitter.PUSH(self.cs.rax)  # push rax

    def compile_variable_expression(self, expression: AstNodeVariableExpression, scope: CompilerScope) -> Optional[CTFunction]:
        self.emit_new_label("variable_expression", scope)
        var = scope.get_variable(expression.name)
        if var is None and scope.Record is not None:
            self.compile_field_expression(expression.name, scope)
            return None
        if var is None:
            func = scope.get_function(expression.name)
            if func is not None:
                self.compile_function_expression(func, scope)
                return func
            self.error(
                f"Variable or function {expression.name} not found at {expression.line}:{expression.column} scope({scope.name})"
            )
        if not isinstance(var, CTVariable):
            self.error(
                f"Variable {expression.name} is not a variable at {expression.line}:{expression.column} scope({scope.name})"
            )
        # variables live on the stack, the start of the stack for a scope is in the rbp register.
        # so we read the value from [rbp + var.offset] (our stack starts at 0 and counts up)
        # and push it to the stack.
        self.var_to_stack(var, scope)

    def compile_indexed_variable_expression(self, expression: AstNodeIndexedVariableExpression, scope: CompilerScope) -> None:
        self.emit_new_label("indexed_variable_expression", scope)
        # Indexed variable expression is very hard.
        # Getting the variable is not a big deal, but handling the index is.
        var = scope.get_variable(expression.name)
        if var is None:
            self.error(f"Variable {expression.name} not defined at {expression.line}:{expression.column} scope({scope.name})")
        if not isinstance(var, CTVariable):
            self.error(
                f"Variable {expression.name} is not a variable at {expression.line}:{expression.column} scope({scope.name})"
            )
        self.var_to_stack(var, scope)
        # The variable value on the stack.
        # Now we need to get the index value.
        for expr in expression.index:
            self.compile_expression(expr, scope)  # the index value is on the stack now.
            self.emitter.POP(self.cs.rbx)  # pop rbx
            self.emitter.POP(self.cs.rax)  # pop rax
            self.emitter.INDEX()  # rax = rax[rbx]
            self.emitter.PUSH(self.cs.rax)  # push rax

    def compile_function_expression(self, func: CTFunction, scope: CompilerScope) -> None:
        # This should only happen in an assignment.
        self.emit_new_label("function_expression", scope)
        self.emitter.MOVRI(self.cs.rax, AstNodetype.FUNCTION, func.start_address)
        self.emitter.PUSH(self.cs.rax)

    def compile_function_call_expression(self, expression: AstNodeFunctionCallExpression, scope: CompilerScope) -> None:
        self.emit_new_label("function_call_expression", scope)
        func = scope.get_function(expression.name)
        if func is None:  # maybe it's a variable? don't know, it should be handled by the other expr types.
            self.error(f"Function {expression.name} not found at {expression.line}:{expression.column} scope({scope.name})")
        self.compile_function_arguments(expression, func, scope)
        self.emitter.CALL(func.start_address)
        self.compile_clean_function_arguments(expression)

    def compile_variable_function_call_expression(
        self, expression: AstNodeVariableFunctionCallExpression, scope: CompilerScope
    ) -> None:
        self.emit_new_label("variable_function_call_expression", scope)
        var = scope.get_variable(expression.variable.name)
        if var is None:
            self.error(
                f"Variable {expression.variable.name} not defined at {expression.line}:{expression.column} scope({scope.name})"
            )
        for expr in expression.args:
            self.compile_expression(expr)
        func = scope.get_function_by_alias(expression.variable.name)
        self.emitter.CALL(func.start_address)
        self.compile_clean_function_arguments(expression)

    # Include implementation

    def find_library(self, name: str) -> Optional[str]:
        for path in SearchPath:
            lib_path = os.path.join(path, f"{name}.mcl")
            if os.path.exists(lib_path):
                return lib_path
        return None

    def load_library(self, path: str) -> Optional[str]:
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return f.read()

    def compile_include_statement(self, statement: AstNodeIncludeStatement, scope: CompilerScope) -> None:
        self.emit_new_label("include_statement", scope)
        for lib in statement.libraries:
            if lib.name in scope.libraries:
                continue
            lib_path = self.find_library(lib.name)
            if lib_path is None:
                self.error(f"Library {lib.name} not found at {lib.line}:{lib.column}")
            source = self.load_library(lib_path)
            if source is None:
                self.error(f"Library {lib.name} not found at {lib.line}:{lib.column}")
            self.emit_new_label(f"include_{lib.name}", scope)
            scope.libraries[lib.name] = self.cs.rip.value
            lex = Lexer(source)
            parser = Parser(lex.tokenize(), lib_path)
            self.compile_block(parser.parse(), scope)

# Select compiler

    def compile_select_statement(self, statement: AstNodeSelectStatement, scope: CompilerScope):
        source_data_register = self.cs.GetFreeRegister()
        self.compile_from(statement, source_data_register, scope)
        self.compile_where(statement, source_data_register, scope)
        self.compile_fields(statement, source_data_register, scope)
        self.compile_merge(statement, source_data_register, scope)
        self.compile_distinct(statement, source_data_register, scope)
        self.compile_into(statement, source_data_register, scope)
        self.cs.ReleaseRegister(source_data_register)

    def compile_from(self, statement: AstNodeSelectStatement, source_data_register: BytecodeRegister, scope: CompilerScope):
        # declare labels used in this function.
        lbl_handle_nil: int  = scope.get_new_label("select_from_handle_nil") # jump label to function that will handle nil values.
        lbl_data_check: int  = scope.get_new_label("select_from_data_check") # jump label to function that will check the data type.
        lbl_from_end: int    = scope.get_new_label("select_from_end")   # jump label to the end of the from statement.
        # Collect data from the select statement.
        # From expression can be a variable, a function call or a literal.
        # The result value of the expression can be nil or false, in addittion to a record or a list of records.
        # The source data registr is used to store the result of the from expression.
        self.compile_expression(statement.From, scope)
        self.emitter.POP(source_data_register)
        # Now we need to check for nil or false. If either is true, we need to make the source an empty list.
        self.emitter.CMPRTI(self.cs.rax, AstNodetype.NIL)
        self.emit_jump(Opcode.JMPZ,lbl_handle_nil, scope)
        self.emitter.CMPRTI(self.cs.rax, AstNodetype.BOOLEAN)
        self.emit_jump(Opcode.JMPNZ,lbl_data_check, scope)
        # If we get here, the source data is either nil or false.
        scope.set_label_address(lbl_handle_nil, self.cs.rip.value)
        self.emitter.MOVRI(source_data_register, AstNodetype.ARRAY, [])
        scope.set_label_address(lbl_data_check, self.cs.rip.value)
        # Now we need to check if the source data is a record or a list.
        self.emitter.CMPRTI(source_data_register, AstNodetype.ARRAY) # if it's an array, we good and exit.
        self.emit_jump(Opcode.JMPZ, lbl_from_end, scope)
        self.emitter.CMPRTI(source_data_register, AstNodetype.RECORD) # if it's a record, we need to make it a list.
        self.emitter.ERRORNZ("From expression must be a record or a list of records.")
        self.emitter.MOVRTOA(source_data_register)
        scope.set_label_address(lbl_from_end, self.cs.rip.value)

    def compile_merge(self, statement: AstNodeSelectStatement, source_data_register: BytecodeRegister, scope: CompilerScope):
        if statement.merge is False:
            return
        # declare labels used in this function.
        lbl_merge_start: int = scope.get_new_label("select_merge_start")
        lbl_merge_end: int = scope.get_new_label("select_merge_end")
        lbl_merge_end2: int = scope.get_new_label("select_merge_end2")

        destination_register = self.cs.GetFreeRegister()
        self.compile_expression(statement.Into, scope)
        self.emitter.POP(destination_register) # pop rax
        # now we need to verify if there is data to merge, if not we need to show an error.
        self.emitter.MOVRI(self.cs.rax, AstNodetype.BOOLEAN, statement.distinct)
        self.emitter.CMPRI(self.cs.rax, AstNodetype.BOOLEAN, False)
        self.emit_jump(Opcode.JMPZ, lbl_merge_start, scope)
        self.emitter.LENR(self.cs.rax, source_data_register)
        self.emitter.CMPRI(self.cs.rax, AstNodetype.INTEGER, 0)
        self.emit_jump(Opcode.JMPZ, lbl_merge_start, scope)
        self.emitter.MOVRR(source_data_register, destination_register) # source_data_register = destination_register
        self.emit_jump(Opcode.JMP, lbl_merge_end2, scope)
        # The data source already contains data we collected from the from statement.
        # If there is a need for merging data, the data to merge is in the variable that's in the into expression.
        # The result of the merge is stored in the data source register.
        scope.set_label_address(lbl_merge_start, self.cs.rip.value)
        self.emitter.MOVRR(self.cs.rax, destination_register) # rax = destination_register
        self.emitter.CMPRTI(self.cs.rax, AstNodetype.NIL)
        self.emitter.ERRORZ("Merge data is nil.")
        # if we get here, there is data to merge, we only need to validate if it is a record or a list of records.
        self.emitter.CMPRTI(self.cs.rax, AstNodetype.ARRAY)
        self.emit_jump(Opcode.JMPZ, lbl_merge_end, scope)
        self.emitter.CMPRTI(self.cs.rax, AstNodetype.RECORD)
        self.emitter.ERRORNZ("Merge data must be a record or a list of records.")
        # if we get here, the data to merge is a list of records and is in RAX
        # and we need to merge it with the data in the source data register.
        scope.set_label_address(lbl_merge_end, self.cs.rip.value)
        self.emitter.MERGE(source_data_register, self.cs.rax, source_data_register)
        scope.set_label_address(lbl_merge_end2, self.cs.rip.value)
        self.cs.ReleaseRegister(destination_register)

    def compile_where(self, statement: AstNodeSelectStatement, source_data_register: BytecodeRegister, scope: CompilerScope):
        if statement.Where is None:
            return
        # declare labels used in this function.
        lbl_where_end: int = scope.get_new_label("select_where_end")
        lbl_where_loop_start: int = scope.get_new_label("select_where_loop_start")
        lbl_where_loop_continue: int = scope.get_new_label("select_where_loop_continue")
        lbl_where_skip_record: int = scope.get_new_label("select_where_skip_record")
        lbl_where_end2: int = scope.get_new_label("select_where_end2")
        # The data source already contains data we collected from the from statement.
        # If there is a need for filtering data, the filter expression is in the where expression.
        # The result of the filtering is stored in the data source register.
        flag_register = self.cs.GetFreeRegister()
        self.emitter.MOVRI(flag_register, AstNodetype.BOOLEAN, False)
        self.emitter.CMPRTI(source_data_register, AstNodetype.RECORD)
        self.emit_jump(Opcode.JMPNZ, lbl_where_skip_record, scope) # already a record
        self.emitter.MOVRTOA(source_data_register)
        self.emitter.MOVRI(flag_register, AstNodetype.BOOLEAN, True)
        scope.set_label_address(lbl_where_skip_record, self.cs.rip.value)
        # first we check if there is any data to filter.
        self.emitter.LENR(self.cs.rcx, source_data_register)
        self.emitter.CMPRI(self.cs.rcx, AstNodetype.INTEGER, 0)
        self.emit_jump(Opcode.JMPZ, lbl_where_end, scope) # no data so exit.
        # if we get here, there is data to filter.
        destination_register = self.cs.GetFreeRegister()
        record_register = self.cs.GetFreeRegister()
        index_register = self.cs.GetFreeRegister()
        self.emitter.MOVRI(destination_register, AstNodetype.ARRAY, [])
        self.emitter.MOVRI(index_register, AstNodetype.INTEGER, 0)
        scope.set_label_address(lbl_where_loop_start, self.cs.rip.value)       
        self.emitter.MOVRR(self.cs.rbx, index_register) # rbx = rcx       
        self.emitter.MOVRR(self.cs.rax, source_data_register)
        self.emitter.INDEX() # rax = rax[rbx]
        self.emitter.MOVRR(record_register, self.cs.rax) # record_register = rax
        self.compile_where_expression(statement, record_register, scope)
        self.emitter.POP(self.cs.rax) # pop rax
        self.emitter.CMPRI(self.cs.rax, AstNodetype.BOOLEAN, True)
        self.emit_jump(Opcode.JMPNZ, lbl_where_loop_continue, scope) # if the result is false, we need to remove the record.
        self.emitter.APPEND(destination_register, record_register) # append record_register to destination_register
        scope.set_label_address(lbl_where_loop_continue, self.cs.rip.value)
        self.emitter.INC(index_register)
        self.emit_jump(Opcode.DJNZ, lbl_where_loop_start, scope) # loop back to start if there is more data to filter.

        self.emitter.MOVRR(source_data_register, destination_register)
        scope.set_label_address(lbl_where_end, self.cs.rip.value)
        self.emitter.CMPRI(flag_register, AstNodetype.BOOLEAN, True)
        self.emit_jump(Opcode.JMPNZ, lbl_where_end2, scope) # if the flag is false, we need to make the source data an empty list.
        self.emitter.MOVATOR(source_data_register)
        scope.set_label_address(lbl_where_end2, self.cs.rip.value)
        self.cs.ReleaseRegister(record_register)
        self.cs.ReleaseRegister(index_register)
        self.cs.ReleaseRegister(destination_register)
        self.cs.ReleaseRegister(flag_register)

    def compile_into(self, statement: AstNodeSelectStatement, source_data_register: BytecodeRegister, scope: CompilerScope):
        expr = AstNodeRegisterExpression(LexToken(AstNodetype.REGISTER, source_data_register, 0,0,0, self.program.filename), source_data_register)
        stmt = AstNodeAssignmentStatement(statement.Into, LexToken(AstNodetype.OPERATOR_ASSIGNMENT, "=", 0,0,0, self.program.filename), expr)
        self.compile_assignment_statement(stmt, scope)
    
    def compile_distinct(self, statement: AstNodeSelectStatement, source_data_register: BytecodeRegister, scope: CompilerScope):
        if statement.distinct is False: return
        # declare labels used in this function.
        lbl_distinct_end: int = scope.get_new_label("select_distinct_end")
        self.emitter.CMPRTI(source_data_register, AstNodetype.RECORD)
        self.emit_jump(Opcode.JMPZ, lbl_distinct_end, scope) # already a record
        self.emitter.MOVATOR(source_data_register)
        scope.set_label_address(lbl_distinct_end, self.cs.rip.value)
        self.compile_special_cases(source_data_register, scope)

    def compile_where_expression(self, statement: AstNodeSelectStatement, record_register: BytecodeRegister, scope: CompilerScope):
        scope.Record = record_register
        self.compile_expression(statement.Where, scope)

    def compile_field_expression(self, field: str, scope: CompilerScope):
        self.emitter.MOVRR(self.cs.rax, scope.Record)  # rax = record
        self.emitter.MOVRI(self.cs.rbx, AstNodetype.STRING, field)  # rbx = name
        self.emitter.INDEX()  # rax = rax[rbx]
        self.emitter.PUSH(self.cs.rax)

    def compile_fields(self, statement: AstNodeSelectStatement, source_data_register: BytecodeRegister, scope: CompilerScope):
        if statement.Fields is None:
            return
        if len(statement.Fields) == 1 and statement.Fields[0].name == "*":
            return
        self.emitter.MOVRI(self.cs.rax, AstNodetype.ARRAY, [{field.name:field.altfieldname} for field in statement.Fields])
        self.emitter.FIELDS(source_data_register, self.cs.rax)

    def compile_special_cases(self, source_data_register: BytecodeRegister, scope: CompilerScope):
        lbl_special_cases_end: int = scope.get_new_label("select_special_cases_end")
        self.emitter.CMPRTI(source_data_register, AstNodetype.RECORD)
        self.emit_jump(Opcode.JMPNZ, lbl_special_cases_end , scope)
        self.emitter.LENR(self.cs.rax, source_data_register)
        self.emitter.CMPRI(self.cs.rax, AstNodetype.INTEGER, 1)
        self.emit_jump(Opcode.JMPNZ, lbl_special_cases_end, scope)
        self.emitter.MOVRI(self.cs.rbx, AstNodetype.INTEGER, 0)
        self.emitter.MOVRR(self.cs.rax, source_data_register)
        self.emitter.FEINDEX() # rax = rax[rbx]
        self.emitter.MOVRR(self.cs.rbx, self.cs.rax)
        self.emitter.MOVRR(self.cs.rax, source_data_register)
        self.emitter.INDEX()
        self.emitter.MOVRR(source_data_register, self.cs.rax)
        scope.set_label_address(lbl_special_cases_end, self.cs.rip.value)
