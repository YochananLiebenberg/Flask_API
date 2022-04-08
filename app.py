import subprocess
import sys

from flask import Flask

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask-restful'])
from flask_restful import Resource, Api, reqparse

import pymongo  # package for working with MongoDB

import json

app = Flask(__name__)
api = Api(app)


class create_dict(dict):
    # __init__ function
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value


# Create endpoint: Events
class Events(Resource):
    def get(self):
        # GET EVENTS API:
        # Connect to MongoDB
        event = pymongo.MongoClient("mongodb://localhost:27017/")
        db = event["eventsdb"]
        events = db["events"]

        events_list = []

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


api.add_resource(Events, '/events')  # and '/movies' is our entry point for Movies

if __name__ == '__main__':
    app.run(

    )  # run our Flask app
