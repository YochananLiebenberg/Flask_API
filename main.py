import ssl
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Give the location of the dataset

path_dataset = "/Users/yochananliebenberg/PycharmProjects/3rdYearProject/IMDBdata_MainData.csv"

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')

data = pd.read_csv(path_dataset)
age_ratings = data['Rated'].unique()

# Used for testing
# data = data.head(100)

# Adding the Title, Genre, Director, Writer, Actors, Type and Country into the Plot
data2 = data.assign(
    Plot=data.Plot.astype(str) + ', ' + data.Title.astype(str) + ', ' + data.Genre.astype(str) + data.Director.astype(
        str) + ', ' + data.Writer.astype(str) + ', ' + data.Actors.astype(str) + ', ' + data.Type.astype(str) + ', ' + data.Country.astype(str))
data2["Title"] = data.Title
data2["Genre"] = data.Genre
data2["Ratings_Value"] = data['Ratings.Value']
finaldata = data2[["Title", "Plot", "Genre", "Ratings_Value"]]  # Required columns - Title and movie plot
finaldata = finaldata.set_index('Title')  # Setting the movie title as index
print(finaldata.Ratings_Value[0])


# Code: Applying natural language processing techniques to pre-process the movie plots:
print("Applying natural language processing techniques to pre-process the movie plots")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

VERB_CODES = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}


def preprocess_sentences(text):
    text = str(text).lower()

    temp_sent = []
    words = nltk.word_tokenize(text)
    tags = nltk.pos_tag(words)
    for i, word in enumerate(words):
        if tags[i][1] in VERB_CODES:
            lemmatized = lemmatizer.lemmatize(word, 'v')
        else:
            lemmatized = lemmatizer.lemmatize(word)
        if lemmatized not in stop_words and lemmatized.isalpha():
            temp_sent.append(lemmatized)

    finalsent = ' '.join(temp_sent)
    finalsent = finalsent.replace("n't", " not")
    finalsent = finalsent.replace("'m", " am")
    finalsent = finalsent.replace("'s", " is")
    finalsent = finalsent.replace("'re", " are")
    finalsent = finalsent.replace("'ll", " will")
    finalsent = finalsent.replace("'ve", " have")
    finalsent = finalsent.replace("'d", " would")
    return finalsent


print("preprocess_sentences")
finaldata["plot_processed"] = finaldata["Plot"].apply(preprocess_sentences)
# Vectorizing pre-processed movie plots using TF-IDF
print("Vectorizing pre-processed movie plots using TF-IDF")
tfidfvec = TfidfVectorizer()
tfidf_movieid = tfidfvec.fit_transform((finaldata["plot_processed"]))

# Finding cosine similarity between vectors
print("Finding cosine similarity between vectors")
cos_sim = cosine_similarity(tfidf_movieid, tfidf_movieid)

# Storing indices of the data
indices = pd.Series(finaldata.index)


def recommendations(title, cosine_sim=cos_sim):
    recommended_movies_title = []

    index = indices[indices == title].index[0]

    similarity_scores = pd.Series(cosine_sim[index]).sort_values(ascending=False)
    top_10_movies = list(similarity_scores.iloc[1:11].index)
    print((list(finaldata.Genre)[index]))
    print((list(finaldata.index)[index]))
    input_genres = (list(finaldata.Genre)[index]).split(", ")
    print(input_genres)

    def movie_rating(id):
        return eval(list(finaldata.Ratings_Value)[id])

    top_10_movies.sort(key=movie_rating, reverse=True)
    for movie in top_10_movies:
        recommended_movies_title.append(list(finaldata.index)[movie])

    return recommended_movies_title


print("recommendations begin")
print(recommendations("Shrek"))


# Doo not use location from device,allow user to select town or city while using app connecting them to relevant database.
