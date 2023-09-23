import requests
import os
from flask import Flask,render_template,request

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"
    from_language = request.form["from_language"]
    to_language = request.form["to_language"]
    
    querystring = {
        "api-version": "3.0",
        "to": f"{to_language}",  # Change this to the target language code
        "textType": "plain",
        "profanityAction": "NoAction"
    }

    payload = [{"Text": f"{from_language}"}]  # Use the input text from the form
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": API_KEY,  # Replace with your actual API key
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)
    data = response.json()
    output = data[0]["translations"][0]["text"]
    if to_language == None:
           raise Exception
    return render_template("index.html", output=output, from_language=from_language, to_language=to_language)

@app.errorhandler(Exception)
def errors(e):
	error_message = f"Error: Caught an exceptional error Pls Try again {e}"
	return render_template("index.html",error_message=error_message),500

