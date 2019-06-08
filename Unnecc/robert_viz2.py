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

def draw_k_nearest(polarity,subjectivity,names_dem,names_rep,k_neighbors = 3):
	cmap_back = ListedColormap(['#00AAFF','#FFAAAA'])
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


def draw_statistics(mean,error,title = None,online = False):
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

def draw_scatter(data_dem,data_rep,title = None,online = False):
	trace0 = go.Scatter(x = data_dem['Polarity'], y = data_dem['Subjectivity'], mode = 'markers', text = data_dem['Labels'], marker = dict(size = 18, color = 'rgb(0,0,255)'),name = 'Democrats',hoverinfo = 'text')
	trace1 = go.Scatter(x = data_rep['Polarity'], y = data_rep['Subjectivity'], mode = 'markers', text = data_rep['Labels'], marker = dict(size = 18, color = 'rgb(255,0,0)',symbol = 5),name = 'Republicans',hoverinfo = 'text')
	layout = dict(title = title, hovermode = 'closest', xaxis = dict(tickfont = dict(size = 20), title = 'Polarity', ticklen = 5, zeroline = False, gridwidth = 2),yaxis = dict(tickfont = dict(size = 20), title = 'Subjectivity', ticklen = 5, zeroline = False, gridwidth = 2),showlegend = True)
	fig = go.Figure(data = [trace0,trace1], layout = layout)
	if online:
		py.plot(fig)
	else:
		plot(fig)

def draw_pie(positive_neutral_negative,title = None,online = False):
	labels = ['Positive','Neutral','Negative']
	colors = ['rgb(0,191,255)','rgb(220,220,220)','red']
	trace = go.Pie(title = title, titlefont = dict(size = 30,color = 'rgb(255,255,255)'), labels = labels, values = positive_neutral_negative, hoverinfo = 'value', textinfo = 'label+percent', textfont = dict(size = 25), marker = dict(colors = colors, line = dict(color='#000000', width=1)))
	layout = dict(legend = dict(itemsizing = 'trace', bgcolor = 'rgba(0,0,0,0)', font = dict(size = 25, color = 'rgb(255,255,255)')), paper_bgcolor = 'rgba(0,0,0,0)')
	fig = go.Figure(data = [trace],layout = layout)
	if online:
		py.plot(fig)
	else:
		plot(fig)

