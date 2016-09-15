import re
import StraightLinePrograms.nodes as nodes
import numpy as np

def tokenize(eq):
    '''
    Takes an equation in string form and produces a set of tokens
    representing the variables and constants used in the SLP

    ex:
    "3*x+2*y+z" -> {3,2,x,y,z}
    '''
    
    return list(re.split('[+]|-|[*]|/|^',eq))

def parse(eq):
    
    def is_float(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    tokens = tokenize(eq)

    var_const = {}

    for t in tokens:
        if is_float(t):
            var_const[t] = nodes.constant_node(float(t))
        else:
            var_const[t] = nodes.variable_node(t)

    return var_const

def construct_slp(eq):
    var_const = parse(eq)

    terms = re.split("[+]|-",eq)

    operators = ['*','/','+']

    for term in terms:
        sub_start = 0
        for i in len(term):
            if term[i] in operators:
                for j in range(i,len(term)):
                        if term[j] in operators:
                            if term[i] == '*':
                                temp = nodes.product_gate(var_const[term[0:i]],var_const[term[i+1:j]])

def read_in_slp(file):
    
    def parse_expression(terms,gate_dict):
        if terms[0] in gate_dict:
            left = gate_dict[terms[0]]
        else:
            gate_dict[terms[0]] = nodes.variable_node(terms[0])
            left = gate_dict[terms[0]]

        if terms[1] in gate_dict:
            right = gate_dict[terms[1]]
        else:
            gate_dict[terms[1]] = nodes.variable_node(terms[1])
            right = gate_dict[terms[1]]

        return left,right,gate_dict

    f = open(file,'r',newline='')
    gate_dict = {}
    for line in f:
        if "OUTPUT:" in line:
            line = line.strip().split(':')[1].split(',')
            output_gates = []
            for i in line:
                output_gates.append(gate_dict[i])
            output = nodes.output_node(output_gates)
            return output

        line = line.split('=')
        gate_name = line[0].strip()
        expression = line[1].strip()
        
        if 'C' in gate_name:
            gate_dict[gate_name] = nodes.constant_node(float(expression))
        
        else:
            if '+' in expression:
                terms = expression.split('+')
                terms = [t.strip() for t in terms]
                left,right,gate_dict = parse_expression(terms,gate_dict)
                gate_dict[gate_name] = nodes.sum_node(left,right)

            elif '*' in expression:
                terms = expression.split('*')
                terms = [t.strip() for t in terms]
                left,right,gate_dict = parse_expression(terms,gate_dict)
                gate_dict[gate_name] = nodes.product_node(left,right)

            elif '/' in expression:
                terms = expression.split('/')
                terms = [t.strip() for t in terms]
                left,right,gate_dict = parse_expression(terms,gate_dict)
                gate_dict[gate_name] = nodes.division_node(left,right)