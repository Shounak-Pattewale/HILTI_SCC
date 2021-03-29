from flask import Blueprint, render_template, redirect, abort
from flask import request, jsonify, make_response, url_for
from datetime import datetime
from flask import session
from flask import flash
import bcrypt
from flask import g
import os
import smtplib

site = Blueprint("site", __name__, template_folder='../templates', static_folder='static',static_url_path='static')

# Custom imports
from app import *
# from app import df

from .models import *
tool = Tools()


@site.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    return (resp, 200)

@site.route("/")
def index():
    tool.data()
    return render_template("base_template.html")

@site.route("/dashboard")
def dashboard():
    # dataset = pandas.read_csv("../site_data/dummy_data.csv")
    # print(dataset.head(10))
    return render_template("dashboard.html")