from generate import QuestionList
from prompt import ChatGPT

def generate_questions():
    # Create question list
    questions = QuestionList()

    # Generate 25 of each type of question and shuffle their order
    questions.generate_questions([
        (25, 'prefix_infix_postfix'),
        (25, 'boolean_algebra'),
        (25, 'number_systems'),
        (25, 'graph_theory')],
        shuffle=True
    )

    # Save questions to a text file
    questions.to_txt()

    # Save questions to a pickle file
    questions.to_pkl()

def main():
    # Create question list
    # generate_questions()

    # Load question list
    questions = QuestionList('data/questions_1.pkl')

    # Initialize ChatGPT
    chat_gpt = ChatGPT()

    # Send ChatGPT your set of questions
    chat_gpt.run(questions)

    # Save results to a text file
    chat_gpt.results_to_txt()

if __name__ == '__main__':
	main()