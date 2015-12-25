'''
test suite
'''
import slp.core.nodes as nodes
import slp.utils.poly_utils as poly_utils
import slp.poly.poly_operations as poly_ops
import slp.utils.debugging as debugging
import slp.utils.parser as parser
import slp.core.node_utils as node_utils
import numpy as np

def basic_poly_test():

    '''
    f = 3x+5y evaluated at (1,3) giving f(1,3) = 18
    '''

    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    v_1 = nodes.variable_node()
    s_0 = nodes.product_node(c_0,v_0)
    s_1 = nodes.product_node(c_1,v_1)
    s_2 = nodes.sum_node(s_0,s_1)
    output = nodes.output_node([s_2])

    print(output.evaluate({v_0:1,v_1:3})==[18])



def derivative_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    v_1 = nodes.variable_node()
    s_0 = nodes.sum_node(c_0,v_0)
    s_1 = nodes.sum_node(c_1,v_1)
    p_0 = nodes.product_node(s_0,s_1)

    d = p_0.differentiate(v_0)

    output = nodes.output_node([p_0,d])
    
    #f(x,y) = 3x+5y
    #f'(x,y) = 3

    debugging.display_polynomial(p_0)

    print(output.evaluate({v_0:2,v_1:3}))


def input_test():
    n = parser.read_in_slp('sample_slp_input.txt').nodes[0] 
    #print(node_utils.get_variable_dependencies(n))
    print(node_utils.get_all_dependencies(n))
    print(debugging.display_polynomial(n))

def matrix_determinant_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    s_0 = nodes.sum_node(c_0,v_0)
    m = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    d = nodes.determinant_node(m)

    '''
    [3 5
     v v+3]

     evaluated at v = 2

     [3 5
      2 5]  = 5
    '''
    output = nodes.output_node([d])
    print(output.evaluate({v_0:2}))

def matrix_sum_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    s_0 = nodes.sum_node(c_0,v_0)
    m_1 = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    m_2 = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    s_1 = nodes.sum_node(m_1,m_2)
    output = nodes.output_node([s_1])
    print(output.evaluate({v_0:2}))

def matrix_derivative_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    s_0 = nodes.product_node(c_0,v_0)
    m = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    d = m.differentiate(v_0)
    output = nodes.output_node([d])
    print(output.evaluate({v_0:2}))

def matrix_determinant_derivative_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    s_0 = nodes.sum_node(c_0,v_0)
    m = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    #print(m.matrix)
    det = nodes.determinant_node(m)
    d = det.differentiate(v_0)

    '''
    3 5
    x 3+x
    '''

    '''
    9+3x-5x = 9-2x
    '''



    output = nodes.output_node([det,d])
    print(output.evaluate({v_0:2}))


def matrix_solve_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    v_1 = nodes.variable_node()
    v_2 = nodes.variable_node()
    s_0 = nodes.sum_node(c_0,v_0)
    s_1 = nodes.sum_node(v_1,v_2)
    a = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    b = nodes.matrix_node([[c_1,s_1],[v_1,v_2]])
    s = nodes.solver_node(a,b)

    output = nodes.output_node([s])

    print(output.evaluate({v_0:2,v_1:3,v_2:5}))

def matrix_solve_derivative_test():
    c_0 = nodes.constant_node(3)
    c_1 = nodes.constant_node(5)
    v_0 = nodes.variable_node()
    s_0 = nodes.sum_node(c_0,v_0)
    a = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    b = nodes.matrix_node([[c_0,c_1],[v_0,s_0]])
    s = nodes.solver_node(a,b)
    d = s.differentiate(v_0)
    output = nodes.output_node([d])
    print(output.evaluate({v_0:2}))


def vector_solve_test():
    c_0 = nodes.constant_node(-1)
    c_1 = nodes.constant_node(1)
    c_2 = nodes.constant_node(0)
    c_3 = nodes.constant_node(2)
    m = nodes.matrix_node([[c_3,c_2,c_3],[c_3,c_2,c_0],[c_1,c_1,c_1]])
    v = nodes.vector_node([c_1,c_1,c_1])
    s = nodes.solver_node(m,v)
    output = nodes.output_node([s])
    print(output.evaluate({}))  


print("Basic Polynomial Test:\n")
basic_poly_test()
print("\n\n")

print("Basic Derivative Test:\n")
derivative_test()
print("\n\n")

print("Basic Input File Test:\n")
input_test()
print("\n\n")

print("Basic Matrix Sum Test:\n")
matrix_sum_test()
print("\n\n")

print("Basic Determinant Test:\n")
matrix_determinant_test()
print("\n\n")

print("Basic Matrix Derivative Test:\n")
matrix_derivative_test()
print("\n\n")

print("Basic Determinant Derivative Test:\n")
matrix_determinant_derivative_test()
print("\n\n")

print("Basic Solve Test:\n")
matrix_solve_test()
print("\n\n")

print("Basic Solve Derivative Test:\n")
matrix_solve_derivative_test()
print("\n\n")