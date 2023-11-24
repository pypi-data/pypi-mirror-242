from macal.macal_vm import MacalVm
from macal.macal_variable import MacalVariable
from macal.ast_nodetype import AstNodetype
from macal.macal_opcode import *

var = MacalVariable("a", None)
vm = MacalVm(False)

print("variable var:")
var.value = [1, 2, 3, 4, 5]
print(var.value)
index = [(Opcode_LOAD_CONSTANT, 2)]

print()
print("print index 2")
x = vm._execute_walk_index(var, index)
print()
print(x)
print(var)

print()
print("update at index 2")
print()
vm._execute_walk_index_for_store(var, index, 42)
print(var)
