from docquery import document, pipeline

# Load the document from the PDF file
doc = document.load_document("8B49232.pdf")

# Initialize the question-answering pipeline
p = pipeline('document-question-answering')

# List of questions to ask
questions = [
    "What is the load number?",
    "What is broker email?",
    "What is Pick up location?",
    "What is Pick up date?",
    "What is the Delivery location?",
    "What is Delivery date?",
    "What is the Total amount?"
]

# Loop through the questions and print the answers
for q in questions:
    result = p(question=q, **doc.context)
    answer = result[0]['answer'] if result else 'No answer found'
    print(f"Question: {q}")
    print(f"Answer: {answer}\n")
