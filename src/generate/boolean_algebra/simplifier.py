import random
from sympy.logic import simplify_logic
from sympy.abc import x, y
from sympy.logic.inference import satisfiable
from sympy.parsing.sympy_parser import parse_expr
from .tree_generator import random_binary_tree, print_tree, tree_str

# Globals
TYPE = 0    # Which type of question should be generated?
            # 0: Random
            # 1: Simplify it
            # 2: Is is satisfiable?
            # 3: All satisfying assignments
            # 4: Number of ordered pairs for true
            # 5: Number of ordered pairs for false
            # 6: Tautology

N = 7
VARS = 3
CONST = False

def config(type=None, n=None, vars=None, const=None):
    global TYPE, N, VARS, CONST
    if type: TYPE = type
    if n: N = n
    if vars: VARS= vars
    if const: CONST = const

def generate_question_1():
    global N, VARS, CONST

    # Question
    root = random_binary_tree(N, VARS, CONST)
    logic_str = tree_str(root)
    print(f"Simplify {logic_str}.")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    print(simplified_str)

def generate_question_2():
    global N, VARS, CONST

    # Question
    root = random_binary_tree(N, VARS, CONST)
    logic_str = tree_str(root)
    print(f"Is {logic_str} satisfiable?")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    valid = satisfiable(simplified_str)
    print("No" if not valid else "Yes")

def generate_question_3():
    global N, VARS, CONST

    # Question
    root = random_binary_tree(N, VARS, CONST)
    logic_str = tree_str(root)
    print(f"Identify all satisfying assignments for {logic_str}.")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    models = satisfiable(simplified_str, all_models=True)
    for model in models:
        if model:
            # Do something with the model.
            print("{", end="")
            for key in sorted(model.keys(), key=lambda x: str(x)):
                print(key, ":", model[key], end=' ')
            print("}")
        else:
            # Given expr is unsatisfiable.
            print("The expression is unsatisfiable.")

def generate_question_4():
    global N, VARS, CONST

    # Question
    root = random_binary_tree(N, VARS, CONST)
    logic_str = tree_str(root)
    print(f"How many ordered pairs make {logic_str} true?")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    models = satisfiable(simplified_str, all_models=True)
    count = 0
    for model in models:
        if model:
            count += 1
    print(f"There are {count} pairs that make {logic_str} true.")

def generate_question_5():
    global N, VARS, CONST

    # Question
    root = random_binary_tree(N, VARS, CONST)
    logic_str = tree_str(root)
    print(f"How many ordered pairs make {logic_str} false?")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    models = satisfiable(simplified_str, all_models=True)
    count = 0
    for model in models:
        if model:
            count += 1
    print(f"There are {2 ** VARS - count} pairs that make {logic_str} false.")

def generate_question_6():
    global N, VARS, CONST

    # Question
    root = random_binary_tree(N, VARS, CONST)
    logic_str = tree_str(root)
    print(f"Is {logic_str} a tautology?")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    models = satisfiable(simplified_str, all_models=True)
    count = 0
    for model in models:
        if model:
            count += 1
    if count == 2 ** VARS:
        print("Yes this is a tautology.")
    else:
        print("No this is not a tautology.")

def main():
    global TYPE

    if TYPE == 0:
        num = random.randint(1, 6)
        eval(f'generate_question_{num}()')
    else:
        eval(f'generate_question_{TYPE}()')

if __name__ == "__main__":
    main()