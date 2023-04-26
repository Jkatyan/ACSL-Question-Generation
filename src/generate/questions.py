import os
import sys
from io import StringIO

from .boolean_algebra import boolean_algebra, boolean_algebra_config
from .expression_trees import prefix_infix_postfix, prefix_infix_postfix_config
from .number_systems import number_systems, number_systems_config
from .graph_theory import graph_theory, graph_theory_config

class Question:
    def __init__(self, function):
        self.name = function
        self.output = []
        functions_map = {
            'boolean_algebra': boolean_algebra,
            'prefix_infix_postfix': prefix_infix_postfix,
            'number_systems': number_systems,
            'graph_theory': graph_theory
        }
        func = functions_map.get(function)
        if func is not None:
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            func()
            sys.stdout = old_stdout
            self.output = mystdout.getvalue().split('\n')
            self.output.pop()

    def print_output(self):
        print('\n'.join(self.output))


class QuestionList:
    def __init__(self):
        self.list = []
        self.clear_images()

    def add_question(self, question):
        self.list.append(question)

    def generate_questions(self, functions):
        for function in functions:
            for _ in range(function[0]):
                self.add_question(Question(function[1]))

    def configure_parameters(self, function, **params):
        functions_map = {
            'boolean_algebra': boolean_algebra_config,
            'prefix_infix_postfix': prefix_infix_postfix_config,
            'number_systems': number_systems_config,
            'graph_theory': graph_theory_config
        }
        
        func = functions_map.get(function)
        if func is not None:
            func(**params)

    def clear_images(self):
        sys.path.append(os.path.abspath('../../../'))
        directory = './data/images'
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)

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
