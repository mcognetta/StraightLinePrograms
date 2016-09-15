'''
nodes.py

Contains code for the graph based SLP

Currently has code for basic variables, constants, and binary operation nodes
'''

'''
derivative check if v is a variable node
'''

import numpy as np

class node:
    
    value_dict = {}

    def __init__(self,name=None):
        self.name = None

class constant_node(node):
    def __init__(self,val,name=None):
        self.val = val
        self.name = name

    def __str__(self):
        return str(self.val)

    __repr__ = __str__

    def evaluate(self):
        return self.val

    def differentiate(self,v,zero=None,one=None):
        if zero == None:
            zero = constant_node(0)
        return zero

class variable_node(node):  
    def __init__(self,name=None):
        self.name = name

    def evaluate(self):
        return self.value_dict[self]

    def differentiate(self,v,zero=None,one=None):
        '''
        differentiate with respect to v
        '''
        if zero == None:
            zero = constant_node(0)
        if one == None:
            one = constant_node(1)
        if v == self:
            return one
        else:
            return zero

class vector_node(node):
    def __init__(self,vector,name=None):
        self.name = name
        self.vector = np.array(vector)

    def evaluate(self):
        if self in self.value_dict:
            return self.value_dict[self]
        else:
            c = self.vector.copy()
            for i in range(len(c)):
                c[i] = c[i].evaluate()
            self.value_dict[self] = c
            return self.value_dict[self]
    
    def differentiate(self,v,zero=None,one=None):
        c = self.matrix.copy()
        for i in range(len(c)):
            c[i] = c[i].differentiate(v,zero,one)
        return vector_node(c)


class matrix_node(node):
    def __init__(self,matrix,name=None):
        self.matrix = np.matrix(matrix)
        self.name = name

    def evaluate(self):
        size = self.matrix.shape[0]
        c = self.matrix.copy()
        for i in range(size):
            for j in range(size):
                c[i,j] = c[i,j].evaluate()
        self.value_dict[self] = c
        return self.value_dict[self]

    def differentiate(self,v,zero=None,one=None):
        c = self.matrix.copy()
        size = self.matrix.shape[0]
        for i in range(size):
            for j in range(size):
                c[i,j] = c[i,j].differentiate(v,zero,one)
        return matrix_node(c)

class sum_node(node):
    def __init__(self,operand_1,operand_2):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.operation = "+"
        self.val_list = None

    def evaluate(self):
        if(self in self.value_dict):
            return self.value_dict[self]
        else:
            self.value_dict[self] = self.operand_1.evaluate() + self.operand_2.evaluate()
            return self.value_dict[self]

    def differentiate(self,v,zero=None,one=None):
        return sum_node(self.operand_1.differentiate(v,zero,one),self.operand_2.differentiate(v,zero,one))
        
class product_node(node):
    def __init__(self,operand_1,operand_2):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.operation = "*"
    def evaluate(self):
        if(self in self.value_dict):
            return self.value_dict[self]
        else:
            self.value_dict[self] = self.operand_1.evaluate()*self.operand_2.evaluate()
            return self.value_dict[self]
    def differentiate(self,v,zero=None,one=None):
        p_0 = product_node(self.operand_1,self.operand_2.differentiate(v,zero,one))
        p_1 = product_node(self.operand_2,self.operand_1.differentiate(v,zero,one))
        return sum_node(p_0,p_1)

class division_node(node):
    def __init__(self,operand_1,operand_2):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.operation = "/"
    def evaluate(self):
        if(self in val_list):
            return val_list[self]
        else:
            if self.operand_2.evaluate(val_list) == 0:
                raise ZeroDivisionError
            else:
                val_list[self] = self.operand_1.evaluate(val_list)/self.operand_2.evaluate(val_list)
                return val_list[self]
    def differentiate(self,v,zero=None,one=None):
        '''
        f/g -> f'g-g'f/(g^2)
        '''
        p_0 = product_node(self.operand_1.differentiate(v,zero,one),self.operand_2)
        p_1 = product_node(self.operand_2.differentiate(v,zero,one),self.operand_1)
        neg = constant_node(-1)
        p_2 = product_node(neg,p_1)
        p_3 = product_node(self.operand_2,self.operand_2)
        s_0 = sum_node(p_0,p_2)
        return division_node(s_0,p_3)

class determinant_node(node):
    def __init__(self,operand):
        self.operand = operand
    def evaluate(self):


        if self in self.value_dict:
            return self.value_dict[self]
        else:
            def prepare_matrix(operand):
                size = operand.matrix.shape
                m = np.zeros(size)

                for i in range(size[0]):
                    for j in range(size[1]):
                        if type(operand.matrix.item(i,j)) == constant_node:
                            m[i][j] = operand.matrix.item(i,j).val
                        else:
                            if type(operand.matrix.item(i,j)) == variable_node:
                                m[i][j] = self.value_dict[operand.matrix.item(i,j)]
                            else:
                                m[i][j] = operand.matrix.item(i,j).evaluate()
                return m

            self.value_dict[self] = np.linalg.det(prepare_matrix(self.operand))
            return self.value_dict[self]

    def differentiate(self,v,zero=None,one=None):
        size = self.operand.matrix.shape[0]
        copies = []
        for s in range(size):
            copies.append(matrix_node(self.operand.matrix.copy()))
        for i in range(len(copies)):
            for j in range(size):
                copies[i].matrix[j,i] = copies[i].matrix[j,i].differentiate(v,zero,one)
        for i in range(len(copies)):
            copies[i] = determinant_node(copies[i])
        s_0 = sum_node(copies[0],copies[1])
        sums = [s_0]
        for i in range(2,len(copies)):
            sums.append(sum_node(copies[i],sums[-1]))
        return sums[-1]

class solver_node(node):
    def __init__(self,operand_1,operand_2):
        '''
        Ax=B
        operand_1 is A
        operand_2 is B
        returns x
        '''
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def evaluate(self):
        if self in self.value_dict:
            return self.value_dict[self]
        else:
            self.value_dict[self] = np.linalg.solve(self.operand_1.evaluate(),self.operand_2.evaluate())
            return self.value_dict[self]
    def differentiate(self,v,zero=None,one=None):
        Y = solver_node(self.operand_1,self.operand_2)
        dA = self.operand_1.differentiate(v,zero,one)
        dB = self.operand_2.differentiate(v,zero,one)
        dAY = product_node(dA,Y)
        negative = constant_node(-1)
        negdAY = product_node(negative,dAY)
        rhs = sum_node(dB,negdAY)
        return solver_node(self.operand_1,rhs)


class output_node(node):
    def __init__(self,nodes):
        self.nodes = nodes
    def evaluate(self,values):
        output = []
        self.value_dict.clear()
        self.value_dict.update(values)
        for n in self.nodes:
            if n in self.value_dict:
                output.append(self.value_dict[n])
            else:
                n.evaluate()
                output.append(self.value_dict[n])
        return output

zero = constant_node(0)
one = constant_node(1)
neg = constant_node(-1)


object_nodes = [variable_node,constant_node,vector_node,matrix_node,output_node]
operation_nodes = [sum_node,product_node,division_node,determinant_node,solver_node]