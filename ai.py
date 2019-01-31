from __future__ import absolute_import, division, print_function
import copy
import random
import math

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
PLAYER_TYPE = { 0:'MAX', 1:'CHANCE'}
class Gametree:
	"""main class for the AI"""
	# Hint: Two operations are important. Grow a game tree, and then compute minimax score.
	# Hint: To grow a tree, you need to simulate the game one step.
	# Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root_state, depth_of_tree, current_score): 
		self.matrix = root_state
		# print('root initially ', self.matrix)
		self.score = current_score


	# expectimax for computing best move
	def expectimax(self, node):
		if node.isTerminal:
			return node.payoff
		elif node.playerType == 0:
			value = -math.inf
			for n in node.children:
				value = max(value, self.expectimax(n))
			if value != -math.inf:
				node.payoff = value
			return value
		elif node.playerType == 1:
			value = 0
			for n in node.children:
				value = value + self.expectimax(n)*(1/len(node.children))
			if value != -math.inf:
				node.payoff = value
			return value
		else:
			'''Error'''

	# function to return best decision to game

	def compute_decision(self):
		#change this return value when you have implemented the function
		root_node = self.make_root()
		self.growtree(root_node)
		# print('Starting expectimax on root')
		self.expectimax(root_node)
		maximum = -math.inf
		max_index = 0
		for i in range(0, len(root_node.children)):
			if root_node.children[i].payoff > maximum:
				maximum = root_node.children[i].payoff
				max_index = root_node.children[i].move
		# print('Suggesting ', max_index)
		# print('Root ', root_node.state)
		# print('Children')
		# for n in root_node.children:
		# 	print('For move ', n.move, ' and payoff ', n.payoff, ' ', n.state)
		# print('')
		return max_index

	def make_root(self):
		root_node = Node()
		root_node.playerType = 0
		root_node.state = self.matrix
		root_node.isRoot = True
		root_node.payoff = self.score
		root_node.children = []
		root_node.depth = 0
		return root_node

	def weight_calculator(self, state):
		weight_matrix = [[4**15, 4**8, 4**7, 4**0],[4**14, 4**9, 4**6, 4**1], [4**13, 4**10, 4**5, 4**2], [4**12, 4**11, 4**4, 4**3]]
		weight = 0
		for i in range(0,4):
			for j in range(0,4):
				weight = weight + (weight_matrix[i][j]*state[i][j])

		return weight

	def detect_corner_max(self, state):
		maximum = -math.inf
		for i in range(0, len(state)):
			if max(state[i]) >= maximum:
				maximum = max(state[i])

		if state[0][0] == maximum | state[0][3] == maximum | state[3][0] == maximum | state[3][3] == maximum:
			return True
		else:
			return False

	def findEmptyTilesCount(self, state):
		count = 0
		for i in range(0, 4):
			for j in range(0, 4):
				if state[i][j] == 0:
					count = count + 1
		return count

	def growtree(self, root):
		root_node = root
		for i in range(0, 4):
			simulator = Simulator(copy.deepcopy(root_node.state), copy.deepcopy(root_node.payoff))
			child_node = Node()
			child_node.playerType = 1
			simulator.move(i)
			child_node.depth = 1
			child_node.move = i
			child_node.state = simulator.tileMatrix
			child_node.payoff = simulator.total_points
			if child_node.state != root_node.state:
				root_node.children.append(child_node)

		depth_two = []

		for node in root_node.children:
			simulator = Simulator(copy.deepcopy(node.state), copy.deepcopy(node.payoff))
			to_fill = simulator.findEmptyTiles()
			for pair in to_fill:
				child_node = Node()
				child_node.playerType = 0
				child_node.state = copy.deepcopy(simulator.tileMatrix)
				child_node.state[pair[0]][pair[1]] = 2
				child_node.payoff = simulator.total_points
				child_node.depth = 2
				node.children.append(child_node)
				depth_two.append(child_node)

		for node in depth_two:
			for i in range(0, 4):
				simulator = Simulator(copy.deepcopy(node.state), copy.deepcopy(node.payoff))
				child_node = Node()
				child_node.playerType = 1
				simulator.move(i)
				child_node.state = simulator.tileMatrix
				# child_node.payoff = simulator.total_points
				child_node.payoff = self.weight_calculator(child_node.state)
				child_node.isTerminal = True
				if child_node.state != node.state:
					child_node.depth = 3
					node.children.append(child_node)

		# print('root_node ', root_node.state)
		# print('')
		# print('0 child ', root_node.children[0].state, ' score: ', root_node.children[0].payoff)
		# for node in root_node.children[0].children:
		# 	print(node.state, ' score: ', node.payoff)
		# 	for child in node.children:
		# 		print(child.state)
		# print('')
		# print('1 child ', root_node.children[1].state, ' score: ', root_node.children[1].payoff)
		# for node in root_node.children[1].children:
		# 	print(node.state, ' score: ', node.payoff)
		# 	for child in node.children:
		# 		print(child.state)
		# print('')
		# print('2 child ', root_node.children[2].state, ' score: ', root_node.children[2].payoff)
		# for node in root_node.children[2].children:
		# 	print(node.state, ' score: ', node.payoff)
		# 	for child in node.children:
		# 		print(child.state)
		# print('')
		# print('3 child ', root_node.children[3].state, ' score: ', root_node.children[3].payoff)
		# for node in root_node.children[3].children:
		# 	print(node.state, ' score: ', node.payoff)
		# 	for child in node.children:
		# 		print(child.state)
		#
		# exit(0)



class Simulator:
	def __init__(self, matrix, points):
		self.tileMatrix = matrix
		self.total_points = points
		self.board_size = 4

	def move(self, direction):
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		if self.canMove():
			self.moveTiles()
			self.mergeTiles()
			#self.placeRandomTile()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()

	def placeRandomTile(self):
		while True:
			i = random.randint(0,self.board_size-1)
			j = random.randint(0,self.board_size-1)
			if self.tileMatrix[i][j] == 0:
				break
		self.tileMatrix[i][j] = 2

	def findEmptyTiles(self):
		to_fill = []
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.tileMatrix[i][j] == 0:
					to_fill.append([i, j])
		return to_fill

	def rotateMatrixClockwise(self):
		tm = self.tileMatrix
		for i in range(0, int(self.board_size/2)):
			for k in range(i, self.board_size- i - 1):
				temp1 = tm[i][k]
				temp2 = tm[self.board_size - 1 - k][i]
				temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
				temp4 = tm[k][self.board_size - 1 - i]
				tm[self.board_size - 1 - k][i] = temp1
				tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
				tm[k][self.board_size - 1 - i] = temp3
				tm[i][k] = temp4

	def canMove(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(1, self.board_size):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False

	def moveTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, self.board_size - 1):
						tm[i][k] = tm[i][k + 1]
					tm[i][self.board_size - 1] = 0

	def mergeTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for k in range(0, self.board_size - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.total_points += tm[i][k]
					self.moveTiles()

class Node:
	def __init__(self):
		self.playerType = 0
		self.state = []
		self.isTerminal = False
		self.isRoot = False
		self.children = []
		self.payoff = 0
		self.chance = 0
		self.depth = 0
		self.move = 0
