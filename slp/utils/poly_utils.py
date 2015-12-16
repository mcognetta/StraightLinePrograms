import slp.core.nodes as nodes
import slp.core.node_utils as node_utils

'''
Takes in a node representing a polynomial and outputs it
in polynomial form like x^2+y+3*z
'''
def display_as_poly(node):
	var_list = node_utils.get_variable_dependencies(node)
	print(var_list)
	count = 0
	var_names = {}
	for i in range(len(var_list)):
		if type(var_list[i]) != nodes.constant_node:
			var_names[var_list[i]] = "v_%d"%count
			count += 1
	def recurse(n,var_names):
		if type(n) == nodes.constant_node:
			return str(n)
		elif type(n) == nodes.variable_node:
			return var_names[n]
		else:
			return recurse(n.operand_1,var_names) + n.operation + recurse(n.operand_2,var_names)
	return recurse(node,var_names)