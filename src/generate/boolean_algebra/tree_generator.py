import random

class Node(object):
  def __init__(self, data=None):
    self.data = data
    self.children = []

  def add_child(self, obj):
    self.children.append(obj)

def add_random_negations(root):
  if not root:
    return
  
  if random.random() < 0.5: # 50% chance of negating the subtree
    if root.data == '&':
      root.data = '|'
    elif root.data == '|':
      root.data = '&'
    elif root.data != '!':
      root.data = '!' + root.data
    
    for child in root.children:
      add_random_negations(child)
  else:
    for child in root.children:
      add_random_negations(child)

def helper(n=10, vars=3, unique=2, const=False, lst=None):
  # Probability of generating constant values
  CONST_PROBABILITY = 0.1

  const_list = ['0', '1']
  var_list = ['A', 'B', 'C', 'D', 'G', 'H', 'K', 'M', 'P', 'U', 'W']

  if (n == 0):
    return None
  
  if not lst:
    random.shuffle(var_list)
    lst = random.sample(var_list[:vars], unique)

  # Number of nodes in the left subtree (in [0, n-1])
  for _ in range(5): # Increase this value to make ~ less likely
    left_subtree_size = random.randrange(n)
    if left_subtree_size == 1:
      break
    if left_subtree_size != 0 and left_subtree_size != n - 1:
      break

  if n == 1:
    if const:
      prob = CONST_PROBABILITY * 10
      combined = int(prob) * const_list + int((10 - prob)) * lst
      root = Node(random.choice(combined))
    else:
      root = Node(random.choice(lst))
  elif left_subtree_size == 0 or left_subtree_size == n - 1:
    root = Node('!')
  else:
    root = Node(random.choice(['&', '|']))
  
  # Recursively build each subtree
  root.add_child(helper(left_subtree_size, vars, unique, const, lst=lst))
  root.add_child(helper(n - left_subtree_size - 1, vars, unique, const, lst=lst))
  return root

def random_binary_tree(n=10, vars=3, unique=2, const=False, lst=None):
  root = helper(n=n, vars=vars, unique=unique, const=const, lst=None)
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