def precalc_plots(self):
	self.names = [
				'HillaryClinton',
				'SenBlumenthal',
				'SenSherrodBrown',
				'SenatorCantwell',
				'SenSanders',
				'SenWarren',
				'SenSchumer',
				'KamalaHarris',
				'CoryBooker',
				'BarackObama',
				'AndrewYang',
				'amyklobuchar',
				'maziehirono',
				'SenatorBaldwin',
				'SenBobCasey',
				'RandPaul',
				'tedcruz',
				'SenAlexander',
				'MarshaBlackburn',
				'JohnBoozman',
				'SenatorBurr',
				'RoyBlunt',
				'BillCassidy',
				'SenTomCotton',
				'realDonaldTrump',
				'TomPerez',
				'SenatorTimScott',
				'GOPChairwoman',
				'JebBush',
				'senatemajldr'
	]

	self.name_to_party = {
						'HillaryClinton':	'dem'
						'SenBlumenthal':	'dem'
						'SenSherrodBrown':	'dem'
						'SenatorCantwell':	'dem'
						'SenSanders':		'dem'
						'SenWarren':		'dem'
						'SenSchumer':		'dem'
						'KamalaHarris':		'dem'
						'CoryBooker':		'dem'
						'BarackObama':		'dem'
						'AndrewYang':		'dem'
						'amyklobuchar':		'dem'
						'maziehirono':		'dem'
						'SenatorBaldwin':	'dem'
						'SenBobCasey':		'dem'
						'RandPaul':			'rep'
						'tedcruz':			'rep'
						'SenAlexander':		'rep'
						'MarshaBlackburn':	'rep'
						'JohnBoozman':		'rep'
						'SenatorBurr':		'rep'
						'RoyBlunt':			'rep'
						'BillCassidy':		'rep'
						'SenTomCotton':		'rep'
						'realDonaldTrump':	'rep'
						'TomPerez':			'rep'
						'SenatorTimScott':	'rep'
						'GOPChairwoman':	'rep'
						'JebBush':			'rep'
						'senatemajldr':		'rep'
	}

	# with open('twitter_handles.txt','r') as f:
	# 	names = f.read().splitlines()
	# with open('real_names.txt') as f:

	self.real_name = {
						'HillaryClinton':'Hillary Clinton',
						'SenBlumenthal':'Richard Blumenthal',
						'SenSherrodBrown':'Sherrod Brown',
						'SenatorCantwell':'Maria Cantwell',
						'SenSanders':'Bernie Sanders',
						'SenWarren':'Elizabeth Warren',
						'SenSchumer':'Chuck Schumer',
						'KamalaHarris':'Kamala Harris',
						'CoryBooker':'Cory Booker',
						'BarackObama':'Barack Obama',
						'AndrewYang':'Andrew Yang',
						'amyklobuchar':'Amy Klobuchar',
						'maziehirono':'Mazie Hirono',
						'SenatorBaldwin':'Tammy Baldwin',
						'SenBobCasey':'Bob Casey',
						'RandPaul':'Rand Paul',
						'tedcruz':'Ted Cruz',
						'SenAlexander':'Lamar Alexander',
						'MarshaBlackburn':'Marsha Blackburn',
						'JohnBoozman':'John Boozman',
						'SenatorBurr':'Richard Burr',
						'RoyBlunt':'Roy Blunt',
						'BillCassidy':'Bill Cassidy',
						'SenTomCotton':'Tom Cotton',
						'realDonaldTrump':'Donald Trump',
						'TomPerez':'Tom Perez',
						'SenatorTimScott':'Tim Scott',
						'GOPChairwoman':'Ronna McDaniel',
						'JebBush':'Jeb Bush',
						'senatemajldr':'Mitch McConnell',
	}

	# 	real_name = {x:y for x,y in [x.split(',') for x in f.read().splitlines()]}
	# for i,name in enumerate(names):
		# name_to_party[name] = 'dem' if i < 15 else 'rep'
	self.names_dem = [name for name in self.names if self.name_to_party[name] == 'dem']
	self.names_rep = [name for name in self.names if self.name_to_party[name] == 'rep']

	self.real_names_dem = [self.real_name[name] for name in self.names_dem]
	self.real_names_rep = [self.real_name[name] for name in self.names_rep]	

	self.name_to_polarity_average = dict()
	self.name_to_subjectivity_average = dict()
	self.dict_for_pie_chart = dict()
	for name in self.names:
		df = pd.read_csv('{}_tweets.csv'.format(name))
		self.name_to_polarity_average[name] = sum(df['Polarity']) / len(df['Polarity'])
		self.name_to_subjectivity_average[name] = sum(df['Subjectivity']) / len(df['Subjectivity'])
		self.positive_neutral_negative = [0,0,0]
		for i in df['Polarity']:
			if i >= 0.1:
				self.positive_neutral_negative[0] += 1
			elif i <= -0.1:
				self.positive_neutral_negative[2] += 1
			else:
				self.positive_neutral_negative[1] += 1
		self.dict_for_pie_chart[name] = self.positive_neutral_negative

	self.party_toq_polarity_average = dict()
	self.party_to_subjectivity_average = dict()
	for party in {'dem','rep'}:
		p = [self.name_to_polarity_average[name] for name in self.names if self.name_to_party[name] == party]
		s = [self.name_to_subjectivity_average[name] for name in self.names if self.name_to_party[name] == party]
		self.party_to_polarity_average[party] = sum(p) / len(p)
		self.party_to_subjectivity_average[party] = sum(s) / len(s)

	self.data_dem = pd.DataFrame({'Polarity':[name_to_polarity_average[name] for name in names_dem],'Subjectivity':[name_to_subjectivity_average[name] for name in names_dem],'Labels':['{}:    Polarity = {}, Subjectivity = {}'.format(real_name[name],round(name_to_polarity_average[name],3),round(name_to_subjectivity_average[name],3)) for name in names_dem]})
	self.data_rep = pd.DataFrame({'Polarity':[name_to_polarity_average[name] for name in names_rep],'Subjectivity':[name_to_subjectivity_average[name] for name in names_rep],'Labels':['{}:    Polarity = {}, Subjectivity = {}'.format(real_name[name],round(name_to_polarity_average[name],3),round(name_to_subjectivity_average[name],3)) for name in names_rep]})

	self.polarity_dem = [self.name_to_polarity_average[name] for name in self.names_dem]
	self.subjectivity_dem = [self.name_to_subjectivity_average[name] for name in self.names_dem]
	self.polarity_rep = [self.name_to_polarity_average[name] for name in self.names_rep]
	self.subjectivity_rep = [self.name_to_subjectivity_average[name] for name in self.names_rep]

	self.mean_polarity = [mean(self.polarity_dem),mean(self.polarity_rep)]
	self.stdev_polarity = [stdev(self.polarity_dem),stdev(self.polarity_rep)]
	self.mean_subjectivity = [mean(subjectivity_dem),mean(subjectivity_rep)]
	self.stdev_subjectivity = [stdev(subjectivity_dem),stdev(subjectivity_rep)]


if __name__ == '__main__':	
	# tls.set_credentials_file(username = 'pocketchange',api_key = '1fH8OYp241zbSbIivkAj')
	
	# draw_k_nearest(name_to_polarity_average,name_to_subjectivity_average,names_dem,names_rep,k_neighbors = 10)
	
	# draw_statistics(mean_polarity,stdev_polarity,title = 'Polarity Average')
	# draw_statistics(mean_subjectivity,stdev_subjectivity,title = 'Subjectivity')

	draw_scatter(data_dem,data_rep,title = 'Subjectivity and Polarity')
	
	# account = ['HillaryClinton','SenSanders','BarackObama','realDonaldTrump','tedcruz','JebBush','KamalaHarris','SenWarren']
	# for x in range(7,8):
	# 	draw_pie(dict_for_pie_chart[account[x]],title = real_name[account[x]])
	
