from flask import Flask, jsonify, request
import time
import os
from flask_cors import CORS
from typing import Dict, List
from groq import Groq
os.environ["GROQ_API_KEY"] = "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"
DEFAULT_MODEL="llama3-70b-8192"
# creating a Flask app
app = Flask(__name__)
CORS(app)
client = Groq()

def assistant(content: str):
    return { "role": "assistant", "content": content }

def user(content: str):
    return { "role": "user", "content": content }

def chat_completion(
    messages: List[Dict],
    model = DEFAULT_MODEL,
    temperature: float = 0.6,
    top_p: float = 0.9,
) -> str:
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
	if(request.method == 'GET'):
		data = "hello world"
		return jsonify({'data': data})

# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/botresponse',methods = ['POST'])
def display():
    print(request)
    query= request.json
    query=str(query)
    answer = chat_completion(messages=[user("Kayla is a Project Manager, contractor at DemoCo, 10 yrs exp. Beneil is a Project Manager experience 20 years and is not a contractor. Miesha is a Diversity and Inclusiveness Researcher with 10 years of work experience and is a permanent employee at DemoCo. Israel has 20 years of experience as a Diversity and Inclusiveness Researcher. He works at SubCo. Subco is a subcontractor to DemoCo."),
    assistant("OK, now ask the questions"),
    user(query+"answer in least words"),])
    print(answer)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify({'response': answer})


# driver function
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=80)
