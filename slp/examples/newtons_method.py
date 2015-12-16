'''
Newtons Method
'''

import slp.core.nodes as nodes
import slp.utils.poly_utils as poly_utils
import slp.poly.poly_operations as poly_ops
import slp.utils.debugging as debugging
import slp.utils.parser as parser
import slp.core.node_utils as node_utils
import numpy as np
import slp.matrix.matrix_utils as matrix_utils


v_0 = nodes.variable_node()
v_1 = nodes.variable_node()
v_2 = nodes.variable_node()

zero = nodes.zero
one = nodes.one
neg = nodes.neg
c_0 = nodes.constant_node(-1)
c_1 = nodes.constant_node(-3)

p_0 = nodes.product_node(v_0,v_0) #x^2
p_1 = nodes.product_node(v_1,v_1) #y^2
p_2 = nodes.product_node(v_2,v_2) #z^2
p_3 = nodes.product_node(v_2,c_0) #-z

s_1 = nodes.sum_node(p_0,p_1) #x^2+y^2
s_2 = nodes.sum_node(s_1,p_2) #(x^2+y^2)+z^2
s_3 = nodes.sum_node(s_1,p_3) #(x^2+y^2)-z
s_4 = nodes.sum_node(v_0,v_1) #x+y
s_5 = nodes.sum_node(s_4,v_2) #(x+y)+z

eq_0 = nodes.sum_node(s_2,c_1) #(x^2+y^2+z^2)-3
eq_1 = nodes.sum_node(s_3,c_0) #(x^2+y^2-z)-1
eq_2 = nodes.sum_node(s_5,c_1) #(x+y+z)-3

print(poly_utils.display_as_poly(eq_0))
print(poly_utils.display_as_poly(eq_1))
print(poly_utils.display_as_poly(eq_2))

functions = [eq_0,eq_1,eq_2] #array of the final functions
variables = [v_0,v_1,v_2] #array of all the variables used
initial_values = [1,0,1]


def newton_test(functions,variables,initial_values,iterations=10): #maybe have an epsilon here as well?
    jacobian = matrix_utils.jacobian(functions,variables) #get the jacobian matrix of the function and variables
    function_vector = nodes.vector_node(functions) #vector representing the functions
    var_vector = nodes.vector_node(variables) #vector of the variables
    
    r_h_s = nodes.product_node(neg,function_vector) #setting up the -f(x) term on the right hand side
    solver = nodes.solver_node(jacobian,r_h_s)
    next_term = nodes.sum_node(solver,var_vector)

    output = nodes.output_node([next_term])
    solution = np.array(initial_values)

    print(solution)
    for i in range(iterations):
        solution = output.evaluate(dict(zip(variables,solution.tolist())))[0]
        print(solution)


newton_test(functions,variables,initial_values)
