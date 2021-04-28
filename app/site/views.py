from flask import Blueprint, render_template, redirect, abort, session
from flask import request, jsonify, make_response, url_for, flash

# For sending files
from flask import send_from_directory, send_file, safe_join, abort

from datetime import datetime
import bcrypt
from time import time
import random
import json
from flask_socketio import send
import pickle
import pandas as pd

site = Blueprint("site", __name__, template_folder='../templates', static_folder='static',static_url_path='static')

# model = pickle.load(open('/mnt/d/Taha/HILTI_SCC/app/site_data/trained.pkl', 'rb'))
model = pickle.load(open('/mnt/d/Shounak/My Projects/HILTI_SCC/app/site_data/trained.pkl', 'rb'))

# Custom imports
from app import *
# from app import socketio
# from app import df

from .models import *
tool = Tools()

site_docs = app.config["SITE_DOCS"]

def prediction(x):
    pred = model.predict([x])
    print('Prediction : ',pred[0])

@socketio.on('message')
def handle_message(resp):
    print('Message: ', resp)
    x = [resp[0],resp[1],resp[2],resp[3]]
    global nowPointer
    nowPointer = resp[4]
    prediction(x)

@site.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    return (resp, 200)

############# INDEX ROUTE #############

@site.route("/")
def index():
    return render_template("home.html")


@site.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
    

@site.route("/user_profile")
def user_profile():
    return render_template("user_profile.html")

@site.route("/get_report")
def get_report():
    df = tool.data()
    new_df = df.head(nowPointer)
    new_df.to_csv(site_docs+'user_data.csv')

    return send_from_directory(site_docs, filename="user_data.csv", as_attachment = True)

@site.route("/history", methods=["POST","GET"])
def history():
    if request.method == "GET":
        val = "Air temp"
        return render_template("stock_chart.html",val=val)
    else :
        req = request.form
        val = req.get('parameter')
        return render_template("stock_chart.html",val=val)

@site.route("/post_json/<string:val>")
def post_json(val):
    df = tool.data()
    d1 = df['unix'].values.tolist()
    d2 = df[val].values.tolist()

    x = []
    for i in range(len(d1)):
        d = []
        d.append(d1[i])
        d.append(d2[i])
        x.append(d)

    response = make_response(json.dumps(x))
    response.content_type = 'application/json'
    return response  