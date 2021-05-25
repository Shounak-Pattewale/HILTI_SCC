# Generic imports from Flask
from flask import Blueprint, render_template, redirect, abort, session
from flask import request, jsonify, make_response, url_for, flash

# For sending files
from flask import send_from_directory, send_file, safe_join, abort

# Google oAuth api
from authlib.integrations.flask_client import OAuth

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
import os
from geopy import Nominatim


# custom imports
from .models import *
from app import *

site = Blueprint("site", __name__, template_folder='../templates',
                 static_folder='static', static_url_path='static')

model = pickle.load(open('app/site_data/trained.pkl', 'rb'))

tool = Tools()
User = Users()

site_docs = app.config["SITE_DOCS"]
email_id = app.config["EMAIL_ID"]
email_pw = app.config["EMAIL_PW"]
account_sid = app.config["ACCOUNT_SID"]
auth_token = app.config["AUTH_TOKEN"]
phone_num = app.config['PHONE_NUM']
google_client_id = app.config['GOOGLE_CLIENT_ID']
google_client_secret = app.config['GOOGLE_CLIENT_SECRET']

# oAuth Setup
google = oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

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

# USER DEFINED FUNCTIONS

# Map API


def getMapData(username):
    resp = tool.getCompanyDetails(username)
    print("resp => ", resp[0])
    new_dict = dict()
    for i in range(len(resp)):
        new_dict[resp[i]['City']] = new_dict.get(resp[i]['City'], 0) + 1

    arr = []
    j = 0
    for key, value in new_dict.items():
        arr.append(
            {
                'Name': key,
                'Count': value,
                'region': resp[j]['Region'],
            }
        )
        j += 1

    final_ = [{
        'Company': username,
        'Cities': arr,
    }]

    return final_

# Send Message


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

# Send Email


def sendEmail(username):
    # For Email Module
    try:
        from_mail = email_id
        from_passw = email_pw

        msg = EmailMessage()
        msg['Subject'] = "HILTI Tool Failure"
        msg['From'] = "Hilti Tool Online Tracking"
        msg['To'] = username
        msg.set_content(html, subtype='html')

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_mail, from_passw)
        server.send_message(msg)
        print("Email sent successfully!")
        server.quit()
    except Exception as error:
        print(error)
        return "<h1> We have following error </h1> <p>{}</p>".format(error)

# Prediction


def prediction(x):
    pred = model.predict([x])
    print('Prediction : ', pred[0])
    if pred[0] == 1:
        try:
            if session:
                print("********************MACHINE FAILURE********************")
                sendEmail('tahamustafa053@gmail.com')
                # sendMessage(phone_num)
        except:
            print("Failure predicted, could not send an email..!!!")

# SOCKET IO


@socketio.on('message')
def handle_message(resp):
    print('Message: ', resp)
    x = [resp[0], resp[1], resp[2], resp[3]]
    global nowPointer
    nowPointer = resp[4]
    prediction(x)

# Error Handler


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
    try:
        if session:
            print("Session : ", session)
            print("Loggedin as : ", session['EMAIL'])
            return render_template("home.html")
        return render_template("home.html")
    except:
        return render_template("home.html")


@site.route("/dashboard")
def dashboard():
    if session:
        return render_template('dashboard.html')
    return redirect(url_for('site.login'))


@site.route('/signup', methods=["GET", "POST"])
def signup():
    if session:
        flash("Please logout first", "danger")
        return redirect(url_for('site.index'))
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
            found = User.getUser(req['email'])
            if found is None:
                flash("Signup successful", "success")
                User.addUser(u_dict, 0)
                return render_template('user/login.html')
            flash("User already exists", "danger")
            return render_template('user/signup.html', u=[])

        flash("Password does not match..!!", 'danger')
        return render_template('user/signup.html', u=u_dict)

    return render_template('user/signup.html', u=[])


