import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from plotly.offline import plot,iplot
import plotly_express as px
import pandas as pd
import numpy as np


class plot_time_v_sent:
	def __init__(self,tweet_df,name):
		assert len(name)>0, "empty string"

		self.tweet_df = tweet_df
		self.name = name
		self.this_person = self.tweet_df[self.name]
		self.this_person['yr-month'] = pd.to_datetime((self.this_person['Date Created'])).dt.strftime('%Y-%b %A')
		self.subjectivity = self.this_person['Subjectivity']
		self.polarity = self.this_person['Polarity']
		self.favorite = self.this_person['Favorites']
		self.retweets = self.this_person['Retweets']
		self.friend_count = self.this_person['Friend Count']
		self.length = max(self.this_person.index)
		self.daily = self.this_person.groupby('yr-month')
		self.avg_df = pd.DataFrame()
		self.plot_df = pd.DataFrame()

	def __repr__(self):
		pass

	def calc_daily_avgs(self):
		'''
			Creates a new dataframe with daily mean values for polarity and subjectivity of tweets
			dataframe consists of: Daily Polarity Avg, Daily Subjectivity Avg, and date in yr-month Day of week format
		'''
		self.avg_df = pd.DataFrame(pd.Series(self.daily['Polarity'].mean(),name="Daily Polarity Avg"))
		self.avg_df['Daily Subjectivity Avg'] = self.daily['Subjectivity'].mean()

		self.this_person['Engagement'] = ((2*self.this_person['Retweets'] + self.this_person['Favorites'])**2)/10000
		self.avg_df['yr-month'] = self.avg_df.index

	def bubble_chart(self):
		self.calc_daily_avgs()

		#finds locations of max engagement
		max_locs = self.this_person.groupby('Date Created')['Engagement'].idxmax()

		#new dataframe created for use with plotly express
		self.plot_df = pd.DataFrame(pd.Series(self.this_person.loc[max_locs]['Date Created'],name="Date"))
		self.plot_df['Retweets'] = self.this_person.loc[max_locs]['Retweets']
		self.plot_df['Favorites'] = self.this_person.loc[max_locs]['Favorites']
		self.plot_df['Engagement'] = self.this_person.loc[max_locs]['Engagement']
		self.plot_df['Polarity'] = self.this_person.loc[max_locs]['Polarity']
		self.plot_df['Tweet'] = self.this_person.loc[max_locs]['Tweet']
		
		#attempting to fix hovertext width by reformatting tweet
		formatted = []
		for tweet in self.this_person['Tweet']:
			temp = self.f(tweet,6)
			formatted.append(temp)
		self.this_person['Formatted Tweet'] = pd.DataFrame(formatted)
		self.plot_df['Formatted Tweet'] = self.this_person.loc[max_locs]['Formatted Tweet']
		#plots the day's max
		p = px.scatter(self.plot_df,x="Date", y="Polarity",
					size='Engagement',size_max=80,hover_data=["Formatted Tweet","Retweets","Favorites"],
					opacity=.6,title=self.name+' Outreach vs. Polarity')
		plot(p)

		#plots all tweets
		#p2 = px.scatter(self.this_person,x="Date Created",y="Polarity",
						size="Engagement",size_max=80,hover_data=["Formatted Tweet","Retweets","Favorites"],
						opacity=.6,title=self.name+' Outreach vs. Polarity')
		#plot(p2)


			# [temp.append('<b>'.join(tweet_hold[i:i+n])) for i in range(0,len(tweet_hold),n)]

		# plot_df['Formatted Tweet'] = pd.DataFrame(temp)

		# trace = go.Scatter(x=self.this_person.loc[max_locs]['Date Created'],
		# 		y=self.this_person.loc[max_locs]['Polarity'],mode='markers',
		# 		text=self.this_person['Tweet'],hoverinfo='y+text',
		# 		marker=dict(size=(self.this_person.loc[max_locs]['Engagement'])**2,opacity=.4,sizemode='area',sizemin=7))
		# layout=dict(title=self.name,hovermode='closest',
		# 			xaxis=dict(title='Date of tweet',ticklen=5,zeroline=False),
		# 			yaxis = dict(title = 'Polarity', ticklen = 5, zeroline = False),showlegend = False)
		# fig=go.Figure(data=[trace],layout=layout)
		# plot(fig)

	def plot_now(self):
		self.calc_daily_avgs()

		#AVG DAILY SUBJ VS TIME & AVG DAILY POLARITY VS TIME
		# fig=plt.figure(1)
		# ax = fig.add_subplot(111)
		# x = self.avg_df['yr-month']
		# ax.bar(x,self.avg_df['Daily Subjectivity Avg'])
		# ax.bar(x,self.avg_df['Daily Polarity Avg'])
		# #ax.set_ylim([min(self.this_person['Polarity']),max(self.this_person['Polarity'])])

		# fig2=plt.figure(2)
		# ax1 = fig2.add_subplot(111)
		# t = self.this_person['Date Created']
		# ax1.scatter(t,self.favorite)
		# ax1.scatter(t,self.retweets)

		# plt.show()

		# plt.close()

		#POLARITY VS SUBJ
		fig=plt.figure()
		cm=plt.cm.get_cmap('gist_heat')
		ax=fig.add_subplot(111)
		x=self.this_person['Polarity']
		y=self.this_person['Subjectivity']
		s=ax.scatter(x,y,c=x,cmap=cm)
		fig.colorbar(s)
		ax.set_xlabel('Polarity')
		ax.set_ylabel('Subjectivity')
		ax.set_title('Polarity vs. Subjectivity')
		#ax.scatter(x,self.retweets)
		#ax.scatter(x,self.favorite)

		plt.show()

#Attempting to fix hovertext; you won't need to use this
	def f(self,string,n):
		split=string.split()
		i=1
		result = ''
		while (i * n) < len(split):
			result = result +' '.join(split[(i-1)*n:i *n]) + '<br>'
			i+=1
		result +=' '.join(split[(i-1)*n:])

		return result

#to load tweet_df so we don't have to rescrape every time
if __name__ == '__main__':


	tweet_df=dict()

	with open('twitter_handles.txt') as f:
		polit_list = f.read().rstrip('\n').split('\n')
	for i in polit_list:
		tweet_df[i] = pd.read_csv(i + '_tweets.csv')
