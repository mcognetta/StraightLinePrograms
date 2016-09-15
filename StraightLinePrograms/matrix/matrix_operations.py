import slp.core.nodes as nodes
import numpy as np
import slp.matrix.matrix_utils as matrix_utils

def solve_linear_equation(a,b):
	assert type(a) == nodes.matrix_node and type(b) == nodes.vector_node, "must have inputs that are a matrix and a vector"

	solution = np.solve(a,b).tolist()

	return nodes.vector_node(solution)

def transpose_matrix(m):

	assert type(m) == nodes.matrix, "Input must be a matrix"

	matrix = matrix_utils.slp_to_numpy(m).np.transpose()

	return nodes.matrix_node(matrix_utils.numpy_to_slp(matrix))
