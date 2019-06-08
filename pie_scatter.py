import os
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import plot, iplot
from statistics import mean, stdev
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
import plotly.tools as tls

def draw_k_nearest(polarity=None,subjectivity=None,names_dem=None,names_rep=None,k_neighbors = 3):
    '''
    This function generates an image showing the results of a KNN on an input scatterplot
    :param polarity: dictionary containing the average polarity values of each person
    :param subjectivity: dictionary containing average subjectivity of each person
    :param names_dem: list of names of all democrats in dataset
    :params names_rep: list of names of all republicans in dataset
    :param k_neighbors: K value for KNN calculation
    :return: None, image shown on screen
    '''
    assert isinstance(polarity, dict)
    assert isinstance(subjectivity, dict)
    assert isinstance(names_dem, list)
    assert isinstance(names_rep, list)
    assert all(isinstance(i, str) for i in names_dem)
    assert all(isinstance(i, str) for i in names_rep)
    assert isinstance(k_neighbors, int)
    assert k_neighbors > 0

    cmap_back = ListedColormap(['#00AAFF', '#FFAAAA'])
    cmap_scatter_dem = ListedColormap(['b'])
    cmap_scatter_rep = ListedColormap(['#FF0000'])

    X = []
    y = []
    x_dem = []
    x_rep = []
    for name in names_dem:
        X.append([polarity[name],subjectivity[name]])
        x_dem.append([polarity[name],subjectivity[name]])
        y.append(0)
    for name in names_rep:
        X.append([polarity[name],subjectivity[name]])
        x_rep.append([polarity[name],subjectivity[name]])
        y.append(1)
    X = np.array(X)
    x_dem = np.array(x_dem)
    x_rep = np.array(x_rep)
    y = np.array(y)
    h = .001

    clf = neighbors.KNeighborsClassifier(k_neighbors, weights='distance')
    clf.fit(X, y)

    x_min, x_max = X[:, 0].min() - 0.05, X[:, 0].max() + 0.05
    y_min, y_max = X[:, 1].min() - 0.05, X[:, 1].max() + 0.05
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap = cmap_back)

    plt.scatter(x_dem[:, 0], x_dem[:, 1], cmap = cmap_scatter_dem,marker = 'o',edgecolors = 'black',linewidths = 1,label = 'Democrats')
    plt.scatter(x_rep[:, 0], x_rep[:, 1], cmap = cmap_scatter_rep,marker = '^',edgecolors = 'black',linewidths = 1,label = 'Republicans')

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title('Democrats vs Republicans')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.legend()
    plt.show()


def draw_statistics(mean=None,error=None,title = None,online = False):
    '''
    This function plots the average polarity of republicans and democrats
    :param mean: average polarity values
    :param error: variance araound the mean values
    :return: None
    '''

    colors = ['rgb(0,0,200)','rgb(200,0,0)']
    x = ['Democrats','Republicans']
    y = mean
    trace0 = go.Scatter(x = x[:1], y = y[:1], error_y = dict(type = 'data', array = error[:1], visible = True, color = 'rgb(0,0,200)'), mode = 'markers',marker = dict(size = 13, color = 'rgb(0,0,200)'),name = 'Democrats')
    trace1 = go.Scatter(x = x[1:], y = y[1:], error_y = dict(type = 'data', array = error[1:], visible = True, color = 'rgb(200,0,0)'), mode = 'markers',marker = dict(size = 13, color = 'rgb(200,0,0)'),name = 'Republicans')
    layout = dict(paper_bgcolor = 'rgba(0,0,0,0)', title = title, titlefont = dict(size = 25, color = 'rgb(255,255,255)'), legend = dict(bgcolor = 'rgba(0,0,0,0)', font = dict(size = 25, color = 'rgb(255,255,255)')), hovermode = 'closest',xaxis = dict(tickfont = dict(size = 20, color = 'rgb(255,255,255)')), yaxis = dict(range = [0,0.3], tickfont = dict(size = 20, color = 'rgb(255,255,255)')))
    fig = go.Figure(data = [trace0,trace1], layout = layout)
    if online:
        py.plot(fig)
    else:
        plot(fig)

def draw_scatter(data_dem=None,data_rep=None,title = None,online = False):
    '''
    This function generates a scatterplot showing the average subjectivity and polarity values for various politicians, democrats and republicans
    :param data_dem: Dataframe containing Polarity and Subjectivity values for democrats
    :param data_rep: Dataframe containing Polarity and Sibjectivity values for republicans
    :param title: Optional string to show as title
    :param online: Toggle to use Plotly online/offline
    :return: None, plot shown on screen
    '''
    assert isinstance(data_dem, pd.DataFrame)
    assert isinstance(data_rep, pd.DataFrame)
    assert isinstance(online, bool)

    trace0 = go.Scatter(x = data_dem['Polarity'], y = data_dem['Subjectivity'], mode = 'markers', text = data_dem['Labels'], marker = dict(size = 18, color = 'rgb(0,0,255)'),name = 'Democrats',hoverinfo = 'text')
    trace1 = go.Scatter(x = data_rep['Polarity'], y = data_rep['Subjectivity'], mode = 'markers', text = data_rep['Labels'], marker = dict(size = 18, color = 'rgb(255,0,0)',symbol = 5),name = 'Republicans',hoverinfo = 'text')
    layout = dict(title = title, hovermode = 'closest', xaxis = dict(tickfont = dict(size = 20), title = 'Polarity', ticklen = 5, zeroline = False, gridwidth = 2),yaxis = dict(tickfont = dict(size = 20), title = 'Subjectivity', ticklen = 5, zeroline = False, gridwidth = 2),showlegend = True)
    fig = go.Figure(data = [trace0,trace1], layout = layout)
    if online:
        py.plot(fig)
    else:
        plot(fig)

