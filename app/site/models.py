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

    def __init__(self):
        self.df = pd.read_csv('telemetry.csv')
        print(self.df.shape)
    
    def data(self):
        self.data = self.df.head(10)

        return self.data