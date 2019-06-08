import re
import pandas as pd
import numpy as np
from textblob import TextBlob
from time import sleep
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def translate_tweets(df=None):
    '''
    This function translates tweets to english using Google translate API.
    :param df: dataframe containing tweets and attributes
    :return: Boolean True/False indicating whether operation was succesful
    '''    
    assert isinstance(df, pd.DataFrame)

    try:
        for i in range(len(df)):
            if(df.loc[i].Language == 'en'):
                df.at[i, 'Clean_tweet'] = df.loc[i].Tweet
            else:
                continue
                print(i)
                temp = blob(df['Tweet'][i])
                df.at[i, 'Clean_tweet'] = temp.translate(to='en')
                sleep(5)
        return True
    except Exception as e:
        print("Error in translating at index " + str(i) + " : " +str(e))
        return False


def only_english(df=None):
    '''
    This function rejects tweets that are not in English.
    :param df: DataFrame containing tweets and attributes
    :return: df, the updated DataFrame with only English tweets
    '''
    assert isinstance(df, pd.DataFrame)

    for entry in range(len(df)):
        if df['Language'][entry] != 'en':
            df = df.drop([entry])
    df.reset_index(inplace=True)
    return df


def remove_mentions(tweet=None):                                      
    '''
    This function removes all mentions from the tweet.
    :param tweet: The text of the tweet to be scrubbed
    :return: The updated, scrubbed tweet text
    '''    
    assert isinstance(tweet, str)

    r = re.findall('@[\w]*', tweet)
    for i in r:                         
        tweet = re.sub(i, '', tweet)
    return tweet


def remove_puncs(df=None, min_len=None):
    '''
    This function scrubs all the tweets and removes any punctuations and small words.
    :param df: The DataFrame containing all tweets and attributes
    :param min_len: The minimum length of the words to be kept in the tweet
    :return: None, operations are done in place.
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(min_len, int)
    assert min_len > 0

    #remove punctuations
    df['Clean_tweet'] = df['Clean_tweet'].str.replace("[^a-zA-Z#]", " ")
    df['Clean_tweet'] = df['Clean_tweet'].str.replace("https", "")

    #remove short words
    df['Clean_tweet'] = df['Clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>min_len]))
    return


def find_sentiments(Clean_tweet=None):
    '''
    This function calculates the sentiment polarity and subjectivities of a tweet using textblob
    :param Clean_tweet: The cleaned, scrubbed tweet to be analysed
    :return: polarity value [-1, 1] and subjectivity value [0, 1]
    '''
    assert isinstance(Clean_tweet, str)

    analyzer = SentimentIntensityAnalyzer()
    blob = TextBlob(Clean_tweet)
    polarity, subjectivity = blob.sentiment
    if polarity == 0:
        vader_op = analyzer.polarity_scores(Clean_tweet)
        polarity = vader_op['compound']
    return polarity, subjectivity


if __name__ == '__main__':

    #set this variable to false to disable filtering out tweets of other languages
    remove_other_langs = True
    tweet_df = dict()
    with open('twitter_handles.txt') as f:
        polit_list = f.read().rstrip('\n').split('\n')
    for i in polit_list:
        tweet_df[i] = pd.read_csv('data/' + i + '_tweets.csv')
        if 'Clean_tweet' in tweet_df[i].columns:
            continue
        tweet_df[i].insert(3, 'Clean_tweet', None)
        tweet_df[i].insert(4, 'Polarity', None)
        tweet_df[i].insert(5, 'Subjectivity', None)

        print('Cleaning tweets for ' + str(i))

        if(remove_other_langs == True):
            #filter out tweets that are not english
            tweet_df[i] = only_english(tweet_df[i])
        else:
            #translate tweets
            if not translate_tweets(tweet_df[i]):
                print("Error in translating tweets")
        
        #remove mentions
        tweet_df[i]['Clean_tweet'] = np.vectorize(remove_mentions)(tweet_df[i]['Tweet'])

        #remove punctuations and short words
        remove_puncs(tweet_df[i], 3)

        print('Calculating sentiment scores for ' + str(i))

        #find the sentiment scores for all the tweets
        tweet_df[i]['Polarity'], tweet_df[i]['Subjectivity'] = np.vectorize(find_sentiments)(tweet_df[i]['Clean_tweet'])

        print('Updating the csv file for ' + str(i))
        os.remove('data/' + str(i) + '_tweets.csv')
        tweet_df[i].to_csv('data/' + str(i) + '_tweets.csv', index=False, mode='w+', line_terminator='\n')
        print('File updated: ' + str(i) + '_tweets.csv')
