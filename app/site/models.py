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
        resp = list(mongo.db.tool_data.find({'Name of Owner': username}, {'_id':0, 'City':1, 'Region':1}))

        return resp

class Users:

    def addUser(self,newuser,google):

        if google == 0:
            user = {
                "Company": newuser['company'],
                "Email": newuser['email'],
                "password": newuser['password']
            }
        elif google == 1:
            user = {
                "First name": newuser['First name'],
                "Last name": newuser['Last name'],
                "Email": newuser['Email'],
                "Profile pic" : newuser['Profile pic']
            }

        mongo.db.htot_users.insert_one(user) 

    def findUser(self,email,password):
        
        found = mongo.db.htot_users.find_one({"Email":email},{"_id":0})
      
        if found is not None:
            if bcrypt.checkpw(password.encode('utf-8'), found["password"]):
                return [found["Email"], found["Company"]]
            else:
                return -1
        else:
            return 0
        
    def getUser(self,email):
        user = mongo.db.htot_users.find_one({'Email': email})
        return user

    def updateUser_data(self,email,edit):
        user = mongo.db.htot_users.update({'Email':email},{'$set':edit})
        return user