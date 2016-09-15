import StraightLinePrograms.nodes as nodes
import StraightLinePrograms.node_utils as node_utils


def display_polynomial(node):

    name_dict = {}

    counter = 0
    for i in node_utils.get_all_dependencies(node):

        if type(i) == nodes.variable_node:
            if i.name == None:
                name_dict[i] = "(v_%d)"%counter
                counter += 1
            else:
                name_dict[i] = i.name
        else:
            name_dict[i] = str(i.val)

    def recurse(n,name_dict):
        if type(n) in nodes.operation_nodes:
            if type(n) == nodes.sum_node:
                return recurse(n.operand_1,name_dict) + '+' + recurse(n.operand_2,name_dict)
            elif type(n) == nodes.product_node:
                return recurse(n.operand_1,name_dict) + '*' + recurse(n.operand_2,name_dict)
            elif type(n) == nodes.division_node:
                return recurse(n.operand_1,name_dict) + '/' + recurse(n.operand_2,name_dict)
        else:
            return name_dict[n]

    print(recurse(node,name_dict))

def display_slp(node):
    non_gates = {}
    gates =  node_utils.get_all_gates(node)
    variable_counter = 0

    for i in node_utils.get_all_dependencies(node):
        if type(i) == nodes.variable_node:
            if i.name == None:
                non_gates[i] = "v_%d"%variable_counter
                variable_counter += 1
            else:
                non_gates[i] = i.name
        else:
            non_gates[i] = str(i.val)

    num_gates = len(gates)
    gate_counter = variable_counter + 1

    return None

def output_slp_to_file(f,slp):
    gates = node_utils.get_all_gates(slp)
    variables = node_utils.get_all_variable_dependencies(n)
    constants = node_utils.get_all_constant_dependencies(n)
    num_gates = len(gates)
    gate_names = {}
    variable_names = {}
    constant_names = {}
    f = open(f,'w')
