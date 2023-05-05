import json
import openai

from .key import KEY

class ChatGPT:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.initialize()

    def initialize(self):
        openai.api_key = KEY

    def prompt(self, question):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": '''I will be sending you a series of questions. For each question, please provide the answer in the format of a json message, with the answer key labeled 'answer' and the value containing only the requested information. The answer should be as short as possible, and if the answer is numeric, it should be returned as a number. Otherwise, it should be returned as a single word. For example: Question: What is the sum of 5 and 6? Answer: {"answer": "11"} Question: What is the color of the sky? Answer: {"answer": "Cannot"} Question: What is it called when water droplets fall out of clouds? Answer: {"answer": "Rain"}'''},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message.content
    
    def run(self, QuestionList):
        self.question_list_count = QuestionList.question_list_count
        self.results = {'list': self.question_list_count}
        questions = QuestionList.get_questions()
        for i, q in enumerate(questions):
            gpt_prompt = '\n'.join(q.question)
            answer = self.prompt(gpt_prompt)
            self.results[f"{i+1}"] = answer
        return self.results
    
    def print_results(self):
        for key, value in self.results.items():
            if isinstance(value, str):
                self.results[key] = json.loads(value)
        print(json.dumps(self.results, indent=4))

    def results_to_txt(self):
        filename = f'data/results_{self.question_list_count}.txt'
        with open(filename, 'w') as f:
            for key, value in self.results.items():
                if isinstance(value, str):
                    self.results[key] = json.loads(value)
            json.dump(self.results, f, indent=4)