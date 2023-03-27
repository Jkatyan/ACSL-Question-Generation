import random
import matplotlib.pyplot as plt
import networkx as nx

random.seed(10)

tree = nx.random_tree(n=10, seed=0, create_using=nx.DiGraph)
for u in tree.nodes:
  if tree.out_degree(u)==0 and tree.in_degree(u)==1:
    tree.nodes[u]['label'] = random.choice(['A', 'B', 'C'])
  elif tree.out_degree(u) == 1:
    tree.nodes[u]['label'] = '!'
  else:
    tree.nodes[u]['label'] = random.choice(['&', '|'])

print(nx.forest_str(tree))
