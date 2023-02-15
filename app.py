from flask import Flask, render_template, request
import openai
import webbrowser
import requests

app = Flask(__name__)
API_KEY = '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' # Add your API key here
openai.api_key = API_KEY
model = 'ada:ft-personal-2023-02-14-10-54-59'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = openai.Completion.create(
            prompt=prompt,
            model=model, 
            max_tokens=2000
        )
        res = response.choices[0].text
        htmlstring = res
        with open("code.html", "w") as file:
            file.write(htmlstring)
            
        generated_code = res

        webbrowser.open("code.html")
        return render_template('index.html', response=res)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
