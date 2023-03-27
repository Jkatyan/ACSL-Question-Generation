import sys
from io import StringIO

from .logic import boolean_algebra, boolean_algebra_config
from .trees import prefix_infix_postfix, prefix_infix_postfix_config
from .numbers import number_systems, number_systems_config

class Question:
    def __init__(self, function):
        self.name = function
        self.output = []

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        eval(function + '()')
        
        sys.stdout = old_stdout
        self.output = mystdout.getvalue().split('\n')
        self.output.pop()

    def print_output(self):
        print('\n'.join(self.output))


class QuestionList:
    def __init__(self):
        self.list = []

    def add_question(self, question):
        self.list.append(question)

    def generate_questions(self, functions):
        for function in functions:
            for _ in range(function[0]):
                self.add_question(Question(function[1]))

    def configure_parameters(self, function, n=None, vars=None, const=None, depth=None, algebra=None, lower_limit=None, count=None,
                             type=None, upper_limit=None, range=None, terms=None, base_2_lower=None, base_2_upper=None, base_8_lower=None,
                             base_8_upper=None, base_10_lower=None, base_10_upper=None, base_16_lower=None, base_16_upper=None):
    
        if function == 'boolean_algebra': boolean_algebra_config(n=n, vars=vars, const=const)
        elif function == 'prefix_infix_postfix': prefix_infix_postfix_config(depth=depth, algebra=algebra)
        elif function == 'number_systems': number_systems_config(lower_limit=lower_limit, upper_limit=upper_limit,
                                                                 type=type, range=range, terms=terms, count=count,
                                                                 base_2_lower=base_2_lower, base_2_upper=base_2_upper,
                                                                 base_8_lower=base_8_lower, base_8_upper=base_8_upper,
                                                                 base_10_lower=base_10_lower, base_10_upper=base_10_upper,
                                                                 base_16_lower=base_16_lower, base_16_upper=base_16_upper)

    def print_questions(self):
        for i in range(len(self.list)):
            print("Question " + str(i + 1) + ":") # + self.list[i].name.replace("_", " ") + "\n")
            # print('─' * len("Question " + str(i + 1) + ": " + str(self.list[i].name)))
            self.list[i].print_output()
            print("\n")

    def save_questions(self, filename):
        with open(filename, 'w') as file:
            for i in range(len(self.list)):
                file.write("Question " + str(i + 1) + ": \n") # + self.list[i].name.replace("_", " ") + "\n")
                # file.write('─' * len("Question " + str(i + 1) + ": " + str(self.list[i].name)) + "\n")
                file.write("\n".join(self.list[i].output) + "\n\n")
