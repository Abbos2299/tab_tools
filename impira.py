from docquery import document, pipeline
p = pipeline('document-question-answering')
doc = document.load_document("https://templates.invoicehome.com/invoice-template-us-neat-750px.png")
for q in ["What is the invoice number?", "What is the invoice total?"]:
    print(q, p(question=q, **doc.context))
