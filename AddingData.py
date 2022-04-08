import pymongo  # package for working with MongoDB
import pandas as pd

# CREATING USER DATABASE
user = pymongo.MongoClient("mongodb://localhost:27017/")
db1 = user["usersdb"]
users = db1["users"]

users_list = [
    {"username": "yoch", "email": "yoch@domain.com", "password": "12345",
     "movies": []},
    {"username": "mosh", "email": "mosh@domain.com", "password": "12345", "movies": []},
    {"username": "john", "email": "john@domain.com", "password": "12345", "movies": []},
]
x = users.insert_many(users_list)

# CREATING MOVIE DATABASE
movie = pymongo.MongoClient("mongodb://localhost:27017/")
db2 = movie["moviesdb"]
movies = db2["movies"]
path_dataset = "/Users/yochananliebenberg/PycharmProjects/3rdYearProject/IMDBdata_MainData.csv"
data = pd.read_csv(path_dataset)
age_ratings = data['Rated'].unique()

# Adding the Title, Genre, Director, Writer, Actors, Type and Country into the Plot
data2 = data.assign(
    Plot=data.Plot.astype(str) + ', ' + data.Title.astype(str) + ', ' + data.Genre.astype(str) + data.Director.astype(
        str) + ', ' + data.Writer.astype(str) + ', ' + data.Actors.astype(str) + ', ' + data.Type.astype(
        str) + ', ' + data.Country.astype(str))
data2["Title"] = data.Title
data2["Genre"] = data.Genre
data2["Ratings_Value"] = data['Ratings.Value']
finaldata = data2[["Title", "Plot", "Genre", "Ratings_Value"]]  # Required columns - Title and movie plot
finaldata = finaldata.drop_duplicates(subset='Title')

y = movies.insert_many(finaldata.to_dict('records'))

# CREATING EVENTS DATABASE
event = pymongo.MongoClient("mongodb://localhost:27017/")
db3 = event["eventsdb"]
events = db3["events"]

events_list = [
    {
        'title': "Movie Night",
        'images': [{'fileName': "poster"}],
        'time': 8,
        'categoryId': 1,
        'userId': '624f1d036061b5d560649c06',
        'location': {
            'latitude': 37.78825,
            'longitude': -122.4324,
        },
    },
    {
        'title': "Dinner With Me",
        'images': [{'fileName': "jacket1"}],
        'time': 6,
        'categoryId': 2,
        'userId': '624f1d036061b5d560649c07',
        'location': {
            'latitude': 37.78825,
            'longitude': -122.4324,
        },
    },
]

z = events.insert_many(events_list)

# print list of the _id values of the inserted documents:
# print(x.inserted_ids)
# print(y.inserted_ids)
