import tweepy
import json

with open('twitter_credentials.json') as cred_data:
    login_info = json.load(cred_data)
consumer_key = login_info['CONSUMER_KEY']
consumer_secret = login_info['CONSUMER_SECRET']
access_key = login_info['ACCESS_KEY']
access_secret = login_info['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

all_tweets = []
twitter_handle = input("Enter twitter handle of user:")
new_tweets = api.user_timeline(screen_name=twitter_handle, count=200)
while(len(new_tweets) > 0):
    all_tweets.extend(new_tweets)
    last_id = all_tweets[-1].id - 1
    new_tweets = api.user_timeline(screen_name=twitter_handle, count=200, max_id=last_id)
    print("######## %d tweets downloaded ########" % len(all_tweets))

