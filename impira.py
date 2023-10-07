from docquery import document, pipeline
p = pipeline('document-question-answering')
doc = document.load_document("8B49232.pdf")
for q in ["What is the load number?",
          "What is broker Email?",
          "What is Pick up location?",
          "What is Pick up date?",
          "What is the Delivery location?",
          "What is Delivery date?",
          "What is the Total amount?"]:
    result = p(question=q, **doc.context)
    answer = result[0]['answer'] if result else 'No answer found'
    print(answer)


