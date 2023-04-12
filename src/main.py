from generate import QuestionList

def main():
    # Create question list
    questions = QuestionList()

    # Configure question parameters
    questions.configure_parameters('boolean_algebra', type=0, n=7, vars=3, const=True)
    questions.configure_parameters('prefix_infix_postfix', type=0, depth=2, algebra=False)
    questions.configure_parameters('graph_theory', type=0, num_nodes_lower=5, num_nodes_upper=6,
                                                   random_vertices_lower=5, random_vertices_upper=10)
    questions.configure_parameters('number_systems', type=0, terms=3, count=3,
                                                     lower_limit=9, upper_limit=30, range=10,
                                                     base_2_lower=16, base_2_upper=64,
                                                     base_8_lower=1000, base_8_upper=7777,
                                                     base_10_lower=100, base_10_upper=1000,
                                                     base_16_lower=4096, base_16_upper=65535)

    # Generate questions
    questions.generate_questions([
        (25, 'prefix_infix_postfix'),    # Generate 25 'prefix_infix_postfix' question
        (25, 'boolean_algebra'),         # Generate 25 'boolean_algebra' questions
        (25, 'number_systems'),          # Generate 25 'number_systems' questions
        (25, 'graph_theory'),            # Generate 25 'number_systems' questions
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