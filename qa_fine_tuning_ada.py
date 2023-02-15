import openai
ft_qa = "ada:ft-personal-2023-02-14-10-54-59"
API_KEY = '' # Add your API key here
openai.api_key = API_KEY
def apply_ft_qa_answer(question, answering_model):
    """
    Apply the fine tuned discriminator to a question
    """
    prompt = f"{question}\nAnswer:"
    result = openai.Completion.create(model=answering_model, prompt=prompt, max_tokens=30, temperature=0, top_p=1, n=1, stop=['.','\n'])
    return result['choices'][0]['text']

print(apply_ft_qa_answer('What is 10Pearls testing process', ft_qa))
print(apply_ft_qa_answer('can you tell me about life', ft_qa))