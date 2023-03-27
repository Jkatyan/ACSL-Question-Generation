from generate import QuestionList

def main():
    # Create question list
    questions = QuestionList()

    # Configure question parameters
    questions.configure_parameters('boolean_algebra', n=7, vars=3, const=True)
    questions.configure_parameters('prefix_infix_postfix', depth=2, algebra=False)
    questions.configure_parameters('number_systems', type=0, terms=3, count=3,
                                                     lower_limit=9, upper_limit=30, range=10,
                                                     base_2_lower=16, base_2_upper=64,
                                                     base_8_lower=1000, base_8_upper=7777,
                                                     base_10_lower=100, base_10_upper=1000,
                                                     base_16_lower=4096, base_16_upper=65535)

    # Generate questions
    questions.generate_questions([
        (1, 'prefix_infix_postfix'),    # Generate 1 'prefix_infix_postfix' question
        (2, 'boolean_algebra'),         # Generate 2 'boolean_algebra' questions
        (6, 'number_systems')           # Generate 6 'number_systems' questions
    ])

    # Modify question parameters
    questions.configure_parameters('boolean_algebra', n=10)
    questions.configure_parameters('number_systems', type=1)

    # Generate questions with new parameters
    questions.generate_questions([
        (1, 'boolean_algebra'),         # Generate 1 'boolean_algebra' question
        (3, 'number_systems')           # Generate 3 'number_systems' questions
    ])

    # Print questions
    questions.print_questions()

    # Save questions to file
    questions.save_questions('data/output.txt')


if __name__ == '__main__':
	main()