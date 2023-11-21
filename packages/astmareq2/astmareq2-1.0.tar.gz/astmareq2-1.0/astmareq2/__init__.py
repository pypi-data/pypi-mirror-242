
def text_clustering_for_groupnews():
    s="""from sklearn.datasets import fetch_20newsgroups

categories = ['soc.religion.christian',
              'comp.graphics']
# Load Data
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=42)

# Check number of records in training and testing data
len(twenty_train.data),len(twenty_test.data)
# TF-IDF Feature Generation
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer

# Initialize regex tokenizer
tokenizer = RegexpTokenizer(r'\w+')

# # Vectorize document using TF-IDF
tf_idf_vect = TfidfVectorizer(lowercase=True,
                        stop_words='english',
                        ngram_range = (1,1),
                        tokenizer = tokenizer.tokenize)

# Fit and Transfrom Text Data
X_train_counts = tf_idf_vect.fit_transform(twenty_train.data)

# Check Shape of Count Vector
X_train_counts.shape
# Import KMeans Model
from sklearn.cluster import KMeans

# Create Kmeans object and fit it to the training data
kmeans = KMeans(n_clusters=2).fit(X_train_counts)

# Get the labels using KMeans
pred_labels = kmeans.labels_
from sklearn import metrics
# Compute DBI score
dbi = metrics.davies_bouldin_score(X_train_counts.toarray(), pred_labels)

# Compute Silhoutte Score
ss = metrics.silhouette_score(X_train_counts.toarray(), pred_labels , metric='euclidean')

# Print the DBI and Silhoutte Scores
print("DBI Score: ", dbi, "\nSilhoutte Score: ", ss)

# Import WordCloud and STOPWORDS
from wordcloud import WordCloud
from wordcloud import STOPWORDS
# Import matplotlib
import matplotlib.pyplot as plt


def word_cloud(text,wc_title,wc_file_name='wordcloud.jpeg'):
    # Create stopword list
    stopword_list = set(STOPWORDS)

    # Create WordCloud
    word_cloud = WordCloud(width = 800, height = 500,
                           background_color ='white',
                           stopwords = stopword_list,
                           min_font_size = 14).generate(text)

    # Set wordcloud figure size
    plt.figure(figsize = (8, 6))

    # Set title for word cloud
    plt.title(wc_title)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig(wc_file_name,bbox_inches='tight')
    plt.show()
import pandas as pd
df=pd.DataFrame({"text":twenty_train.data,"labels":pred_labels})
for i in df.labels.unique():
    new_df=df[df.labels==i]
    text="".join(new_df.text.tolist())
    word_cloud(text,twenty_train.target_names[i], twenty_train.target_names[i]+'.jpeg')"""
    return s
def text_classification_for_spam():
    s="""import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv', encoding='latin-1')

data.head()
# drop unnecessary columns and rename cols

data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)

data.columns = ['label', 'text']

data.head()
data.isna().sum()

data.shape
# text preprocessing




# download nltk

import nltk

nltk.download('all')




# create a list text

text = list(data['text'])




# preprocessing loop

import re

from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()




corpus = []




for i in range(len(text)):

    r = re.sub('[^a-zA-Z]', ' ', text[i])

    r = r.lower()

    r = r.split()

    r = [word for word in r if word not in stopwords.words('english')]

    r = [lemmatizer.lemmatize(word) for word in r]

    r = ' '.join(r)

    corpus.append(r)




#assign corpus to data['text']

data['text'] = corpus

data.head()

# Create Feature and Label sets

X = data['text']

y = data['label']




# train test split (66% train - 33% test)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)




print('Training Data :', X_train.shape)

print('Testing Data : ', X_test.shape)

# Train Bag of Words model

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()

X_train_cv = cv.fit_transform(X_train)

X_train_cv.shape
# Training Logistic Regression model

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()

lr.fit(X_train_cv, y_train)




# transform X_test using CV

X_test_cv = cv.transform(X_test)




# generate predictions

predictions = lr.predict(X_test_cv)

predictions

# confusion matrix

import pandas as pd

from sklearn import metrics

df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions), index=['ham','spam'], columns=['ham','spam'])

df"""
    return s
def topic_detection():
    s="""corpus = [ "Rafael Nadal Joins Roger Federer in Missing U.S. Open",
          "Rafael Nadal Is Out of the Australian Open",
          "Biden Announces Virus Measures",
          "Biden's Virus Plans Meet Reality",
          "Where Biden's Virus Plan Stands"]
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from nltk.corpus import stopwords
count_vect = CountVectorizer(stop_words=stopwords.words('english'), lowercase=True)
x_counts = count_vect.fit_transform(corpus)
x_counts.todense()
count_vect.get_feature_names()
tfidf_transformer = TfidfTransformer()
x_tfidf = tfidf_transformer.fit_transform(x_counts)
dimension = 2
lda = LDA(n_components = dimension)
lda_array = lda.fit_transform(x_tfidf)
lda_array


components = [lda.components_[i] for i in range(len(lda.components_))]
features = count_vect.get_feature_names()
important_words = [sorted(features, key = lambda x: components[j][features.index(x)], reverse = True)[:3] for j in range(len(components))]
important_words



"""
    return s
