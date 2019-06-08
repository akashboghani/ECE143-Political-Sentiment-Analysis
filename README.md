# Group 9: Political Sentiment Analysis on Twitter

## Team Members
* Akash Boghani - aboghani@ucsd.edu
* Khushboo Agrawal - khagrawa@ucsd.edu
* Lina Yi - lkyi@ucsd.edu
* Haoran Wu - haw004@ucsd.edu

## Objective
Twitter is the modern battleground of politics. This project aims to perform sentiment analysis on the tweets of popular politicians, and find interesting correlations based on:
* Their tweeting habits
* Their stance on major issues
* Their support base 

## Requirements
In order to run the code in this repository, you will need to install the following dependencies:
* tweepy:
`pip install tweepy`
* pandas:
`pip install pandas`
* numpy:
`pip install numpy`
* textblob: 
`pip install textblob`
* vader:
`pip install vaderSentiment`
* wordcloud:
`pip install wordcloud`
* matplotlib
`pip install matplotlib`
* plotly
`pip install plotly`
* plotly-express
`pip install plotly-express`
* statistics
`pip install statistics`
* sklearn
`pip install sklearn`

## File Structure

#### _Presentation_
* **Twitter Sentiment Analysis.pdf**
This is the final presentation converted to pdf format for your reference.

#### _Demo_
* **Code_Demo.ipynb**
This Jupyter notebook contains the demo. To run, clone the repository. Then, navigate to the repository in Terminal, and type `jupyter notebook`. Click on **Code_demo.ipynb** to run the demo.

#### _Data Collection_
* **collect_data.py**
This python code file fetches the tweets given the twitter handle of the politician and stores in a csv file.

#### _Data Processing_
* **process_tweets.py**
This python code file is used to process the tweets from the csv file by cleaning the data and adding the subjectivity and polarity.

#### _Data Visualization_
* **pie_scatter.py**
This python file contains the functions to plot: 
    * Scatterplot of the average polarity and subjectivity of the tweets of the politicians. 
    * The K-Nearest Neighbors plot for finding out the boundary between the republicans and democrats. 
    * Functions to plot the pie charts of percentage polarity for each politicians.

* **gen_wordcloud.py**
This python file contains the functions to generate the word cloud for positive and negative polarity of the tweets of politicians.

* **engagement_plot.py**
This python file contains functions for plotting the engagement vs polarity bubble chart for each politician.

* **average_tweets.py**
This python file contains functions for plotting the average tweets per day of the politicians

* **christchurch_shooting.py**
This python file contains functions for plotting the comparison of the sentiment polarity of tweets with the average tweets during the christchurch shooting. 

#### _Logistics and Data_
* **twitter_credentials.json**
This python file contains the configuration of the twitter developer  app for extracting the tweets. 

* **all_handles.txt**
This text file contains all the twitter handles of the politicians for which we have extracted the data and analyzed.

* **real_names.txt**
This text file contains the name of the politician real name and their twitter handle

* **data/ folder**
The folder contains all the csv files of the politicians containing the tweets and other attributes