import os
import sys
import shutil
import random
import pickle
from io import StringIO

from .boolean_algebra import boolean_algebra, boolean_algebra_config
from .expression_trees import prefix_infix_postfix, prefix_infix_postfix_config
from .number_systems import number_systems, number_systems_config
from .graph_theory import graph_theory, graph_theory_config

QUESTION_LIST_COUNT = 1

class Question:
    def __init__(self, function):
        self.name = function
        self.question = []
        self.answer = []
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
            output = mystdout.getvalue().split('\n')
            output.pop()
            output_iter = iter(output)
            while True:
                try:
                    line = next(output_iter)
                    if line.startswith('Question:'):
                        self.question.append(line)
                        while True:
                            line = next(output_iter)
                            if line.startswith('Answer:'):
                                break
                            self.question.append(line)
                    if line.startswith('Answer:'):
                        self.answer.append(line)
                        while True:
                            line = next(output_iter, None)
                            if line is None:
                                break
                            self.answer.append(line)
                except StopIteration:
                    break
            self.answer.pop(0)
            self.question.pop(0)

    def print_question(self):
        print('\n'.join(self.question))

    def print_answer(self):
        print('\n'.join(self.answer))

    def print_output(self):
        print('\n'.join(self.question))
        print('\n'.join(self.answer))


class QuestionList:
    def __init__(self, directory=None):
        global QUESTION_LIST_COUNT

        if directory != None:
            with open(directory, 'rb') as file:
                QuestionList = pickle.load(file)
            self.__dict__ = QuestionList.__dict__
        else:
            if QUESTION_LIST_COUNT == 1:
                self.clear_data()
            self.question_list_count = QUESTION_LIST_COUNT
            QUESTION_LIST_COUNT += 1

            self.parameter_list = []
            self.parameter_list.append({'name': 'boolean_algebra', 'params': {'type': 0, 'n': 10, 'vars': 4, 'unique': 2, 'const': True}})
            self.parameter_list.append({'name': 'prefix_infix_postfix', 'params': {'type': 0, 'depth': 2, 'algebra': False}})
            self.parameter_list.append({'name': 'graph_theory', 'params': {'type': 0, 'num_nodes_lower': 5, 'num_nodes_upper': 6, 'generate_images': False,
                                        'random_vertices_lower': 5, 'random_vertices_upper': 10, 'question_list_count': self.question_list_count}})
            self.parameter_list.append({'name': 'number_systems', 'params': {'type': 0, 'terms': 3, 'count': 3,
                                        'lower_limit': 9, 'upper_limit': 30, 'range': 10, 'base_2_lower': 16, 'base_2_upper': 64,
                                        'base_8_lower': 1000, 'base_8_upper': 7777, 'base_10_lower': 100, 'base_10_upper': 1000,
                                        'base_16_lower': 4096, 'base_16_upper': 65535}})
            self.list = []

    def get_questions(self):
        return self.list

    def add_question(self, question):
        self.list.append(question)

    def shuffle(self):
        random.shuffle(self.list)

    def generate_questions(self, functions, shuffle=False):
        self.configure_parameters()
        for function in functions:
            for _ in range(function[0]):
                self.add_question(Question(function[1]))
        if shuffle:
            self.shuffle()

    def configure_parameters(self):
        functions_map = {
            'boolean_algebra': boolean_algebra_config,
            'prefix_infix_postfix': prefix_infix_postfix_config,
            'number_systems': number_systems_config,
            'graph_theory': graph_theory_config
        }
        for param_dict in self.parameter_list:
            name = param_dict['name']
            params = param_dict['params']
            func = functions_map.get(name)
            if func is not None:
                func(**params)

    def set_parameters(self, name, **params):
        for item in self.parameter_list:
            if item['name'] == name:
                for key in params:
                    item['params'][key] = params[key]

    def clear_data(self):
        sys.path.append(os.path.abspath('../../../'))
        dir_path = './data/'
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def print_questions(self):
        for i in range(len(self.list)):
            print("Problem " + str(i + 1) + ":")
            self.list[i].print_output()
            print("\n")

    def to_txt(self):
        filename = f'data/questions_{self.question_list_count}.txt'
        with open(filename, 'w') as file:
            for i in range(len(self.list)):
                file.write("Question " + str(i + 1) + ": \n")
                file.write("\n".join(self.list[i].question) + "\n")
                file.write("\n".join(self.list[i].answer) + "\n\n")

    def to_pkl(self):
        filename = f'data/questions_{self.question_list_count}.pkl'
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