def sentiment_classification():
    s="""# Load and prepare the dataset
import nltk
from nltk.corpus import movie_reviews
import random

documents = [(list(movie_reviews.words(fileid)), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)
# Define the feature extractor

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features
# Train Naive Bayes classifier
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
# Test the classifier
print(nltk.classify.accuracy(classifier, test_set))
# Show the most important features as interpreted by Naive Bayes
classifier.show_most_informative_features(5)
"""
    return s
def web_scraping():
    s="""import requests

# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)
import requests

# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# print request object
print(r.url)

# print status code
print(r.status_code)
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())
import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

# Getting the title tag
print(soup.title)

# Getting the name of the tag
print(soup.title.name)

# Getting the name of parent tag
print(soup.title.parent.name)

# use the child attribute to get
# the name of the child tag
import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('div', class_='entry-content')

lines = s.find_all('p')

for line in lines:
    print(line.text)
"""
    return s
def web_crawling():
    s="""import re
import urllib.request
from collections import deque

class WebCrawler:
    def __init__(self):
        self.queue = deque()
        self.discovered_websites = set()

    def discover(self, root):
        self.queue.append(root)
        self.discovered_websites.add(root)

        while self.queue:
            v = self.queue.popleft()
            raw = self.read_url(v)
            regex = r"https://(\w+\.)?(\w+)"
            pattern = re.compile(regex)
            matches = pattern.finditer(raw)

            for match in matches:
                actual = match.group()
                if actual not in self.discovered_websites:
                    self.discovered_websites.add(actual)
                    print("Website found:", actual)
                    self.queue.append(actual)

    def read_url(self, v):
        raw = ""
        try:
            response = urllib.request.urlopen(v)
            data = response.read()
            raw = data.decode("utf-8")
        except Exception as ex:
            print(ex)
        return raw

def main():
    web_crawler = WebCrawler()
    root = "https://www.google.com"
    web_crawler.discover(root)

if __name__ == "__main__":
    main()"""
    return s
def web_indexing():
    s="""import requests
list_urls = ["https://www.example.com", "https://www.example/test2/"]
for y in list_urls:
    url = 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=yourapikey'
    myobj = '{"siteUrl":"https://www.example.com", "urlList":["'+ str(y) +'"]}'
    headers = {'Content-type': 'application/json; charset=utf-8'}
    x = requests.post(url, data=myobj, headers=headers)
    print(str(y) + ": " + str(x))


API key: 6575e7e571ab4f108ab2de7033704dcc


"""
    return s
def information_visulization():
    s="""from itertools import islice
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt
def load_text(filename):
    my_text = list()
    with open(filename, encoding= "latin-1") as f:
        for line in islice(f, 0, None):
            my_text.append(line)
    my_text = [word_tokenize(sentence) for sentence in my_text]
    flat_list = [item for sublist in my_text for item in sublist]
    return flat_list
thacher = load_text('thacher-2021.txt')
otis = load_text('otis-2021.txt')
mayhew = load_text('mayhew2-2021.txt')
def prepare_text(list_of_words):
  #load stopwords:
  stops = stopwords.words('english')
  #transform all word characters to lower case:
  list_of_words = [word.lower() for word in list_of_words]
  #remove all words containing up to two characters:
  list_of_words = [word for word in list_of_words if len(word)>2]
  #remove stopwords:
  list_of_words = [word for word in list_of_words if word not in stops]
  return list_of_words

thacher = prepare_text(thacher)
otis = prepare_text(otis)
mayhew = prepare_text(mayhew)

# Create DataFrames
thacher_df = pd.DataFrame(thacher, columns=['word'])
otis_df = pd.DataFrame(otis, columns=['word'])
mayhew_df = pd.DataFrame(mayhew, columns=['word'])

# Assuming you want to count the occurrences of each word
thacher_df = thacher_df['word'].value_counts().reset_index()
thacher_df.columns = ['word', 'count']

otis_df = otis_df['word'].value_counts().reset_index()
otis_df.columns = ['word', 'count']

mayhew_df = mayhew_df['word'].value_counts().reset_index()
mayhew_df.columns = ['word', 'count']

thacher_10 =thacher_df.iloc[:10]
otis_10 = otis_df.iloc[:10]
mayhew_10 = mayhew_df.iloc[:10]

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(12, 4))
# horizontal barplot:
ax1.barh(thacher_10["word"], thacher_10["count"],
        color = "#f0027f",
        edgecolor = "#f0027f")
ax2.barh(otis_10["word"], otis_10["count"],
        color = "#386cb0",
        edgecolor = "#386cb0")
ax3.barh(mayhew_10["word"], mayhew_10["count"],
        color = "#fdb462",
        edgecolor = "#fdb462")
# title:
ax1.set_title("Thacher")
ax2.set_title("Otis")
ax3.set_title("Mayhew")
# iterate over ax1, ax2, ax3 to:
# invert the y axis;
# eliminate grid;
# set fonts and background colors;
# eliminate spines;
for ax in fig.axes:
    ax.invert_yaxis()
    ax.grid(False)
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_facecolor('#2E3031')
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
# fig background color:
fig.patch.set_facecolor('#2E3031')
# layout:
fig.tight_layout()
plt.show()"""
    return s
