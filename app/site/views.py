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
from geopy import Nominatim


# custom imports
from .models import *
from app import *

site = Blueprint("site", __name__, template_folder='../templates',
                 static_folder='static', static_url_path='static')

model = pickle.load(open('app/site_data/trained.pkl', 'rb'))

tool = Tools()
user = Users()

site_docs = app.config["SITE_DOCS"]
email_id = app.config["EMAIL_ID"]
email_pw = app.config["EMAIL_PW"]
account_sid = app.config["ACCOUNT_SID"]
auth_token = app.config["AUTH_TOKEN"]
phone_num = app.config['PHONE_NUM']

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
display: flex;
justify-content: center;
align-items:center;
flex-direction: column;
background-color: #d0d0d0;

}
# first {
padding: 10px;
border-radius: 5px;
background-color: #fff;
}

button {
padding: .5rem 1rem;
border: none;
border-radius: 2px;
}
</style>
</head>
<body>
<div id="first">
<h3>The tool Serial number L6880 needs service. Please contact Hilti Service by clicking the following link</h3>

<button style="background: linear-gradient(to right, #243B55, #141E30) !important; color: white;">
<a href="https://www.hilti.in/content/hilti/A2/IN/en/services/tool-services/tool-service-.html" style="text-decoration: none; color: white;">Click here</a>
</button>
<br>
<br>
<br>
</div>
<p><b>Thank you and Regards</b></p>
<p><b>Team HTOT</b></p>
</body>
</html>

'''
def getMapData(username):
    resp = tool.getCompanyDetails(username)
    new_dict = dict()
    for i in range(len(resp)):
        new_dict[resp[i]['City']] = new_dict.get(resp[i]['City'], 0) + 1

    geolocator = Nominatim(user_agent='App')
    arr = []
    j = 0
    for key, value in new_dict.items():
        location = geolocator.geocode(key)
        arr.append(
            {'Name': key, 
            'Count': value, 
            'latitude': location.latitude, 
            'longitude': location.longitude, 
            'region': resp[j]['Region']
            }
        )
        j += 1
    
    final_ = [{
        'Company': username,
        'Cities': arr,
    }]

    return final_

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
    if session:
        return render_template('dashboard.html')
    return redirect(url_for('site.login'))


@site.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.form

        password = req['password']
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

        u_dict = {
        "company": req['company'],
        "email": req['email'],
        "password": hashed_pw
        }

        if req['password'] == req['cm_password']:
            flash("Signup successful", "success")
            user.addUser(u_dict)
            return render_template('user/login.html')

        flash("Password does not match..!!", 'danger')
        return render_template('user/signup.html', u=u_dict)

    return render_template('user/signup.html', u=[])


@site.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req = request.form
        email = req['email']
        password = req['password']
        status = user.findUser(email, password)
        print("status => ", status)
        if status:
            session.clear()
            session['logged_in'] = True
            session['EMAIL'] = status[0]
            session['COMPANY'] = status[1]
            print("Logged in as : ", session['EMAIL'])
            flash("Login successful", "success")

            print(datetime.now())            
            json_object = json.dumps(getMapData(status[1]))
            
            with open('app/static/map_data.js', 'w') as file:
                file.write("let mapdata = " + json_object)

            
            file.close()

            print(datetime.now())
            
            return redirect(url_for('site.index'))
        elif status == -1:
            flash("Incorrect Email or Password","danger")
        else:
            flash("User does not exist, Please Sign Up!","danger")

    return render_template('user/login.html')


@site.route('/logout')
def logout():
    if session:
        print("CLEARING SESSION FOR : ",session['EMAIL'])
        session.clear()
        return redirect(url_for('site.index'))
    
    print("Please login first")
    return render_template('home.html')


@site.route("/profile")
def user_profile():
    if session:
        user_ = user.getUser(session['EMAIL'])
        return render_template('user/user_profile.html', user=user_)
    return redirect(url_for("site.login"))



def sendMessage(receipent):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        body="Your Hilti tool might require some action. Check mail for more info. -Team HTOT",
        from_='+13312530016',
        to=receipent
        )

        print(message.sid)
    except:
        print("Error while sending message. Try again!")

def sendEmail(username):
    # For Email Module
    try:
        email_address = email_id
        email_password = email_pw
        msg = EmailMessage()
        msg['Subject'] = 'HILTI tool failure'
        msg['From'] = email_address
        msg['To'] = username
        msg.set_content(html, subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
        print("Email Sent successfully!")
    except Exception as error:
        print(error)
        return "<h1> We have following error </h1> <p>{}</p>".format(error)

def prediction(x):
    pred = model.predict([x])
    print('Prediction : ', pred[0])


    if pred[0] == 1:
        sendEmail('tahambohra@gmail.com')
        sendMessage(phone_num)

@socketio.on('message')
def handle_message(resp):
    print('Message: ', resp)
    x = [resp[0], resp[1], resp[2], resp[3]]
    global nowPointer
    nowPointer = resp[4]
    prediction(x)

@site.route("/generate report")
def get_report():
    df = tool.data()
    new_df = df.head(nowPointer)
    new_df.to_csv(site_docs+'user_data.csv')

    return send_from_directory(site_docs, filename="user_data.csv", as_attachment = True)

@site.route("/history", methods=["POST","GET"])
def history():
    if session:
        if request.method == "GET":
            val = "Air temp"
            return render_template("stock_chart.html",val=val)
        else :
            req = request.form
            val = req.get('parameter')
            return render_template("stock_chart.html",val=val)
    return redirect(url_for('site.login'))

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

@site.route('/tool_location')
def map():
    username = session['COMPANY']
    response = getMapData(username)
    return render_template('map.html', mapdb=response)
