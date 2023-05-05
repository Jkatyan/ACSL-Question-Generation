#Author: Mandar (mandarsharma@vt.edu)

import random
from treelib import Node, Tree

# Global variables
TYPE = 0    # Which type of question should be generated?
            # 0: Random
            # 1: Prefix (numeric)
            # 2: Postfix (numeric)
            # 3: Infix (numeric)
            # 4: Evaluate prefix
            # 5: Evaluate postfix
            # 6: Convert between types (numeric)
            # 7: Convert between types (algebra)
            # 8: Prefix (algebra)
            # 9: Postfix (algebra)
            # 10: Infix (algebra)
DEPTH = 2
ALGEBRA = False
FORCE_ALGEBRA = False

CURRENT = 1

def config(type=None, depth=None, algebra=None):
    global TYPE, DEPTH, ALGEBRA
    if type != None: TYPE = type
    if depth != None: DEPTH = depth
    if algebra != None: ALGEBRA = algebra

def build_random_tree(depth, algebra):
    global FORCE_ALGEBRA

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
                if FORCE_ALGEBRA == True:
                    random_tree.create_node(operators[random.randint(0,5)], node_id, parent = parent_id)
                else:
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

def evaluate_prefix(expression):
    size = -1
    items = []

    def isEmpty():
        nonlocal size, items
        return size == -1
        
    def push(item):
          nonlocal size, items
          items.append(item)
          size += 1

    def pop():
        nonlocal size, items
        if isEmpty():
            return 0
        else:
            size -= 1
            return items.pop()
        
    def evaluate(expr):
        for i in reversed(expr):
            if i in '0123456789':
                push(i)
            else:
                op1 = pop()
                op2 = pop()
                result = cal(op1,op2,i)
                push(result)
        return pop()
    
    def cal(op1, op2, i):
        if i == '*':
            return int(op1)*int(op2)
        elif i == '/':
            return int(op1)/int(op2)
        elif i == '+':
            return int(op1)+int(op2)
        elif i == '-':
            return int(op1)-int(op2)
        elif i == '^':
            return int(op1)^int(op2)
        
    return evaluate(expression.replace(" ", ""))

def evaluate_postfix(expression):
    items = []
    size = -1

    def isEmpty():
        nonlocal size, items
        return items == []
    
    def push(item):
        nonlocal size, items
        items.append(item)
        size += 1

    def pop():
        nonlocal size, items
        if isEmpty():
            return 0
        else:
            size -= 1
            return items.pop()
        
    def evaluate(expr):
        for i in expr:
            if i in '0123456789':
                push(i)
            else:
                op1 = pop()
                op2 = pop()
                result = cal(op2,op1,i)
                push(result)
        return pop()
    
    def cal(op2,op1,i):
        if i == '*':
            return int(op2)*int(op1)
        elif i == '/':
            return int(op2)/int(op1)
        elif i == '+':
            return int(op2)+int(op1)
        elif i == '-':
            return int(op2)-int(op1)
        elif i == '^':
            return int(op1)^int(op2)
        
    return evaluate(expression.replace(" ", ""))

def generate_question_1():
    global DEPTH, ALGEBRA

    print("Question:")
    print("Find the prefix expression for this expression tree:")
    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expression_tree.show(line_type="ascii-em")
    prefix, postfix, infix = traversals(expression_tree)
    print("Answer:")
    print(prefix)

def generate_question_2():
    global DEPTH, ALGEBRA

    print("Question:")
    print("Find the postfix expression for this expression tree:")
    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expression_tree.show(line_type="ascii-em")
    prefix, postfix, infix = traversals(expression_tree)
    print("Answer:")
    print(postfix)

def generate_question_3():
    global DEPTH, ALGEBRA

    print("Question:")
    print("Find the infix expression for this expression tree:")
    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expression_tree.show(line_type="ascii-em")
    prefix, postfix, infix = traversals(expression_tree)
    print("Answer:")
    print(infix)

