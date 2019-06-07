import re
import pandas as pd
import numpy as np
from textblob import TextBlob
from time import sleep
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def translate_tweets(df=None):
    '''
    INSERT DOCSTRING HERE
    '''    
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
    INSERT DOCSTRING HERE
    '''
    for entry in range(len(df)):
        if df['Language'][entry] != 'en':
            df = df.drop([entry])
    df.reset_index(inplace=True)
    return df


def remove_mentions(tweet):                                      
    '''
    INSERT DOCSTRING HERE
    '''    
    r = re.findall('@[\w]*', tweet)
    for i in r:                         
        tweet = re.sub(i, '', tweet)
    return tweet


def remove_puncs(df, min_len):
    '''
    INSERT DOCSTRING HERE
    '''
    #remove punctuations
    df['Clean_tweet'] = df['Clean_tweet'].str.replace("[^a-zA-Z#]", " ")
    df['Clean_tweet'] = df['Clean_tweet'].str.replace("https", "")

    #remove short words
    df['Clean_tweet'] = df['Clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>min_len]))
    return


def find_sentiments(Clean_tweet):
    '''
    INSERT DOCSTRING HERE
    '''
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