
import tweepy
from textblob import TextBlob
import pandas as pd
import re

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'RT[\s]+', '', tweet)
    return tweet

def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

query = "stock market"
tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(100)

data = []
for tweet in tweets:
    cleaned_tweet = clean_tweet(tweet.full_text)
    sentiment = analyze_sentiment(cleaned_tweet)
    data.append([cleaned_tweet, sentiment])

df = pd.DataFrame(data, columns=["Tweet", "Sentiment"])
df.to_csv("tweets_sentiment.csv", index=False)
