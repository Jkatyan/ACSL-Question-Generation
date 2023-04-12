# Logic Expression

The goal is to generate random logic expression and simplify it. Step 1 is to generate a random tree with operators like AND, OR, NOT and put A, B, C at leaves. Note that NOT takes only one argument but AND/OR take 2 arguments. Step 2 is to simplify the logic expreesion. A similar application is [boolean-algebra](https://www.boolean-algebra.com/).

## Random logic expression generator

There are some algorithms to generate a random tree. One of the famous algorithm is utilize the Prüfer sequence to uniformly randomly convert to a tree. However, such tree may be a multi-branch tree. At our current work phase, we need a tree that each node has two or one child. 

So we start with a simple algorithm: starting from the root, randomly choose the number of nodes in each subtree, then recurse. Note that such algorithm does not enforce uniform distribution of results and will heavily favor balanced trees. (Proof: Catalan numbers for the related combinatorics)

The random mechanism can be continuously improved with need. Check [a related blog](https://stackoverflow.com/questions/56873764/how-to-randomly-generate-a-binary-tree-given-the-node-number).

**Current version note:** For each node, we have a subtree size `n` for it, and do a random dice for the `left subtree size`. Thus, when the `left subtree size` is `0` or `n-1`, the current node only has one child. (one child means only `!` is appliable.) So we didn't specifically directly give a proportion of the choice of the operators.

In this way, the propotion of `[! & |]` operators is affected by the size of tree `n`. For example, if the total number of the tree is 7 (`n^2-1`), the tree is more likely to be **balanced**, or say less `!`. On the contrary, if the size is 8 or 9, one child branch seems to occur more.

## Logic expression simplify

We utilize the `sympy` math toolbox. Check the [logic API doc](https://docs.sympy.org/latest/modules/logic.html).

## Installation

Environment Preparation

key package dependencies
```
python3
sympy
```

or just create an env with conda

```
conda create --name <env> --file requirements.txt
```

## Do a quick run.
Note that the random tree size `n` can be set of function `random_binary_tree()`. The random control can be set throgh `random.seed(10)` at line4 of `tree_generator.py`
```zsh
python simplifier.py
```

The parameter of the generation function: `n` the size of the total items (operators and variables) in the expression; `vars` the number of possible variables (A,B, C, etc.) to occur. `const` whether `0` or `1` is allowed in the expression.
```python
root = random_binary_tree(n=7, vars=3, const=True)
```

Run result examples
```
└──&
    ├──!
    |   └──&
    |       ├──C
    |       └──1
    └──!
        └──B
1. A random logic expression:
         ((~(C & 1)) & (~B))
2. Simplify it:
         ~B & ~C
3. Is is satisfiable?
         Yes
4. All satisfying assignments:
        {B : False,     C : False,      }
```