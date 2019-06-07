import pandas as pd
from collections import defaultdict
import csv
import matplotlib.pyplot as plt
#%matplotlib notebook
"""
Plotting the average tweets of specific politicians which are of key interst, hence we form a list of politicians
"""
def average_tweets(twitter_handles,politician):
    """ 
    takes in an input of the list of politicians, read their csv files and plots a histogram of their average tweets
    """
    average_tweet=defaultdict(float)
    for p in range(len(politician)):
        per_day=defaultdict(int)
        data=pd.read_csv('data/' + twitter_handles[p])
        date=data['Date Created']
        for d in date:
            per_day[d]+=1
        avg=sum(per_day.values())/len(per_day.keys())
        average_tweet[politician[p]]=avg
    return average_tweet
if __name__ == '__main__':
    twitter_handles=['tedcruz_tweets.csv','BarackObama_tweets.csv','HillaryClinton_tweets.csv','JebBush_tweets.csv','KamalaHarris_tweets.csv','RandPaul_tweets.csv','realDonaldTrump_tweets.csv','SenSanders_tweets.csv','SenWarren_tweets.csv']
    politician=['Ted Cruz','Barack Obama','Hillary Clinton','Jeb Bush','Kamala Harris','Rand Paul', 'Donald Trump','Bernie Sanders','Elizabeth Warren']
    average_tweet=average_tweets(twitter_handles,politician)
    key=list(average_tweet.keys())
    plt.bar(key, average_tweet.values(), color='grey')
    plt.xticks(key, rotation='-60')
    plt.ylabel('Average tweets per day')
    plt.tight_layout()
    plt.grid(color='k', linestyle='--', linewidth=0.2)
    plt.show()
    

