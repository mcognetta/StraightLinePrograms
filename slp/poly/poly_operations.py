import slp.core.nodes as nodes
import slp.core.node_utils as node_utils

def differentiate(slp,v,zero=None,one=None):
    '''
    differentiates an slp (given by its final node) by a given variable, v
    returns a node representing to the differentiated slp

    if a zero and one are already constructed we can just use those.
    otherwise, create new ones
    '''

    diff_dict = {}  #will store {node:its derivative}
    if zero == None:
        zero = nodes.constant_node(0)
    if one == None:
        one = nodes.constant_node(1)
    
    for i in node_utils.get_all_dependencies(slp):
        if type(i) == nodes.constant_node:
            diff_dict[i] = zero
        else:
            if i == v:
                diff_dict[i] = one
            else:
                diff_dict[i] = zero

    def recurse(n,diff_dict):
        if type(n) in nodes.operation_nodes:
            if n.operand_1 not in diff_dict:
                diff_dict = recurse(n.operand_1,diff_dict)
            if n.operand_2 not in diff_dict:
                diff_dict = recurse(n.operand_2,diff_dict)
            if type(n) == nodes.sum_node:
                diff_dict[n] = nodes.sum_node(diff_dict[n.operand_1],diff_dict[n.operand_2])
            elif type(n) == nodes.product_node:
                temp_left = nodes.product_node(n.operand_1,diff_dict[n.operand_1])
                temp_right = nodes.product_node(n.operand_2,diff_dict[n.operand_2])
                diff_dict[n] = nodes.sum_node(temp_left,temp_right)
        return diff_dict

    diff_dict = recurse(slp,diff_dict)
    return diff_dict[slp]