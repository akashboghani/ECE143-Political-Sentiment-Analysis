import re
import pandas as pd
import numpy as np
from textblob import TextBlob as blob
from time import sleep


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
        print("Error at index " + str(i) + " : " +str(e))
        return False



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

    #remove short words
    df['Clean_tweet'] = df['Clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>min_len]))
    return


if __name__ == '__main__':
    tweet_df = dict()
    with open('twitter_handles.txt') as f:
        polit_list = f.read().rstrip('\n').split('\n')
    for i in polit_list:
        tweet_df[i] = pd.read_csv(i + '_tweets.csv')
        tweet_df[i].insert(3, 'Clean_tweet', None)
        
        #translate tweets
        if not translate_tweets(tweet_df[i]):
            print("Error in translating tweets")
        
        #remove mentions
        tweet_df[i]['Clean_tweet'] = np.vectorize(remove_mentions)(tweet_df[i]['Tweet'])

        #remove punctuations and short words
        remove_puncs(tweet_df[i], 3)
        