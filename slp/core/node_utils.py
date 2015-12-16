'''
node_utils.py
'''

import slp.core.nodes as nodes
import numpy as np

'''
get_var_dependencies(node)

returns a list of variable nodes that the specified gate depends on to evaluate
'''

def get_variable_dependencies(node):

    '''
    return all variables that make up the computation path of node
    '''

    out_list = []
    if type(node) == nodes.variable_node:
        out_list.append(node)
    else:
        if type(node) in nodes.operation_nodes:
            out_list += get_variable_dependencies(node.operand_1)
            out_list += get_variable_dependencies(node.operand_2)
    return list(set(out_list))

def get_constant_dependencies(node):

    '''
    returns all constants that make up the computation path of node
    '''

    out_list = []
    if type(node) == nodes.constant_node:
        out_list.append(node)
    else:
        if type(node) in nodes.operation_nodes:
            out_list += get_constant_dependencies(node.operand_1)
            out_list += get_constant_dependencies(node.operand_2)
    
    return list(set(out_list))

def get_all_dependencies(node):

    '''
    returns all constants and variables that make up the computataion 
    path of node
    '''
    #return get_variable_dependencies(node) + get_constant_dependencies(node)
    out_list = []
    if type(node) not in nodes.operation_nodes and type(node) != np.matrix:
        out_list.append(node)
    else:
        if(type(node) != nodes.matrix_node and type(node) != np.matrix):
            out_list += get_all_dependencies(node.operand_1)
            out_list += get_all_dependencies(node.operand_2)

    return list(set(out_list))

def get_all_gates(node):

    '''
    return all gates that make up the computation path of node
    no constants or variables are returned
    '''

    out_list = []
    if type(node) in nodes.operation_nodes:
        out_list.append(node)
        out_list += get_all_gates(node.operand_1)
        out_list += get_all_gates(node.operand_2)
    return list(set(out_list))

'''
get_depth(node)

returns the distance from the specified node to the farthest variable it depends on

Technical note: this actually returns the height in the traditional graph theoretic sense
'''

def get_depth(node):
    def recurse(n,h):
        if type(n) == var_node or type(n) == const_node:
            return h
        else:
            h += 1
            return max(recurse(n.operand_1,h),recurse(n.operand_2,h))
    return recurse(node,0)

def prob_minimize(slp,trials=None):

    '''
    not working
    '''
    import random

    eval_dict = {}
    variables = [v for v in get_var_dependencies(slp) if type(v) == slp.core.nodes.var_node]

    if trials == None:
        trials = len(variables)**2

    def construct_eval_dict(variables, values):
        out = {}
        i = 0
        for v in var:
            out[v] = values[i]
            i += 1
        return out

    def group(gates,trial):

        if trial == 0:
            return gates

        buckets = {}
        out = []
        num_vars = len(variables)
        tests = random.sample(range(num_vars**3),num_vars)
        eval_dict = construct_eval_dict(variables,tests)
        for g in gates:
            value = g.evaluate(eval_dict)
            if value not in buckets:
                buckets[value] = []
            buckets[g.evaluate(eval_dict)].append(g)

        for b in buckets:
            if len(buckets[b]) > 1:
                out.append(group(buckets[b],trial-1))
        #return out

