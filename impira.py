from docquery import document, pipeline



def extract_information(text):
    # Define the questions to ask
    questions = [
        "What is the load number?",
        "What is broker Email?",
        "What is Pick up location?",
        "What is Pick up date?",
        "What is the Delivery location?",
        "What is Delivery date?",
        "What is the Total amount?"
    ]

    # Initialize DocQuery pipeline
    docquery_pipe = pipeline("tableqa")

    # Extract information using DocQuery
    answers = docquery_pipe(text, questions)

    return answers
answers = extract_information(all_text)
print("DocQuery Answers:")
for question, answer in zip(questions, answers):
    print(f"{question}: {answer}")

@app.route('/get_answers', methods=['GET'])
def get_answers():
    user_uid = request.args.get('uid')
    text = request.args.get('text')
    answers = extract_information(text)

    # Create a dictionary to hold the answers
    answer_dict = {questions[i]: answers[i] for i in range(len(questions))}

    # Convert the dictionary to JSON
    response_json = json.dumps(answer_dict)

    # Return the JSON response
    return response_json
