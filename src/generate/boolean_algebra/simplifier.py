import random
from sympy import Not
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
UNIQUE = 2
CONST = False

def config(type=None, n=None, vars=None, unique=None, const=None):
    global TYPE, N, VARS, UNIQUE, CONST
    if type: TYPE = type
    if n: N = n
    if vars: VARS = vars
    if unique: UNIQUE = unique
    if const: CONST = const

def generate_question_1():
    global N, VARS, UNIQUE, CONST

    # Question
    root = random_binary_tree(N, VARS, UNIQUE, CONST)
    logic_str = tree_str(root)
    print(f"Simplify {logic_str}.")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    print(simplified_str)

def generate_question_2():
    global N, VARS, UNIQUE, CONST

    # Question
    root = random_binary_tree(N, VARS, UNIQUE, CONST)
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
    global N, VARS, UNIQUE, CONST

    # Question
    root = random_binary_tree(N, VARS, UNIQUE, CONST)
    logic_str = tree_str(root)
    print(f"Identify all satisfying assignments for {logic_str}.")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    models = satisfiable(simplified_str, all_models=True)

    empty = True
    for model in models:
        if model:
            string = '{'
            for key in sorted(model.keys(), key=lambda x: str(x)):
                if str(key) != 'True' and str(key) != 'False':
                    string += str(key) + ": " + str(model[key]) + ", "
            if len(string) > 1:
                print(string[:-2] + '}')
                empty = False
        else:
            print("The expression is unsatisfiable.")
            return

    if empty:
        print("The expression is always satisfiable.")

def generate_question_4():
    global N, VARS, UNIQUE, CONST

    # Question
    root = random_binary_tree(N, VARS, UNIQUE, CONST)
    logic_str = tree_str(root)
    print(f"How many ordered pairs make {logic_str} true?")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    models = satisfiable(simplified_str, all_models=True)

    logic_str = logic_str.replace('x', '0')
    logic_str = logic_str.replace('y', '1')

    count = 0
    for model in models:
        if model:
            string = '{'
            for key in sorted(model.keys(), key=lambda x: str(x)):
                if str(key) != 'True' and str(key) != 'False':
                    string += str(key) + ": " + str(model[key]) + ", "
            if len(string) > 1:
                count += 1
        else:
            print(f"0 pairs make {logic_str} true.")
            return

    if count == 1:
        print(f"1 pair makes {logic_str} true.")
    else:
        print(f"{count} pairs make {logic_str} true.")

def generate_question_5():
    global N, VARS, UNIQUE, CONST

    # Question
    root = random_binary_tree(N, VARS, UNIQUE, CONST)
    logic_str = tree_str(root)
    print(f"How many ordered pairs make {logic_str} false?")

    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(Not(logic_exp))
    models = satisfiable(simplified_str, all_models=True)

    logic_str = logic_str.replace('x', '0')
    logic_str = logic_str.replace('y', '1')

    count = 0
    for model in models:
        if model:
            string = '{'
            for key in sorted(model.keys(), key=lambda x: str(x)):
                if str(key) != 'True' and str(key) != 'False':
                    string += str(key) + ": " + str(model[key]) + ", "
            if len(string) > 1:
                count += 1
        else:
            print(f"All pairs make {logic_str} false.")
            return

    if count == 1:
        print(f"1 pair makes {logic_str} false.")
    else:
        print(f"{count} pairs make {logic_str} false.")

def generate_question_6():
    global N, VARS, UNIQUE, CONST

    # Question
    root = random_binary_tree(N, VARS, UNIQUE, CONST)
    logic_str = tree_str(root)
    print(f"Is {logic_str} a tautology?")
    
    # Answer
    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    
    if simplified_str == True:
        print("Yes, this is a tautology.")
    else:
        print("No, this is not a tautology.")

def main():
    global TYPE

    if TYPE == 0:
        num = random.randint(1, 6)
        eval(f'generate_question_{num}()')
    else:
        eval(f'generate_question_{TYPE}()')

if __name__ == "__main__":
    main()