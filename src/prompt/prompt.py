import json
import backoff
import openai

from .key import KEY

class ChatGPT:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.initialize()

    def initialize(self):
        openai.api_key = KEY

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def prompt(self, question, type):
        if type == 'boolean_algebra':
            assistance = "You are solving a boolean algebra question."
            example = ""
        elif type == 'prefix_infix_postfix':
            assistance = "You are solving a prefix infix postfix question."
            example = ""
        elif type == 'number_systems':
            assistance = "You are solving a number systems question."
            example = ""
        elif type == 'graph_theory':
            assistance = "You are solving a graph theory question."
            example = ""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": '''You are a question answering bot that returns answers in json format. Please provide the answer to your question in the format of a json message, with the answer key labeled 'answer' and the value containing only the requested information. The answer should be as short as possible, and if the answer is numeric, it should be returned as a number. For example: Question: What is the sum of 5 and 6? Answer: {"answer": "11"} Question: What is the color of the sky? Answer: {"answer": "Cannot"} Question: What is it called when water droplets fall out of clouds? Answer: {"answer": "Rain"}'''},
                {"role": "system", "content": assistance},
                {"role": "user", "content": question}
                # {"role": "assistant", "content": example}
            ]
        )
        return response.choices[0].message.content
    
    def run(self, QuestionList):
        self.question_list_count = QuestionList.question_list_count
        self.results = {'list': self.question_list_count}
        questions = QuestionList.get_questions()
        for i, q in enumerate(questions):
            question_type = q.name
            gpt_prompt = '\n'.join(q.question)
            answer = self.prompt(gpt_prompt, question_type)
            self.results[f"{i+1}"] = answer
        return self.results
    
    def print_results(self):
        for key, value in self.results.items():
            print(f"{key}: {value}\n") 

    def results_to_txt(self):
        filename = f'data/results_{self.question_list_count}.txt'
        with open(filename, 'w') as f:
            for key, value in self.results.items():
                f.write(f"{key}: {value}\n")
