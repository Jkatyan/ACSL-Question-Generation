import os
import json
from sympy.logic import simplify_logic
from sympy.abc import x, y
from sympy.logic.inference import satisfiable
from sympy.parsing.sympy_parser import parse_expr
from .tree_generator import random_binary_tree, print_tree, tree_str

# Global variables
N = None
VARS = None
CONST = None

def config(n=None, vars=None, const=None):
    global N, VARS, CONST
    if n: N = n
    if vars: VARS= vars
    if const: CONST = const

def main():
    global N, VARS, CONST

    root = random_binary_tree(N, VARS, CONST)
    print_tree(root)
    logic_str = tree_str(root)
    print("1. A random logic expression:\n\t", logic_str)

    logic_str = logic_str.replace('0', 'x')
    logic_str = logic_str.replace('1', 'y')
    logic_exp = parse_expr(logic_str).subs({x: False, y: True})
    simplified_str = simplify_logic(logic_exp)
    print("2. Simplify it:\n\t", simplified_str)

    valid = satisfiable(simplified_str)
    print("3. Is is satisfiable?\n\t", "No" if not valid else "Yes")

    print("4. All satisfying assignments:")
    models = satisfiable(simplified_str, all_models=True)
    for model in models:
        if model:
            # Do something with the model.
            print("\t{", end="")
            for key in sorted(model.keys(), key=lambda x: str(x)):
                print(key, ":", model[key], end=',\t')
            print("}")
        else:
            # Given expr is unsatisfiable.
            print("\tUNSAT")


if __name__ == "__main__":
    main()
