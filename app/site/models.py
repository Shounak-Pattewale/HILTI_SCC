from flask import Flask, session
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt

import pandas as pd

# Custom imports
from app import *
from app import mongo


class Tools:

    def __init__(self):
        self.df = pd.read_csv('./app/site_data/tool_data.csv')
        # print(self.df.shape)

    def data(self):
        data = self.df
        return data

    def getCompanyDetails(self, username):
        resp = list(mongo.db.tool_data.find({'Name of Owner': username}, {
                    '_id': 0, 'City': 1, 'Region': 1, 'latitude': 1, 'longitude': 1}))

        return resp

    def updateCompanyDetails(self, username, latitude, longitude):
        resp = list(mongo.db.tool_data.update({'Name of Owner': username}, {
                    '$set': {'latitude': latitude, 'longitude': longitude}}))

        return resp

    def assignTool(self, tool_id, site, assign_to, date, status):
        resp = list(mongo.db.tool_data.update({'Product ID': tool_id}, {
                    '$set': {'site': site, 'assigned to': assign_to, 'assigned on' : date, 'status': status}}))

        return resp

    def getTools(self, company):
        resp = list(mongo.db.tool_data.find({'Name of Owner' : company}).limit(5))
        return resp

    def updateTool(self, tool_id, status):
        resp = mongo.db.tool_data.update({'Product ID': tool_id}, {
                                         '$set': {'status': status}})

        return resp


class Users:

    def addUser(self, newuser, google):
        if google:
            user = {
                "First name": newuser['First name'],
                "Last name": newuser['Last name'],
                "Email": newuser['Email'],
                "Profile pic": newuser['Profile pic'],
                "Account type": newuser['account_type']
            }
        else:
            user = {
                "Company": newuser['company'],
                "Email": newuser['email'],
                "password": newuser['password'],
                'Account type': newuser['account_type']
            }
        mongo.db.htot_users.insert_one(user)

    def findUser(self, email, password):
        found = mongo.db.htot_users.find_one({"Email": email}, {"_id": 0})
        if found is not None:
            if bcrypt.checkpw(password.encode('utf-8'), found["password"]):
                return found
            else:
                return -1
        else:
            return 0

    def getUser(self, email):
        user = mongo.db.htot_users.find_one({'Email': email})
        return user

    def updateUserData(self, email, edit):
        user = mongo.db.htot_users.update({'Email': email}, {'$set': edit})
        return user
