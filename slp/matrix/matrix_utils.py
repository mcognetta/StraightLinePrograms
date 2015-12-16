import slp.core.nodes as nodes
import numpy as np

def jacobian(functions,variables):
	#assert len(functions) == len(variables)

		#m = np.empty((len(functions),len(variables)))
		m = [[0 for x in range(len(functions))] for x in range(len(variables))] 
		for i in range(len(functions)):
			for j in range(len(variables)):
				m[i][j] = functions[i].differentiate(variables[j])
		matrix = nodes.matrix_node(m)
		return matrix


