import ssl
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Give the location of the dataset

path_dataset = "/Users/yochananliebenberg/PycharmProjects/3rdYearProject/TA_restaurants_curated.csv"

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')

df = pd.read_csv(path_dataset)

# Used for testing
# data = data.head(100)

# Create a different dataset for each city
#  'Amsterdam' 'Athens' 'Barcelona' 'Berlin' 'Bratislava' 'Brussels'
#  'Budapest' 'Copenhagen' 'Dublin' 'Edinburgh' 'Geneva' 'Hamburg'
#  'Helsinki' 'Krakow' 'Lisbon' 'Ljubljana' 'London' 'Luxembourg' 'Lyon'
#  'Madrid' 'Milan' 'Munich' 'Oporto' 'Oslo' 'Paris' 'Prague' 'Rome'
#  'Stockholm' 'Vienna' 'Warsaw' 'Zurich'

Amsterdam = df.loc[df['City'] == 'Amsterdam']
Athens = df.loc[df['City'] == 'Athens']
Barcelona = df.loc[df['City'] == 'Barcelona']
Berlin = df.loc[df['City'] == 'Berlin']
Bratislava = df.loc[df['City'] == 'Bratislava']
Brussels = df.loc[df['City'] == 'Brussels']
Budapest = df.loc[df['City'] == 'Budapest']
Copenhagen = df.loc[df['City'] == 'Copenhagen']
Dublin = df.loc[df['City'] == 'Dublin']
Edinburgh = df.loc[df['City'] == 'Edinburgh']
Geneva = df.loc[df['City'] == 'Geneva']
Hamburg = df.loc[df['City'] == 'Hamburg']
Krakow = df.loc[df['City'] == 'Krakow']
Lisbon = df.loc[df['City'] == 'Lisbon']
Ljubljana = df.loc[df['City'] == 'Ljubljana']
London = df.loc[df['City'] == 'London']
Luxembourg = df.loc[df['City'] == 'Luxembourg']
Lyon = df.loc[df['City'] == 'Lyon']
Madrid = df.loc[df['City'] == 'Madrid']
Milan = df.loc[df['City'] == 'Milan']
Munich = df.loc[df['City'] == 'Munich']
Oporto = df.loc[df['City'] == 'Oporto']
Oslo = df.loc[df['City'] == 'Oslo']
Paris = df.loc[df['City'] == 'Paris']
Prague = df.loc[df['City'] == 'Prague']
Rome = df.loc[df['City'] == 'Rome']
Stockholm = df.loc[df['City'] == 'Stockholm']
Vienna = df.loc[df['City'] == 'Vienna']
Warsaw = df.loc[df['City'] == 'Warsaw']
Zurich = df.loc[df['City'] == 'Zurich']

cities = [Amsterdam, Athens, Barcelona, Berlin, Bratislava, Brussels, Budapest, Copenhagen, Dublin, Edinburgh, Geneva, Hamburg, Helsinki, Krakow, Lisbon, Ljubljana, London, Luxembourg, Lyon, Madrid, Milan, Munich, Oporto, Oslo, Paris, Prague, Rome, Stockholm, Vienna, Warsaw, Zurich]
for city in cities:


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
print(recommendations("Anne of Green Gables"))


# Doo not use location from device,allow user to select town or city while using app connecting them to relevant database.