def draw_pie(positive_neutral_negative=None,title = None,online = False):
    '''
    This function generates pie charts depicting percentage of positive, negative and neutral tweets by a person.
    :param positive_neutral_negative: list with number of pos, neg and neutral tweets for each user
    :param title: Optional string to show as title
    :param online: Toggle to use Plotly online/offline
    :return: None, plot shown on screen
    '''
    assert isinstance(positive_neutral_negative, list)
    assert isinstance(online, bool)

    labels = ['Positive','Neutral','Negative']
    colors = ['rgb(0,191,255)','rgb(220,220,220)','red']
    trace = go.Pie(title = title, titlefont = dict(size = 30,color = 'rgb(255,255,255)'), labels = labels, values = positive_neutral_negative, hoverinfo = 'value', textinfo = 'label+percent', textfont = dict(size = 25), marker = dict(colors = colors, line = dict(color='#000000', width=1)))
    layout = dict(legend = dict(itemsizing = 'trace', bgcolor = 'rgba(0,0,0,0)', font = dict(size = 25, color = 'rgb(0,0,0)')), paper_bgcolor = 'rgba(0,0,0,0)')
    fig = go.Figure(data = [trace],layout = layout)
    if online:
        py.plot(fig)
    else:
        plot(fig)

name_to_party = dict()
with open('all_handles.txt','r') as f:
	names = f.read().splitlines()
with open('real_names.txt') as f:
	real_name = {x:y for x,y in [x.split(',') for x in f.read().splitlines()]}
for i,name in enumerate(names):
	name_to_party[name] = 'dem' if i < 15 else 'rep'
names_dem = [name for name in names if name_to_party[name] == 'dem']
names_rep = [name for name in names if name_to_party[name] == 'rep']
real_names_dem = [real_name[name] for name in names_dem]
real_names_rep = [real_name[name] for name in names_rep]	

name_to_polarity_average = dict()
name_to_subjectivity_average = dict()
dict_for_pie_chart = dict()
for name in names:
	df = pd.read_csv('data/{}_tweets.csv'.format(name))
	name_to_polarity_average[name] = sum(df['Polarity']) / len(df['Polarity'])
	name_to_subjectivity_average[name] = sum(df['Subjectivity']) / len(df['Subjectivity'])
	positive_neutral_negative = [0,0,0]
	for i in df['Polarity']:
		if i >= 0.1:
			positive_neutral_negative[0] += 1
		elif i <= -0.1:
			positive_neutral_negative[2] += 1
		else:
			positive_neutral_negative[1] += 1
	dict_for_pie_chart[name] = positive_neutral_negative

party_to_polarity_average = dict()
party_to_subjectivity_average = dict()
for party in {'dem','rep'}:
	p = [name_to_polarity_average[name] for name in names if name_to_party[name] == party]
	s = [name_to_subjectivity_average[name] for name in names if name_to_party[name] == party]
	party_to_polarity_average[party] = sum(p) / len(p)
	party_to_subjectivity_average[party] = sum(s) / len(s)

data_dem = pd.DataFrame({'Polarity':[name_to_polarity_average[name] for name in names_dem],'Subjectivity':[name_to_subjectivity_average[name] for name in names_dem],'Labels':['{}:    Polarity = {}, Subjectivity = {}'.format(real_name[name],round(name_to_polarity_average[name],3),round(name_to_subjectivity_average[name],3)) for name in names_dem]})
data_rep = pd.DataFrame({'Polarity':[name_to_polarity_average[name] for name in names_rep],'Subjectivity':[name_to_subjectivity_average[name] for name in names_rep],'Labels':['{}:    Polarity = {}, Subjectivity = {}'.format(real_name[name],round(name_to_polarity_average[name],3),round(name_to_subjectivity_average[name],3)) for name in names_rep]})

polarity_dem = [name_to_polarity_average[name] for name in names_dem]
subjectivity_dem = [name_to_subjectivity_average[name] for name in names_dem]
polarity_rep = [name_to_polarity_average[name] for name in names_rep]
subjectivity_rep = [name_to_subjectivity_average[name] for name in names_rep]

mean_polarity = [mean(polarity_dem),mean(polarity_rep)]
stdev_polarity = [stdev(polarity_dem),stdev(polarity_rep)]
mean_subjectivity = [mean(subjectivity_dem),mean(subjectivity_rep)]
stdev_subjectivity = [stdev(subjectivity_dem),stdev(subjectivity_rep)]


if __name__ == '__main__':	
	# tls.set_credentials_file(username = 'pocketchange',api_key = '1fH8OYp241zbSbIivkAj')
	
	# draw_k_nearest(name_to_polarity_average,name_to_subjectivity_average,names_dem,names_rep,k_neighbors = 10)
	
	# draw_statistics(mean_polarity,stdev_polarity,title = 'Polarity Average')
	# draw_statistics(mean_subjectivity,stdev_subjectivity,title = 'Subjectivity')

	draw_scatter(data_dem,data_rep,title = 'Subjectivity and Polarity')
	
	# account = ['HillaryClinton','SenSanders','BarackObama','realDonaldTrump','tedcruz','JebBush','KamalaHarris','SenWarren']
	# for x in range(7,8):
	# 	draw_pie(dict_for_pie_chart[account[x]],title = real_name[account[x]])
	
