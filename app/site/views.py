# Generic imports from Flask
from flask import Blueprint, render_template, redirect, abort, session
from flask import request, jsonify, make_response, url_for, flash

# For sending files
from flask import send_from_directory, send_file, safe_join, abort

# imports for sending alert message
import smtplib
from email.message import EmailMessage
from twilio.rest import Client

# useful libraries
from flask_socketio import send
from datetime import datetime
from time import time
import bcrypt
import random
import json
import pickle
import pandas as pd


# custom imports
from .models import *
from app import *

site = Blueprint("site", __name__, template_folder='../templates',
                 static_folder='static', static_url_path='static')

model = pickle.load(
    open('/mnt/d/Taha/HILTI_SCC/app/site_data/trained.pkl', 'rb'))
# model = pickle.load(open('/mnt/d/Shounak/My Projects/HILTI_SCC/app/site_data/trained.pkl', 'rb'))

tool = Tools()

site_docs = app.config["SITE_DOCS"]

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


def sendMessage(receipent):
    try:
        account_sid = 'ACc320869579518126eca9bff99e30433a'
        auth_token = '9169a92a56be0b88d0a5b4a0c8fae845'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        body="Your HILTI tool with id #HT4587 may require maintenance. You are suggested to take necessary actions to prevent your tools from further damage. View tool stats on the link given below. -Team H",
        from_='+13312530016',
        to=receipent
        )

        print(message.sid)
    except:
        print("Error while sending message. Try again!")


def sendEmail(username):
    # For Email Module
    try:
        print("Sending email..!!")
        email_address = 'lustblood03@gmail.com'
        email_password = 'Bloodlust1703'
        msg = EmailMessage()
        msg['Subject'] = 'HILTI tool failure'
        msg['From'] = email_address
        msg['To'] = username
        msg.set_content('Your HILTI tool with id #HT4587 may require maintenance. You are suggested to take necessary actions to prevent your tools from further damage. Click on the link given below to visit the Dashboard. -Team HTOT')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except Exception as error:
        print(error)
        return "<h1> We have following error </h1> <p>{}</p>".format(error)


def prediction(x):
    pred = model.predict([x])
    print('Prediction : ', pred[0])

    # if pred[0] == 1:
    #     sendEmail('sarbajitrc@gmail.com')
    #     sendMessage('9823196905')


@socketio.on('message')
def handle_message(resp):
    print('Message: ', resp)
    x = [resp[0], resp[1], resp[2], resp[3]]
    global nowPointer
    nowPointer = resp[4]
    prediction(x)


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
>>>>>>> 88bd33a34822d031cf48333c001d0c580488eb1d