def informatio_extraction():
    s="""import spacy
# Load the English NLP model
nlp = spacy.load("en_core_web_sm")
# Text data to extract information from
text = ""
Apple Inc. is an American multinational technology company headquartered in Cupertino, California.
It was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
Apple designs, manufactures, and markets consumer electronics, computer software, and online services.
""
# Process the text with spaCy
doc = nlp(text)
# Extract named entities (e.g., organizations, persons, locations)
for entity in doc.ents:
    print(f"Entity: {entity.text}, Label: {entity.label_}")
# Extract specific information
found_keywords = []
for token in doc:
    if token.text.lower() == "founded":
        found_keywords.append(token)
if found_keywords:
# Assuming we want to extract the organization's founding det
ails
    organization = None
    for ent in found_keywords[0].head.children:
        if ent.ent_type_ == "ORG":
            organization = ent.text
    if organization:
        print(f"{organization} was founded by:")
        for child in found_keywords[0].children:
            if child.ent_type_ == "PERSON":
                print(child.text)"""
    return s
def twitter_data_analytics():
    s="""Lab 10 : Twitter Data Analytics
Analyzing Twitter data in Python involves several steps, including data collection, data pre￾processing, and data analysis.
Here's the steps involved on how to perform Twitter data analytics using Python:
1. Set Up Your Twitter Developer Account:
To access Twitter data, you need to create a Twitter Developer account and create a Twitter App to
obtain API keys and tokens.
Visit the Twitter Developer website (https://developer.twitter.com/en/apps) and follow the
instructions to create an app.
2. Install Python Libraries:
You'll need several Python libraries for this project, including tweepy for accessing the Twitter API
and pandas for data manipulation. You can install them using pip:


pip install tweepy pandas


3. Authenticate with the Twitter API:
Use the API keys and tokens obtained from your Twitter Developer account to authenticate with the
Twitter API using the tweepy library.
code:


import tweepy
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


4. Collect Twitter Data:
You can collect Twitter data by searching for specific keywords or hashtags, fetching tweets from
specific users, or using streaming APIs for real-time data collection. Here's an example of searching
for tweets with a specific hashtag:
code:


hashtag = '#Python'
tweets = api.search(q=hashtag, count=100)


5. Preprocess Twitter Data:
Twitter data often needs preprocessing to clean and structure it for analysis. You may want to
remove special characters, URLs, and perform tokenization. Also, you can convert the data into a
pandas DataFrame for easier manipulation.
code:


import pandas as pd
data = pd.DataFrame([tweet.text for tweet in tweets], columns=['Text'])


6. Analyze Twitter Data:
Once you have the data in a DataFrame, you can perform various analyses, such as sentiment
analysis, word frequency analysis, or network analysis (if you have user data).
code:
# Example: Sentiment Analysis using TextBlob



from textblob import TextBlob
data['Sentiment'] = data['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)


7. Visualize the Results:
Use data visualization libraries like Matplotlib or Seaborn to create plots and visualizations to better
understand the Twitter data.
code:


import matplotlib.pyplot as plt
data['Sentiment'].hist(bins=10)
plt.xlabel('Sentiment Polarity')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of Tweets')
plt.show()


8. Interpret and Present the Results:
Interpret the results of your analysis and present your findings in a clear and informative way using
Jupyter notebooks, reports, or other formats.
This is a basic outline of how to perform Twitter data analytics in Python. Depending on your specific
goals, you can explore more advanced techniques and libraries for deeper analysis and insights.
Additionally, consider data privacy and ethical considerations when working with Twitter data and
respect Twitter's terms of service and API usage policies."""
    return s
def Opinion_analysis():
    s="""
pip install nltk
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')
# Create a SentimentIntensityAnalyzer object
sid = SentimentIntensityAnalyzer()
# Sample texts for opinion mining
texts = [
 "I love this product! It's amazing.",
 "The service was terrible. I'm very disappointed.",
 "This movie is neither good nor bad.",
 "I don't have any strong feelings about this issue."
]
# Perform sentiment analysis on each text
for text in texts:
 # Analyze the sentiment of the text
    sentiment_scores = sid.polarity_scores(text)
 # Determine the sentiment label based on the compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
 # Print the text and its sentiment
print(f"Text: '{text}'")
print(f"Sentiment: {sentiment} (Compound Score: {sentiment_scores['compound']})")
print("-" * 30)
"""
    return s
def Classification_facebook_data():
    s="""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv('your_facebook_data.csv')

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])

X_train, X_test, y_train, y_test = train_test_split(X, df['label'], test_size=0.2, random_state=42)

classifier = MultinomialNB()
classifier.fit(X_train, y_train)

predictions = classifier.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:\n', report)"""
    return s
