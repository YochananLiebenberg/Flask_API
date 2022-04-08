import requests
import json


def search_movie(search_keyword):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q": search_keyword}
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "08681649e8msh76832571dd7e29fp1f3602jsn196881d58509"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


def get_movie_plot(title):
    url = "https://imdb8.p.rapidapi.com/title/get-plots"
    querystring = {"tconst": title}
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "08681649e8msh76832571dd7e29fp1f3602jsn196881d58509"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()["plots"][0]['text']


# Adding the Title, Genre, Director, Writer, Actors, Type and Country into the Plot
def get_details(title):
    response = ''

    url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

    querystring = {"tconst": title}

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "08681649e8msh76832571dd7e29fp1f3602jsn196881d58509"
    }

    # dict_keys(['id', 'title', 'certificates', 'ratings', 'genres', 'releaseDate', 'plotOutline', 'plotSummary'])
    request = requests.request("GET", url, headers=headers, params=querystring).json()
    response += str(request['title']) + ' '
    print(request['genres'])
    return response


main_response = search_movie("Pride & Prejudice")
# result = json.loads(json.loads(str(main_response)))
print(main_response.json().keys())
print(main_response.json()["results"][0].keys())
best_result = main_response.json()["results"][0]
best_result_ID = best_result["id"].split('/')
best_result_ID = best_result_ID[2]
print(best_result_ID)
print(get_movie_plot(best_result_ID))

# Adding the Title, Genre, Director, Writer, Actors, Type and Country into the Plot
print(get_details(best_result_ID))

# main_response_plot = get_movie_plot(best_result_ID)
# print(main_response_plot.json().keys())
'''
if main_response:
    if "results" in main_response.body:
        best_match = main_response.body["results"][0]
        movie_id = best_match["id"][7:-1]

        movie_title = best_match["title"]
        movie_plot = str(best_match["plot"])

print(movie_title)
print(movie_plot)
'''
