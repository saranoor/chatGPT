import openai
API_KEY = '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' # Add your API key here
openai.api_key = API_KEY
model = 'davinci'
def get_questions(context):
    try:
        response = openai.Completion.create(
            prompt=f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.",
            model='text-davinci-001',
            max_tokens=2000,
            temperature=0
        )
        return response['choices'][0]['text']
    except:
        return "hey"
import csv
file = open('Promotion_Policy.txt')
doc=file.read()
doc=doc.strip()
doc=doc.replace(r"\s*","")
doc=" ".join(doc.split())
print(doc)
print(get_questions(doc))
