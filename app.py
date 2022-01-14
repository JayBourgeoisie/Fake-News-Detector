## importarea tuturor variabilelor
import numpy as np
import flask
from flask import Flask, request, render_template
from flask_cors import CORS
import os
##Joblib is optimized to be fast and robust on large data in particular and has specific optimizations for numpy arrays. It is BSD-licensed.
import joblib
#from sklearn.externals import joblib
import pickle
##Python object hierarchy is converted into a byte stream, and “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object)
import os
import newspaper
##Newspaper has seamless language extraction and detection. If no language is specified, Newspaper will attempt to auto detect a language.
from newspaper import Article
##collects several modules for working with URLs
import urllib
##text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries
import nltk
#tokenizer divides a text into a list of sentences
nltk.download('punkt')

#Loading the Flask framework to enable web page processing in a single python file
app = Flask(__name__)
##initialize the Flask-Cors extension with default arguments in order to allow CORS for all domains on all routes
CORS(app)
app=flask.Flask(__name__,template_folder='templates')

with open('model.pkl', 'rb') as handle:
    model = pickle.load(handle)

@app.route('/')
def main():
    return render_template('index.html')
    
#Receiving the input url from the user and using Web Scrapping to extract the news content
@app.route('/predict',methods=['GET','POST'])
def predict():
    url = request.get_data(as_text=True)[5:]
    url = urllib.parse.unquote(url)
    article = Article(str(url))
    article.download()
    article.parse()
    article.nlp()
    news = article.summary
    
    
#Passing the news article to the model and returing whether it is Fake or Real

    pred = model.predict([news])
    return render_template('index.html', prediction_text='The news are "{}"'.format(pred[0]))
##afisarea link-ului care duce catre interfata web din browser
if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)