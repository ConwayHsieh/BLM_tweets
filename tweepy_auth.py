import tweepy

def tweepy_auth():

	key_file = open('key.txt')

	consumer_key = key_file.readline().rstrip('\n')
	consumer_secret = key_file.readline().rstrip('\n')

	auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

	return auth
	