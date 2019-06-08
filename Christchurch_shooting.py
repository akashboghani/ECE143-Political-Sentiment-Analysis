import pandas as pd
import numpy as np
from collections import defaultdict
import csv
import matplotlib.pyplot as plt
#%matplotlib notebook
import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode()
'''
Plotting the average tweets polarity and comparing it with the polraity of tweets during the Christchurch mosque shooting
'''
def Christchurch_shooting(dates=None, politician=None, twitter_handles=None):
    '''
    This function finds average polarity of tweets during a specified time period.
    :param dates: the list of dates to be analysed in YYYY-MM-DD format
    :param politician: the list of names of politicians to be analysed
    :param twitter_handles: the list of file names from the dataset to be analysed
    '''
    assert isinstance(dates, list)
    assert isinstance(politician, list)
    assert all(isinstance(i, str) for i in politician)
    assert isinstance(twitter_handles, list)
    assert all(isinstance(i, str) for i in twitter_handles)

    average_polarity=defaultdict(float)
    event_polarity=defaultdict(float)
    for i in range(len(politician)):
        data = pd.read_csv('data/' + twitter_handles[i],index_col=1) 
        Polarity=data['Polarity']
        avg_p=np.sum(Polarity)/len(Polarity)
        average_polarity[politician[i]]=avg_p
        p=0
        tweets=0
        for d in dates:  
            try:
                p=sum(Polarity[d])
                tweets+=len(Polarity[d])
            except:
                try:
                    p=Polarity[d]
                    tweets+=1
                except:
                    pass
        try:
            avg_p_c=p/tweets
        except:
            avg_p_c=0
        event_polarity[politician[i]]=avg_p_c
    return average_polarity, event_polarity

if __name__ == '__main__':
    twitter_handles=['tedcruz_tweets.csv','BarackObama_tweets.csv','HillaryClinton_tweets.csv','JebBush_tweets.csv','KamalaHarris_tweets.csv','RandPaul_tweets.csv','realDonaldTrump_tweets.csv','SenSanders_tweets.csv','SenWarren_tweets.csv']
    politician=['Ted Cruz','Barack Obama','Hillary Clinton','Jeb Bush','Kamala Harris','Rand Paul', 'Donald Trump','Bernie Sanders','Elizabeth Warren']
    dates=['2019-03-15','2019-03-16','2019-03-17','2019-03-18']
    average_polarity, event_polarity= Christchurch_shooting(dates, politician, twitter_handles)
    # Plotting
    trace_a = go.Bar(x=list(average_polarity.keys()),
    y = list(average_polarity.values()),
                    name='Average Polarity',marker=dict(color='rgb(220,220,220)'))
    colors=['red','rgb(0,191,255)','red','rgb(0,191,255)','red','rgb(0,191,255)','red','red','red']

    trace_b = go.Bar(x=list(event_polarity.keys()),
    y = list(event_polarity.values()),
                    name='Decreased Average Polarity During Event',marker=dict(color=colors))
    layout = go.Layout(
        title=go.layout.Title(
            text='Christchurch Mosque Shooting',
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Average Polarity',
                font=dict(
                    size=18,
                    color='black'
                )
            )
        )
    )
    trace_c=(go.Bar(x=[None], y=[None],
                           marker=dict(color='rgb(0,191,255)'),
                            name='Increased Average Polarity During Event'))
    data3 = go.Data([trace_a,trace_b,trace_c])
    fig = go.Figure(data=data3,layout=layout)
    plotly.offline.iplot(fig, filename='jupyter/Christchurch')