@site.route('/login', methods=["GET", "POST"])
def login():
    if session:
        flash("Please logout first", "danger")
        return redirect(url_for('site.index'))
    if request.method == "POST":
        req = request.form
        email = req['email']
        password = req['password']
        status = User.findUser(email, password)
        print("status => ", status)
        if status:
            session.clear()
            session['logged_in'] = True
            session['EMAIL'] = status[0]
            session['COMPANY'] = status[1]
            print("Logged in as : ", session['EMAIL'])
            flash("Login successful", "success")

            return redirect(url_for('site.index'))
        elif status == -1:
            flash("Incorrect Email or Password", "danger")
        else:
            flash("User does not exist, Please Sign Up!", "danger")

    return render_template('user/login.html')

# Google oAuth login


@site.route('/google_login')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('site.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# Google oAuth authorize


@site.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session['EMAIL'] = user_info['email']
    session['logged_in'] = True
    session.permanent = True
    found = User.getUser(user_info['email'])
    if found is None:
        newuser = {
            'First name': user_info['given_name'],
            'Last name': user_info['family_name'],
            'Email': user_info['email'],
            'Profile pic': user_info['picture']
        }

        User.addUser(newuser, 1)
        return redirect(url_for('site.user_profile', _user=newuser))

    return redirect(url_for('site.index'))

# Add try/except


@site.route('/logout')
def logout():
    try:
        if session:
            print("CLEARING SESSION FOR : ", session['EMAIL'])
            session.clear()
            return redirect(url_for('site.index'))
    except:
        print("Please login first")
        return render_template('home.html')


@site.route("/profile", methods=['GET', 'POST'])
def user_profile():
    if request.method == "POST":
        if session:
            req = request.form
            edit = {
                'Company': req['Company'],
                'First name': req['First name'],
                'Last name': req['Last name'],
                'Address': req['Address'],
                'City': req['City'],
                'Country': req['Country'],
                'Zip_code': req['Zip_code'],
                'Info': req['Info']
            }
            User.updateUser_data(session['EMAIL'], edit)
            return redirect(url_for('site.user_profile'))
        return redirect(url_for("site.login"))

    if request.method == "GET":
        if session:
            _user = User.getUser(session['EMAIL'])
            return render_template('user/user_profile.html', _user=_user)

    return redirect(url_for("site.login"))


@site.route("/generate report")
def get_report():
    df = tool.data()
    new_df = df.head(nowPointer)
    new_df.to_csv(site_docs+'user_data.csv')

    return send_from_directory(site_docs, filename="user_data.csv", as_attachment=True)


@site.route("/history", methods=["POST", "GET"])
def history():
    if session:
        if request.method == "GET":
            val = "Air temp"
            return render_template("stock_chart.html", val=val)
        else:
            req = request.form
            val = req.get('parameter')
            return render_template("stock_chart.html", val=val)
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
    print(username)
    # response = json.dumps(getMapData(username))
    mapdb = getMapData(username)

    # data = json.dumps(getMapData(username))
    
    # with open('app/static/map.js', 'w') as file:
    #     file.write("let googlemap = " + data)
    
    return render_template('map.html', company=username, mapdb=mapdb)


@site.route('/create_file')
def create_file():
    final_ = []
    for i in range(1, 16):
        company = 'Company ' + str(i)

        resp = tool.getCompanyDetails(company)
        new_dict = dict()
        for i in range(len(resp)):
            new_dict[resp[i]['City']] = new_dict.get(resp[i]['City'], 0) + 1

        geolocator = Nominatim(user_agent='App')
        arr = []
        j = 0
        for key, value in new_dict.items():
            location = geolocator.geocode(key)
            arr.append(
                {
                    'Name': key,
                    'Count': value,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'region': resp[j]['Region']
                }
            )
            j += 1

        final_.append(
            {
                company: arr
            }
        )
        print("Company " + str(i) + " Created")

    data = json.dumps(final_)

    with open('app/static/map_data.js', 'w') as file:
        file.write("let mapdata = " + data)

    return "Completed"


# @site.route('/datafromdb')
# def database():
#     # final_ = []

#     for i in range(2, 16):
#         company = 'Company ' + str(i)

#         geolocator = Nominatim(user_agent='App')
#         location = geolocator.geocode(company)
#         lat, lng = location.latitude, location.longitude

#         tool.updateCompanyDetails(company, lat, lng)


#     return "Completed"
