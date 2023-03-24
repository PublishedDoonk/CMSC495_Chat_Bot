from datetime import datetime
import re
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

import openai

import chat_bot_api

openai.api_key = #enter you own open ai key

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    """the homepage of the website access allowed once you are logged in"""

    if request.method == "POST":
        prompt = request.form['prompt']
        res = {}
        
        res['answer'] = chat_bot_api.generateChatResponse(prompt)
        return jsonify(res), 200
        
    return render_template('index2.html')

           
if __name__== '__main__':
    app.run(debug=True, port=5000)
