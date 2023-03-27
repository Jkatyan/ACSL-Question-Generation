#Author: Mandar (mandarsharma@vt.edu)

import random
from treelib import Node, Tree

# Global variables
DEPTH = 2
ALGEBRA = False

def build_random_tree(depth, algebra):
	operators = ['a','b','x','y','m','n']
	operands = ['+','-','*','/','^']
	random_tree = Tree()
	node_id = 1
	parent_id = 0
	random_tree.create_node(operands[random.randint(0,4)], node_id, parent=None)
	while random_tree.depth() <= (depth-1):
		if random_tree.depth() < (depth-1):
			for enum, i in enumerate(range(2**(random_tree.depth()+1))):
				if enum%2 == 0:
					parent_id += 1
				node_id += 1
				random_tree.create_node(operands[random.randint(0,4)], node_id, parent = parent_id)
		else:
			for enum, i in enumerate(range(2**(random_tree.depth()+1))):
				if enum%2 == 0:
					parent_id += 1
				node_id += 1
				if algebra == True:
					choice = random.randint(0,1)
					if choice == 0:
						random_tree.create_node(str(random.randint(1,9)), node_id, parent = parent_id)
					else:
						random_tree.create_node(operators[random.randint(0,5)], node_id, parent = parent_id)
				else:
					random_tree.create_node(str(random.randint(1,9)), node_id, parent = parent_id)                    
	return random_tree


def traversals(tree):
	tree_depth = tree.depth()
	dfs = [tree[node].tag for node in tree.expand_tree(mode=Tree.DEPTH)]
	postfix = ' '.join([x for x in dfs[::-1]])
	#Infix
	if tree_depth == 1:
		infix = dfs[2] + ' ' + dfs[0] + ' ' + dfs [1]
	else:
		infix = []
		dfs_rev = dfs[::-1]
		i = 0
		while i < len(dfs):
			if i == 28:
				infix.insert(i+11, dfs_rev[i])
				i += 1
				infix.insert(i+5, dfs_rev[i])
				i += 1
				infix.insert(i-7, dfs_rev[i])
				i += 1
			elif i == 21:
				infix.insert(i+7, dfs_rev[i])
				i += 1
			elif i==13:
				infix.insert(i+3, dfs_rev[i])
				i += 1
				infix.insert(i-3, dfs_rev[i])
				i += 1
			elif i == 6 or i == 21:
				infix.insert(i-1, dfs_rev[i])
				i += 1
			else:
				chunk = dfs_rev[i:i+3]
				infix.extend([ '(', chunk[0], chunk[2], chunk[1], ')'])
				i = i + 3
	#Prefix
	if tree_depth == 1:
		prefix = dfs[0] + ' ' + dfs[2] + ' ' + dfs [1]
	else:
		prefix = []
		dfs_rev = dfs[::-1]
		i = 0
		while i < len(dfs):
			if i == 28:
				prefix.insert(i-6, dfs_rev[i])
				i += 1
				prefix.insert(i-14, dfs_rev[i])
				i += 1
				prefix.insert(0, dfs_rev[i])
				i += 1
			elif i == 21:
				prefix.insert(i-6, dfs_rev[i])
				i += 1
			elif i == 13:
				prefix.insert(i-6, dfs_rev[i])
				i += 1
				prefix.insert(0, dfs_rev[i])
				i += 1
			elif i == 6:
				prefix.insert(0, dfs_rev[i])
				i += 1
			else:
				chunk = dfs_rev[i:i+3]
				prefix.extend([chunk[2], chunk[0], chunk[1]])
				i = i + 3
		infix = ' '.join([x for x in infix])
		prefix = ' '.join([x for x in prefix])
	return prefix, postfix, infix


def config(depth=None, algebra=None):
	global DEPTH, ALGEBRA
	if depth: DEPTH = depth
	if algebra: ALGEBRA = algebra


def main():
	global DEPTH, ALGEBRA

	expression_tree = build_random_tree(DEPTH, ALGEBRA)
	expression_tree.show(line_type="ascii-em")

	prefix, postfix, infix = traversals(expression_tree)

	print("Prefix: ", prefix)
	print("Postfix: ", postfix)
	print("Infix: ", infix)


if __name__ == '__main__':
	main()
