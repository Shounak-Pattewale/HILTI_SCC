from flask import Flask, session
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt

import pandas as pd

# Custom imports
# from app import *
# from app import mongo

class Tools:
    
    def data(self):
        df = pd.read_csv('data.csv')
        print(df.head(10))