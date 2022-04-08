import json

from bson import json_util
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import pymongo  # package for working with MongoDB
import ast
import json
import jwt

app = Flask(__name__)
api = Api(app)


class create_dict(dict):

    # __init__ function
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value


# Create endpoint: USERS
class Users(Resource):
    # methods go here
    def get(self):
        # LOGIN VALIDATION API:
        # Connect to MongoDB
        user = pymongo.MongoClient("mongodb://localhost:27017/")
        db = user["usersdb"]
        users = db["users"]

        mydict = create_dict()
        for user in users.find():
            mydict.add("id: " + str(user['_id']), (
                {"username": user['username'], "password": user['password'],
                 "preference_genre": user['preference_genre'],
                 "movies": user['movies']}))
        # stud_json = json.dumps(mydict, indent=2, sort_keys=True)

        return {'data': mydict}, 200  # return data and 200 OK code

    def post(self):
        # REGISTRATION VALIDATION API:
        # http://127.0.0.1:5000/users?username=Yochanan2&password=password
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('username', required=True)  # add args
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()  # parse arguments to dictionary

        # create new dataframe containing new values
        new_data = {
            'username': args['username'],
            'email': args['email'],
            'password': args['password'],
            'movies': [],
            'expoPushToken': '',
        }

        # Check if username is already used:
        user = pymongo.MongoClient("mongodb://localhost:27017/")
        db = user["usersdb"]
        users = db["users"]

        for user in users.find():
            if args['email'] == user['email']:
                return {'message': "A user with the given email already exists."}, 401

        users.insert_many([new_data])

        return 200  # return data with 200 OK

    pass


# Create endpoint: Movies
class Movies(Resource):
    # methods go here
    pass


# Create endpoint: Movies
class ExpoPushToken(Resource):
    # methods go here
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('userId', required=True)
        parser.add_argument('expoPushToken', required=True)

        args = parser.parse_args()  # parse arguments to dictionary

        # Check if user exists:
        user = pymongo.MongoClient("mongodb://localhost:27017/")
        db = user["usersdb"]
        users = db["users"]

        for user in users.find():
            if args['userId'] == user['userId']:
                filter = {'userId': args['userId']}
                newvalues = {"$set": {'expoPushToken': args['expoPushToken']}}
                users.update_one(filter, newvalues)
                return 200

        return {'message': "Invalid user."}, 400

    pass


# Create endpoint: Events
class Events(Resource):
    def get(self):
        # GET EVENTS API:
        # Connect to MongoDB
        event = pymongo.MongoClient("mongodb://localhost:27017/")
        db = event["eventsdb"]
        events = db["events"]

        events_list = {}

        for event in events.find():
            mydict = create_dict()
            mydict.add("id", str(event['_id']))
            mydict.add("title", event['title'])
            mydict.add("images", event['images'])
            mydict.add("time", event['time'])
            mydict.add("categoryId", event['categoryId'])
            mydict.add("userId", event['userId'])
            mydict.add("location", event['location'])

            events_list.update(mydict)

        return json.dumps(events_list), 200  # return data and 200 OK code

    pass


api.add_resource(Users, '/users')  # '/users' is our entry point for Users
api.add_resource(Movies, '/movies')  # and '/movies' is our entry point for Movies
api.add_resource(Events, '/events')  # and '/movies' is our entry point for Movies

if __name__ == '__main__':
    app.run(

    )  # run our Flask app
