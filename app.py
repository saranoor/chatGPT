from flask import Flask, render_template, request
import openai
import webbrowser
import requests

app = Flask(__name__)
API_KEY = '' # Add your API key here
openai.api_key = API_KEY
model = 'davinci:ft-personal-2023-02-15-12-48-41'

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
        with open('/home/saranoor/Data/chatGPT_fine_tuning/chatGPT/response.txt','w', newline='') as r:
            r.write(res)
        htmlstring = res
        with open("code.html", "w") as file:
            file.write(htmlstring)
        generated_code = res

        webbrowser.open("code.html")
        return render_template('index.html', response=res)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
