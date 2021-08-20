# Generic imports from Flask
import socket
from flask import Blueprint, render_template, redirect, abort, session
from flask import request, jsonify, make_response, url_for, flash

# For sending files
from flask import send_from_directory, send_file, safe_join, abort

# Google oAuth api
from authlib.integrations.flask_client import OAuth

# imports for sending alert message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
from .email_template import email_template

# useful libraries
from flask_socketio import send
from datetime import datetime
import time
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
account_sid = app.config["ACCOUNT_SID"]
auth_token = app.config["AUTH_TOKEN"]
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

# USER DEFINED FUNCTIONS
# Map API
def getMapData(username):
    resp = tool.getCompanyDetails(username)
    # print("resp => ", resp[0])
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
        client = Client(app.config["ACCOUNT_SID"], app.config["AUTH_TOKEN"])
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
        from_mail = app.config["EMAIL_ID"]
        from_passw = app.config["EMAIL_PW"]
# 'ds661225@gmail.com' : 'app/templates/email_templates/inventory.html',
            # 'sarbajitrc@gmail.com' : 'app/templates/email_templates/workshop.html'
        emails = {
            'developer8242@gmail.com' : 'app/templates/email_templates/user.html'
        }
        for email, template in emails.items():
            message = MIMEMultipart("alternative")
            message['Subject'] = 'HILTI Tool Failure'
            message['From'] = 'HILTI Tools Online Tracking'
            message['To'] = username
            user_template = open(template, 'r')
            user_template = user_template.read()
            template = MIMEText(user_template, 'html')
            message.attach(template)
            # msg.set_content(html, subtype='html')

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(from_mail, from_passw)
            server.sendmail(from_mail, email, message.as_string())
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
                sendEmail('ds661225@gmail.com')
                response = tool.updateTool("L47333", 'Failure')
                # sendMessage(app.config['PHONE_NUM'])
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


@socketio.on('pickupSchedule')
def pickup_schedule(toolid):
    print('pickup ', toolid)

    socketio.emit('receive pickup notification', toolid)


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
            # print("Session : ", session)
            # print("Loggedin as : ", session['EMAIL'])
            return render_template("home.html")
        return render_template("home.html")
    except:
        return render_template("home.html")


@site.route("/dashboard")
def dashboard():
    if session:
        return render_template('dashboard.html')
    return redirect(url_for('site.login'))


@site.route("/workshop/dashboard")
def workshop_dashboard():
    if session:
        return render_template('workshop/workshop_dashboard.html')
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
            "password": hashed_pw,
            "account_type" : req['account_type']
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
        if status:
            session.clear()
            session['logged_in'] = True
            session['EMAIL'] = status["Email"]
            session['COMPANY'] = status["Company"]
            session['ACCOUNT_TYPE'] = status["account_type"]
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
    if found:
        if found['Company']:
            session['COMPANY'] = found['Company']
        else:
            session['COMPANY'] = 'Company 1'

        return redirect(url_for('site.index'))
    else:
        newuser = {
            'First name': user_info['given_name'],
            'Last name': user_info['family_name'],
            'Email': user_info['email'],
            'Profile pic': user_info['picture'],
            'Account type': 'user'
        }
        User.addUser(newuser, 1)
        session['COMPANY'] = 'Company 1'
        return redirect(url_for('site.user_profile', _user=newuser))
    return redirect(url_for('site.index'))


@site.route('/logout')
def logout():
    try:
        if session:
            session.clear()
            return redirect(url_for('site.index'))
    except:
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
            User.updateUserData(session['EMAIL'], edit)
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
    mapdb = getMapData(username)

    # data = json.dumps(getMapData(username))
    
    # with open('app/static/map.js', 'w') as file:
    #     file.write("let googlemap = " + data)
    
    return render_template('map.html', company=username, mapdb=mapdb)


@site.route('/tool_tracking', methods=['GET'])
def tool_tracking():
    return render_template('timeline.html')


@site.route('/manage_tools')
def manage_tools():
    company = session['COMPANY']
    response = tool.getTools(company)
    return render_template('manage_tool.html', tools=response)


@site.route('/assign_tool', methods=['POST'])
def assign_tool():
    req = request.form
    tool_id = req['tool-id']
    site = req['site']
    assign_to = req['assign-to']
    status = "Assigned"
    date = datetime.now().strftime('%x')

    response = tool.assignTool(tool_id, site, assign_to, date, status)

    return redirect(url_for('site.manage_tools'))


@site.route('/unassign', methods=['POST'])
def unassign():
    tool_id = request.args['toolid']
    response = tool.updateTool(tool_id)
    return redirect(url_for('site.manage_tools'))

@site.route('/schedule_pickup', methods=['POST'])
def schedule_pickup():
    return "Pick up scheduled"
