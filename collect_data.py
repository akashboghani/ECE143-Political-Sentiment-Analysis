import tweepy
import json
import csv

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
new_tweets = api.user_timeline(screen_name=twitter_handle, count=200, tweet_mode='extended')
while(len(new_tweets) > 0):
    all_tweets.extend(new_tweets)
    last_id = all_tweets[-1].id - 1
    new_tweets = api.user_timeline(screen_name=twitter_handle, count=200, max_id=last_id, tweet_mode='extended')
    print("######## %d tweets downloaded ########" % len(all_tweets))


outtweets = [[  tweet.id_str, tweet.created_at, tweet.full_text, tweet.favorite_count, tweet.retweet_count, 
                tweet.lang, tweet.user.id_str, tweet.user.name, tweet.user.screen_name, 
                tweet.user.followers_count, tweet.user.friends_count, tweet.user.location, 
                tweet.user.verified ] for tweet in all_tweets]

# writing to the csv file

with open(twitter_handle + '_tweets.csv', 'w', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(['Tweet ID', 'Date Created', 'Tweet','Favorite Count' ,'Retweets', 'Language', 'User ID', 
                    'User Name', 'User Twitter Handle', 'Follower Count', 'Friend Count',
                    'Location', 'Verified'])
    writer.writerows(outtweets)
