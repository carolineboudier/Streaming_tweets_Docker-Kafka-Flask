'''L'application Flask récupère les données de la base de données et crée deux diagrammes en barre permettant de compter les unigrammes et les hashtags'''

from flask import Flask, render_template, url_for,jsonify
import plotly
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
import flask_table
from flask_table import Table, Col
import pandas as pd
import numpy as np
import json


app = Flask(__name__)

# connection à la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:secret@db:5432/database"
db = SQLAlchemy(app)

# querys que l'on utilisera pour aller chercher nos deux tables
hashtags_db = db.Table("hashtags_table", db.metadata, autoload=True, autoload_with=db.engine)
unigrams_db= db.Table("unigrams_table", db.metadata, autoload=True, autoload_with=db.engine)

# fonction permettant de créer un graphique
def create_plot(results):
    df = pd.DataFrame(results,columns=["Id", "Hashtag", "Count"])
    df = df.sort_values(by=["Count"],ascending=False)
    df = df.head(10)
    data =[
        go.Bar(
            x= df["Hashtag"],
            y= df["Count"],
            marker_color="brown"
            )
        ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

'''Code de l'application'''
@app.route('/')
def index():
    # pour les hashtags
    results_hash=db.session.query(hashtags_db).all()
    bar_hash = create_plot(results_hash)
    # for unigrams
    results_uni=db.session.query(unigrams_db).all()
    bar_uni = create_plot(results_uni)
    # on retournera un html basé sur le template du folder templates
    return render_template('index.html',bar_hash=bar_hash,bar_uni=bar_uni)