def generate_question_4():
    global DEPTH, ALGEBRA

    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    prefix, postfix, infix = traversals(expression_tree)
    ans = evaluate_prefix(prefix)

    while not isinstance(ans, int):
        expression_tree = build_random_tree(DEPTH, ALGEBRA)
        prefix, postfix, infix = traversals(expression_tree)
        ans = evaluate_prefix(prefix)

    print("Question:")
    print(f"Evaluate the prefix expression: {prefix}")
    print("Answer:")
    print(ans)

def generate_question_5():
    global DEPTH, ALGEBRA

    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    prefix, postfix, infix = traversals(expression_tree)
    ans = evaluate_postfix(postfix)

    while not isinstance(ans, int):
        expression_tree = build_random_tree(DEPTH, ALGEBRA)
        prefix, postfix, infix = traversals(expression_tree)
        ans = evaluate_postfix(postfix)

    print("Question:")
    print(f"Evaluate the postfix expression: {postfix}")
    print("Answer:")
    print(ans)

def generate_question_6():
    global DEPTH, ALGEBRA

    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expressions = traversals(expression_tree)

    a = random.randint(0, 2)
    b = random.randint(0, 2)
    while (a == b):
        b = random.randint(0, 2)

    if a == 0: strA = 'prefix'
    elif a == 1: strA = 'postfix'
    else: strA = 'infix'

    if b == 0: strB = 'prefix'
    elif b == 1: strB = 'postfix'
    else: strB = 'infix'

    print("Question:")
    print(f"Convert {strA} to {strB}: {expressions[a]}")
    print("Answer:")
    print(expressions[b])

def generate_question_7():
    global DEPTH, ALGEBRA, FORCE_ALGEBRA

    FORCE_ALGEBRA = True

    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expressions = traversals(expression_tree)

    FORCE_ALGEBRA = False

    a = random.randint(0, 2)
    b = random.randint(0, 2)
    while (a == b):
        b = random.randint(0, 2)

    if a == 0: strA = 'prefix'
    elif a == 1: strA = 'postfix'
    else: strA = 'infix'

    if b == 0: strB = 'prefix'
    elif b == 1: strB = 'postfix'
    else: strB = 'infix'

    print("Question:")
    print(f"Convert {strA} to {strB}: {expressions[a]}")
    print("Answer:")
    print(expressions[b])

def generate_question_8():
    global DEPTH, ALGEBRA, FORCE_ALGEBRA

    print("Question:")
    print("Find the prefix expression for this expression tree:")
    FORCE_ALGEBRA = True
    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expression_tree.show(line_type="ascii-em")
    FORCE_ALGEBRA = False
    prefix, postfix, infix = traversals(expression_tree)
    print("Answer:")
    print(prefix)

def generate_question_9():
    global DEPTH, ALGEBRA, FORCE_ALGEBRA

    print("Question:")
    print("Find the postfix expression for this expression tree:")
    FORCE_ALGEBRA = True
    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expression_tree.show(line_type="ascii-em")
    FORCE_ALGEBRA = False
    prefix, postfix, infix = traversals(expression_tree)
    print("Answer:")
    print(postfix)

def generate_question_10():
    global DEPTH, ALGEBRA, FORCE_ALGEBRA

    print("Question:")
    print("Find the infix expression for this expression tree:")
    FORCE_ALGEBRA = True
    expression_tree = build_random_tree(DEPTH, ALGEBRA)
    expression_tree.show(line_type="ascii-em")
    FORCE_ALGEBRA = False
    prefix, postfix, infix = traversals(expression_tree)
    print("Answer:")
    print(infix)

def main():
    global TYPE, CURRENT

    if TYPE == 0:
        while True:
            try:
                eval(f'generate_question_{CURRENT}()')
                if CURRENT == 10:
                    CURRENT = 1
                else:
                    CURRENT += 1
                break
            except:
                pass
    else:
        while True:
            try:
                eval(f'generate_question_{TYPE}()')
                break
            except:
                pass
            
if __name__ == '__main__':
    main()
