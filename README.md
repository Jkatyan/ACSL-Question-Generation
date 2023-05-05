<div align='center'>
  <a href='https://sanghani.cs.vt.edu/'><img src="https://sanghani.cs.vt.edu/wp-content/themes/FoundationPress/assets/images/logos/sanghani_footer.svg" alt="Logo"width="300"/></a>
</div>
<div align='center'>
  <h2><b>ACSL Elementary Division Exam Generation</b>
</div>

---
<h2>Introduction</h2>

This script is designed to generate exams using <a href='https://www.acsl.org/about'>ACSL</a> Elementary Division problems. Problems are generated from the following four categories:
<ul>
<li><a href='http://datafiles.acsl.org/samples/contest1/1elementary.pdf'>Computer Number Systems</a></li>
<li><a href='http://datafiles.acsl.org/samples/contest2/2elementary.pdf'>Prefix/Infix/Postfix Notation</a></li>
<li><a href='http://datafiles.acsl.org/samples/contest3/3elementary.pdf'>Boolean Algebra</a></li>
<li><a href='http://datafiles.acsl.org/samples/contest4/4elementary.pdf'>Graph Theory</a></li>
</ul>

---

<h2>Usage</h2>

<b id="one">1.</b> To get started, create a `QuestionList` object in `src/main.py` to store your questions:

```py
from generate import QuestionList

# Initialize a QuestionList object
questions = QuestionList()
```

If you've previously created a `QuestionList` you'd like to restore, you can pass in the path to a pickle file:

```py
questions = QuestionList(directory='data/questions_1.pkl')
```

**2.** Next, configure any question generation parameters if necessary. Parameters can be configured using the `set_parameters` method. A full list of available parameters can be found in the <a href="#reference">reference</a> section.

```py
# Set question parameters
questions.set_parameters('boolean_algebra', type=0, n=10, vars=4, unique=2, const=True)
questions.set_parameters('prefix_infix_postfix', type=0, depth=2, algebra=False)
questions.set_parameters('graph_theory', type=0, num_nodes_lower=5, num_nodes_upper=6, generate_images=False,
                                          random_vertices_lower=5, random_vertices_upper=10)
questions.set_parameters('number_systems', type=0, terms=3, count=3,
                                            lower_limit=9, upper_limit=30, range=10,
                                            base_2_lower=16, base_2_upper=64,
                                            base_8_lower=1000, base_8_upper=7777,
                                            base_10_lower=100, base_10_upper=1000,
                                            base_16_lower=4096, base_16_upper=65535)
```

**3.** Generate a set of questions using the `generate_questions` method. To use this method, identify how many of each type of question should be generated. If you'd like to shuffle the order of questions, use `shuffle=True`:

```py
# Generate 25 of each type of question and shuffle their order
questions.generate_questions([
    (25, 'prefix_infix_postfix'),
    (25, 'boolean_algebra'),
    (25, 'number_systems'),
    (25, 'graph_theory')],
    shuffle=True
)
```

If you'd like to add questions with a different configuration, you can choose to configure the parameters and then generate additional questions. Using `shuffle=True` when calling `generate_questions` again will reshuffle the entire question list. The question list can also be manually shuffled using the `shuffle` method:

```py
# Modify question parameters
questions.set_parameters('boolean_algebra', n=10)
questions.set_parameters('number_systems', type=1)

# Generate questions with new parameters
questions.generate_questions([
    (1, 'boolean_algebra'),        
    (3, 'number_systems')]
)

# Shuffle the question list
questions.shuffle()
```

To view the generated questions, use `print_questions` to view the questions in your terminal or `to_txt` to save the questions to a text file. The output will include both the questions and their answers.

```py
# Print questions
questions.print_questions()

# Save questions to a text file
questions.to_txt()
```

You can choose to save this `QuestionList` for future use by using the `to_pkl` method. This will generate a pickle file containing your `QuestionList` object. Refer to <a href="#one">step 1</a> for instructions on how to load this pickle file.

```py
# Save questions to a pickle file
questions.to_pkl()
```

**4.** To analyze ChatGPT's performance on our generated questions, you will need to create a file containing your <a href='https://platform.openai.com/account/api-keys'> OpenAI API key</a>. Navigate to `src/prompt/` and create a file called `key.py`. Within this file, add the following line and replace `sk-...` with your secret key:

```py
# Do not share this with anyone!
KEY = 'sk-...'
```

With `key.py` successfully created, create a `ChatGPT` object in `src/main.py`. Set a specific <a href='https://platform.openai.com/docs/models/overview'>model</a> using the `model` parameter.

```py
from prompt import ChatGPT

# Create a ChatGPT object using model gpt-3.5-turbo
chat_gpt = ChatGPT(model="gpt-3.5-turbo")
```

**5.** Test ChatGPT's performance against your question list by using the `run` method. To view the results, use either the `print_results` or `results_to_txt` method.

```py
# Send ChatGPT your set of questions
chat_gpt.run(questions)

# Print results
chat_gpt.print_results()

# Save results to a text file
chat_gpt.results_to_txt()
```

---

<h2 id="reference">Reference</h2>

**Section coming soon.**

