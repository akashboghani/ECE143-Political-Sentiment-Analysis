import os
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
# import seaborn as sns

# def draw_bar(freq_dict,xlabel,ylabel,title,tilt_ticks = False):
# 	plt.figure()
# 	plt.bar(list(freq_dict.keys()),list(freq_dict.values()),width = 0.5)
# 	if tilt_ticks:
# 		plt.tick_params(axis = 'x',rotation = -45)
# 	plt.xlabel(xlabel)
# 	plt.ylabel(ylabel)
# 	plt.title(title)
# 	plt.show(block = False)

# def draw_scatter(x,y,color,annotation):
# 	plt.scatter(x,y,c = color)
# 	for i, txt in enumerate(annotation):
# 		plt.annotate(txt,(x[i],y[i]))

def draw_scatter(data_dem,data_rep):
	trace0 = go.Scatter(x = data_dem['Polarity'], y = data_dem['Subjectivity'], mode = 'markers', marker = dict(size = 5, color = 'rgb(0,0,100)'),text = data_dem[['Polarity','Subjectivity','Labels']])
	trace1 = go.Scatter(x = data_rep['Polarity'], y = data_rep['Subjectivity'], mode = 'markers', marker = dict(size = 5, color = 'rgb(100,0,0)'),text = data_rep[['Polarity','Subjectivity','Labels']])
	layout = dict(title = 'Polarity and Subjectivity', hovermode = 'closest', xaxis = dict(title = 'Polarity', ticklen = 5, zeroline = False, gridwidth = 2),yaxis = dict(title = 'Subjectivity', ticklen = 5, zeroline = False, gridwidth = 2),showlegend = False)
	fig = go.Figure(data = [trace0,trace1], layout = layout)
	py.iplot(fig)


if __name__ == '__main__':	
	name_to_party = dict()
	with open('twitter_handles.txt','r') as f:
		names = f.read().splitlines()
	with open('real_names.txt') as f:
		real_name = {x:y for x,y in [x.split(',') for x in f.read().splitlines()]}
	for i,name in enumerate(names):
		name_to_party[name] = 'dem' if i < 13 else 'rep'
	names_dem = [name for name in names if name_to_party[name] == 'dem']
	names_rep = [name for name in names if name_to_party[name] == 'rep']
	real_names_dem = [real_name[name] for name in names_dem]
	real_names_rep = [real_name[name] for name in names_rep]	

	name_to_polarity_average = dict()
	name_to_subjectivity_average = dict()
	for name in names:
		df = pd.read_csv('{}_tweets.csv'.format(name))
		name_to_polarity_average[name] = sum(df['Polarity']) / len(df['Polarity'])
		name_to_subjectivity_average[name] = sum(df['Subjectivity']) / len(df['Subjectivity'])

	party_to_polarity_average = dict()
	party_to_subjectivity_average = dict()
	for party in {'dem','rep'}:
		p = [name_to_polarity_average[name] for name in names if name_to_party[name] == party]
		s = [name_to_subjectivity_average[name] for name in names if name_to_party[name] == party]
		party_to_polarity_average[party] = sum(p) / len(p)
		party_to_subjectivity_average[party] = sum(s) / len(s)

	data_dem = pd.DataFrame({'Polarity':[name_to_polarity_average[name] for name in names_dem],'Subjectivity':[name_to_subjectivity_average[name] for name in names_dem],'Labels':real_names_dem})
	data_rep = pd.DataFrame({'Polarity':[name_to_polarity_average[name] for name in names_rep],'Subjectivity':[name_to_subjectivity_average[name] for name in names_rep],'Labels':real_names_rep})
	draw_scatter(data_dem,data_rep)
	# draw_scatter([name_to_polarity_average[name] for name in names_dem],[name_to_subjectivity_average[name] for name in names_dem],'b',real_names_dem)
	# draw_scatter([name_to_polarity_average[name] for name in names_rep],[name_to_subjectivity_average[name] for name in names_rep],'r',real_names_rep)
	# plt.xlabel('Polarity')
	# plt.ylabel('Subjectivity')
	# draw_bar(name_to_polarity_average,'Account','Polarity','Polarity of People',tilt_ticks = True)
	# draw_bar(name_to_subjectivity_average,'Account','Subjectivity','Subjectivity of People',tilt_ticks = True)
	# draw_bar(party_to_polarity_average,'Party','Polarity','Polarity of Party')
	# draw_bar(party_to_subjectivity_average,'Party','Subjectivity','Subjectivity of Party')
	plt.pause(1000)
