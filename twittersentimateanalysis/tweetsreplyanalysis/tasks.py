from .models import TwitterData
from django.utils import timezone
from celery import shared_task
import os, errno
from datetime import datetime
from asyncio.log import logger
import re, string, random
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import unicodedata2
import sys
from tkinter import *
import tkinter
import nltk.classify.util
from nltk.sentiment import sentiment_analyzer
from nltk import FreqDist
import numpy as np
from matplotlib import pylab
from textblob.classifiers import NaiveBayesClassifier
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import logging
from tweetsreplyanalysis import twitterconfig
logging.basicConfig( level=logging.DEBUG)
acrp=0
plid,lid=None,None
parsed_tweet={}
tweets=[]
choice=None
import logging

def remove_noise(tweet_tokens, stop_words = ()):
    
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def word_feats(words):
    return dict([(word, True) for word in words])

positive_vocab = [  ]
negative_vocab = [ ]
neutral_vocab = [ ]    
positive_features = []
negative_features = []
neutral_features = []
train_set = None
classifier = None

def trainset():
    logger.debug("apply trainning set")
    # positive_tweets = twitter_samples.strings('positive_tweets.json')
    # negative_tweets = twitter_samples.strings('negative_tweets.json')
    # text = twitter_samples.strings('tweets.20150430-223406.json')
    global positive_vocab,negative_vocab,neutral_vocab
    global positive_features,negative_features,neutral_features
    global train_set
    global classifier
    # positive_tweets = twitter_samples.strings('positive_tweets.json')
    # negative_tweets = twitter_samples.strings('negative_tweets.json')
    # text = twitter_samples.strings('tweets.20150430-223406.json')
    # tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    # all_pos_words = get_all_words(positive_cleaned_tokens_list)

    # freq_dist_pos = FreqDist(all_pos_words)
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    # test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    filename = ""
    def __init__(self,filename):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = twitterconfig.consumer_key
        consumer_secret = twitterconfig. consumer_secret
        access_token = twitterconfig.access_token
        access_token_secret = twitterconfig.access_token_secret
        self.filename = filename
        logger.debug("intialiaze twitterclient instance")
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet),classifier=c1)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets_wtno(self, query,sid,mid=None):
        '''
        Main function to fetch tweets and parse them.
        '''
        global acrp,plid
        if mid==None:
            plid=None
            lid=None
        else:
            lid=int(mid)
        try:
            logger.debug(f"starting query=>{query}")
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            fetched_tweets =self.api.search_tweets(q ="@"+query,since_id=sid,max_id=mid,count=200)
            try:
                i=0
                emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
                f=open(self.filename,"a",encoding="utf-8")
                for status in fetched_tweets:
                    parsed_tweet={}
                    if(status._json['in_reply_to_status_id_str']==sid):
                        try:
                            txt=str(status.text).translate(non_bmp_map)
                            txt=emoji_pattern.sub(r'',status.text)
                            txt=txt.lower()
                            txt=re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\S', '', txt)
                            txt= re.sub(r'#','', txt)
                            txt=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",txt).split())
                            if txt!='' or txt==None:
                                parsed_tweet['text']=txt
                                parsed_tokens = remove_noise(word_tokenize(txt))
                                parsed_tweet['sentiment'] =  classifier.classify(dict([token, True] for token in parsed_tokens))
                                acrp+=1
                                f.write(txt)
                                logger.debug(f"reply text is{txt}")
                                print("reply text is=>",txt)
                                if len(tweets)>0:
                                    if parsed_tweet not in tweets:
                                        tweets.append(parsed_tweet)
                                else:
                                    tweets.append(parsed_tweet)
                        #    print(status.text)
                            #    print("acrp",acrp)
                                    
                            
                            
                        except UnicodeEncodeError:
                            logger.debug("---------------------------------------error here-------------------------------------------------------")
                            logger.debug(status.text)
                            
                    if(lid==None or lid>int(status._json['id'])):
                        lid=int(status._json['id'])
                        
                    i+=1
                    
            
            finally:
                f.close();
            if(lid==None or lid!=int(sid)+1):
                if(plid!=lid):
                    plid=lid
                    self.get_tweets_wtno(query,sid,lid)
                    return
                else:
                    return
 
        except Exception as e:
            print("Error : " + str(e))
        
        return


@shared_task(name="tweetanalysis")
def tweetanalysis():
    objs = TwitterData.get_submitted_url()
    if len(objs) > 0:
        trainset()
        for obj in objs:
            obj.analysis_status = "Processing"
            obj.analysis_updated_at = timezone.now()
            
            url = obj.twitter_url
            url=((url.replace('//','/')).replace('/',' ')).split(' ')
            sid =obj.twitter_id = url[4]
            uname = url[2]
            obj.save()
            filename = "replies_"+str(sid)+".txt"
            api = TwitterClient(filename)
            global acrp
            acrp=0
            # calling function to get tweets
            api.get_tweets_wtno(uname,sid)
            ptweets=[tweet for tweet in tweets if tweet['sentiment']=='Positive']
            ntweets=[tweet for tweet in tweets if tweet['sentiment']=='Negative']
            netweets=[tweet for tweet in tweets if tweet['sentiment']=='Neutral']
            if len(tweets) > 0:
                positive=(len(ptweets)/len(tweets))*100
                negative=(len(ntweets)/len(tweets))*100
                neutral=(len(netweets)/len(tweets))*100
            else:
                positive= negative= neutral = 0.0
            
            obj.twitter_positive_percentage = positive
            obj.twitter_negative_percentage = negative
            obj.twitter_neutral_percentage = neutral
            obj.twitter_replies_texts_classification = tweets
            obj.analysis_status = "Completed"
            obj.analysis_updated_at =  timezone.now()
            obj.save()
            try:
                os.remove(filename)
            except OSError as e: # this would be "except OSError, e:" before Python 2.6
                if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                    raise # re-raise exception if a different error occurred