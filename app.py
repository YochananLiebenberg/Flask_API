from flask import Flask

import pymongo  # package for working with MongoDB

import json

app = Flask(__name__)


class create_dict(dict):
    # __init__ function
    def __init__(self):
        self = dict()
        # Function to add key:value

    def add(self, key, value):
        self[key] = value


@app.route('/')
def hello_world():
    return "Hello, World!"


# Create endpoint: Events
@app.route('/events')
def events():
    # GET EVENTS API:
    # Connect to MongoDB
    event = pymongo.MongoClient("mongodb://100.67.53.133:27017/")
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

        events_list.append(mydict)

    return json.dumps(events_list), 200  # return data and 200 OK code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
