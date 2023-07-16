# -*- coding: utf-8 -*-
from flask import Flask,render_template,jsonify
import json
import requests
from functions import extract_keywords

app = Flask(__name__)


METEO_API_KEY = "393fb1c3aa6234b01b1ce7226c9ca6c5" # Remplacez cette ligne par votre clé OPENWEATHERMAP

if METEO_API_KEY is None:
    # URL de test :
    METEO_API_URL = "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
else: 
    # URL avec clé :
    METEO_API_URL = "https://api.openweathermap.org/data/2.5/forecast?lat=48.883587&lon=2.333779&appid=" + METEO_API_KEY



#PAGE D'ACCEUIL#
@app.route("/")
def hello():
    return "Hello World!"


#PAGE D'ACCEUIL#
@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')

# LA METEO #
@app.route('/api/meteo/')
def meteo():

    response = requests.get(METEO_API_URL) #RECUPERATION DES DONNEES#
    content = json.loads(response.content.decode('utf-8')) #CONVERSION AU FORMAT DICTIONNAIRE PYTHON#


#En cas d'erreur .......#

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500


    data = [] # On initialise une liste vide#
    for prev in content["list"]:
        datetime = prev['dt'] * 1000
        temperature = prev['main']['temp'] - 273.15 # Conversion de Kelvin en °c
        temperature = round(temperature, 2)
        data.append([datetime, temperature]) #LISTE DE LISTES ( voir operation sur les listes)#
 
    return jsonify({
      'status': 'ok', 
      'data': data
    })

    # SEARCH  FOR NEWS #

  

NEWS_API_KEY = "7ad333611b6345129f52fffe363d4bb0"  # Remplacez None par votre clé NEWSAPI, par exemple "4116306b167e49x993017f089862d4xx"

if NEWS_API_KEY is None:
    # URL de test :
    NEWS_API_URL = "https://s3-eu-west-1.amazonaws.com/course.oc-static.com/courses/4525361/top-headlines.json" # exemple de JSON
else:
    # URL avec clé :
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines?sortBy=publishedAt&pageSize=100&language=fr&apiKey=" + NEWS_API_KEY

@app.route('/api/news/')
def get_news():
 
    response = requests.get(NEWS_API_URL)

    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API des articles d\'actualité n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500

    keywords, articles = extract_keywords(content["articles"])#RETOURNE 2 VARIABLES,UNE CONTENANT LES MOTS ISSUS D'UNE LISTE#
    #DE TEXTES PRISES EN PARAMETRES,ET UNE AUTRE CONTENANT LES ARTICLES ASSOCIES A CES MOTS CLES#

    return jsonify({
        'status'   : 'ok',
        'data'     :{
            'keywords' : keywords[:100], # On retourne uniquement les 100 premiers mots
            'articles' : articles
        }
    })






if __name__ == "__main__":
    app.run(debug=True)
