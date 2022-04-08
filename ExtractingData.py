import pymongo  # package for working with MongoDB

user = pymongo.MongoClient("mongodb://localhost:27017/")
db = user["usersdb"]
#db.drop_collection("users")
users = db["users"]

movie = pymongo.MongoClient("mongodb://localhost:27017/")
db2 = movie["moviesdb"]
#db2.drop_collection("movies")
movies = db2["movies"]

event = pymongo.MongoClient("mongodb://localhost:27017/")
db3 = event['eventsdb']
#db3.drop_collection("events")
events = db3["events"]

# CHECKING
for user in users.find():
    print(user)

print("\n")

#for movie in movies.find():
 #   print(movie)
  #  break

print("\n")

for event in events.find():
    print(event)