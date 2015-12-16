import slp.core.nodes as nodes
import numpy as np

class subtraction_node:

	def __init__(self,operand_1,operand_2,name=None):
		self.operand_1 = operand_1
		self.operand_2 = operand_2
		self.name = name

	def evaluate(self):
		global nodes.value_dict
		if self in nodes.value_dict


