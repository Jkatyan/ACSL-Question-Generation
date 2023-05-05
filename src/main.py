from generate import QuestionList
from prompt import ChatGPT

def generate_questions():
    # Create question list
    questions = QuestionList()

    # Generate 5 of each type of question and shuffle their order
    questions.generate_questions([
        (5, 'prefix_infix_postfix'),
        (5, 'boolean_algebra'),
        (5, 'number_systems'),
        (5, 'graph_theory')],
        shuffle=True
    )

    # Save questions to a text file
    questions.to_txt()

    # Save questions to a pickle file
    questions.to_pkl()

def main():
    # Create question list
    generate_questions()

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