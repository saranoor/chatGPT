from flask import Flask, render_template, request
import openai
import webbrowser
import requests
import numpy as np
import openai
import pandas as pd
import pickle
import tiktoken

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

from openai.embeddings_utils import get_embedding
# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191
API_KEY = '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' # Add your API key here
openai.api_key = API_KEY
def parse_float_list(string):
    # Remove brackets and split by comma
    values = string.strip('[]').split(',')
    # Convert each value to a float and return as a list
    if len(values) == 1 and values[0] == '':
      return np.nan
    return [float(value) for value in values]

df_test=pd.read_csv('./data_policy/qs_ans_embeddings.csv', converters={'embeddings': parse_float_list})
df_test.drop(['Unnamed: 0'],axis=1, inplace=True)


def load_embeddings(fname: str):
    """
    Read the document embeddings and their keys from a CSV.

    fname is the path to a CSV with exactly these named columns:
        "title", "heading", "0", "1", ... up to the length of the embedding vectors.
    """
    # df=pd.read_excel(fname)
    return {
        (r.title, r.heading): r.embeddings for _, r in df_test.iterrows()
    }
test_doc_embeddings=load_embeddings('.csv')
list(test_doc_embeddings.items())[59:60]
# An example embedding:
example_entry = list(test_doc_embeddings.items())[0]
print(f"{example_entry[0]} : {example_entry[1][:5]}... ({len(example_entry[1])} entries)")


def vector_similarity(x, y):
    """
    Returns the similarity between two vectors.

    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    # print(type(x), type(y))
    # x = np.array(x)
    # y = np.array(y)

    x = np.array(x, dtype="float64")
    y = np.array(y, dtype="float64")
    if np.isnan(x).any():
        return 0.0
    elif np.isnan(y).any():
        return 0.0
    return np.dot(x, y)
def order_document_sections_by_query_similarity (query, contexts):
    """
    query in string format is given, context are basically document embeddings, we have calculated above, first this fn finds embeddings of string
    query then find similary docs
    """
    # query_embedding = get_embedding(query)
    query_embedding=get_embedding(query, engine=embedding_model)
    # document_similarities = sorted([
    #     (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    # ], reverse=True)
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ],reverse=True)
    return document_similarities

MAX_SECTION_LEN = 500
SEPARATOR = "\n* "
ENCODING = "gpt2"  # encoding for text-davinci-003

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

f"Context separator contains {separator_len} tokens"
df_test = df_test.set_index(["title", "heading"])


def construct_prompt(question: str, context_embeddings: dict, df: pd.DataFrame) -> str:
    """
    Fetch relevant
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)

    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []

    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.
        document_section = df.loc[section_index]

        chosen_sections_len += document_section.n_tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break

        chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))

    # Useful diagnostic information
    print(f"Selected {len(chosen_sections)} document sections:")
    print("\n".join(chosen_sections_indexes))

    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""

    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"

COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 300,
    "model": COMPLETIONS_MODEL,
}


def answer_query_with_context(
        query: str,
        df: pd.DataFrame,
        document_embeddings,
        show_prompt: bool = False
) -> str:
    prompt = construct_prompt(
        query,
        document_embeddings,
        df
    )

    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
        prompt=prompt,
        **COMPLETIONS_API_PARAMS
    )

    return response["choices"][0]["text"].strip(" \n")

print(df_test)
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        question = request.form['prompt']
        res=answer_query_with_context(question, df_test, test_doc_embeddings)

        htmlstring = res
        with open("code.html", "w", newline='') as file:
            file.write(htmlstring.replace('end_it', '\n'))

        #webbrowser.open("code.html")
        return render_template('index.html', response=res)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
