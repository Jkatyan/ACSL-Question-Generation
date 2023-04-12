import random
import copy

class Node(object):
  def __init__(self, data=None):
    self.data = data
    self.children = []

  def add_child(self, obj):
    self.children.append(obj)

const_list = ['0', '1']
var_list = ['A', 'B', 'C', 'D', 'G', 'H', 'K', 'M', 'P', 'U', 'W']

def random_binary_tree(n=10, vars=3, const=False):
  global CONST_PROBABILITY  

  if (n == 0):
    return None
  
  random.shuffle(var_list)

  # Number of nodes in the left subtree (in [0, n-1])
  left_subtree_size = random.randrange(n)
  # Fill the node operator
  # root = Node(n)
  if n == 1:
    if const:
      root = Node(random.choice(const_list+var_list[:vars]+var_list[:vars]+var_list[:vars]+var_list[:vars]))
    else:
      root = Node(random.choice(var_list[:vars]))
  elif left_subtree_size == 0 or left_subtree_size == n - 1:
    root = Node('!')
  else:
    root = Node(random.choice(['&', '|']))
  
  # Recursively build each subtree
  root.add_child(random_binary_tree(left_subtree_size, vars, const))
  root.add_child(random_binary_tree(n - left_subtree_size - 1, vars, const))
  return root

def print_tree(node, prefix="", is_last=True):
  if node:
    print(prefix, end="")
    print("└──" if is_last else "├──", end="")

    # print the value of the node
    print(node.data)

    # enter the next tree level
    print_list = [x for x in node.children if x]
    for i in range(len(print_list)):
      print_tree(print_list[i], prefix + ("    " if is_last else "|   "), True if i == len(print_list)-1 else False)
  
def tree_str(node):
  ret = ""
  if node:
    if node.data not in ['&', '|', '!']:
      # leaf node
      ret += node.data
    elif node.data == "!":
      # NOT operator
      child_idx = 0 if node.children[0] else 1
      ret += "~" + tree_str(node.children[child_idx])
    else:
      # AND/OR operatot
      ret += tree_str(node.children[0]) + " " + node.data + " " + tree_str(node.children[1])
  if len(ret) > 1:
    ret = "(" + ret + ")"
  return ret
  

if __name__ == "__main__":
  root = random_binary_tree(n=10, vars=2)
  print_tree(root)
  logic_str = tree_str(root)
  print(logic_str)
