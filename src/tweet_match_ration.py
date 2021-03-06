# check the match ratio between two tweets


from flask import Flask, render_template
import tweepy, time, sys
from time import sleep
from random import randint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
from flask import jsonify
from flask import request
import os
import io
import json
from pprint import pprint
import pickle
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__, template_folder="mytemplate")
@app.route("/")
def hello():
    return "Hello World!"


list_names = ["@fakeNewsBots"]
list2 = []
##load from database
# try:
#     with open('data.pkl', 'rb') as f:
#         l = pickle.load(f)
#         list2 = l
#
# except KeyError:
#     pass

try:
    t_consumerkey = 'TW_CONSUMERKEY'
    t_secretkey = 'TW_SECRETKEY'
    access_tokenkey = 'TW_ACCESS_TOKENKEY'
    access_tokensecret = 'TW_TOKENSECRET'
except KeyError:
    print(
    "You need to set the environment variables: TW_CONSUMERKEY, TW_SECRETKEY, TW_ACCESS_TOKENKEY, TW_TOKENSECRET")
    sys.exit(1)
auth = tweepy.OAuthHandler(t_consumerkey, t_secretkey)
auth.set_access_token(access_tokenkey, access_tokensecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5,
                 retry_errors=5)


class myStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        re_tweet(status)

    def on_error(self, status_code):
        if status_code == 420:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False
        else:
            print(status_code)
            return False


def re_tweet(tweet):
    #open file to read hashtags
    with open('hashtags.txt') as f:
       for line in f:
            auth = tweepy.OAuthHandler(t_consumerkey, t_secretkey)
            auth.set_access_token(access_tokenkey, access_tokensecret)

            api = tweepy.API(auth)

            search_text = line
            search_number = 2
            search_result = api.search(search_text, rpp=search_number)
            flag = True
            # tweet to compare to
            compare_text = ""

            with io.open('output_tweets.txt', 'w', encoding='utf8') as w:
                for tweet in search_result:

                    if flag:
                        compare_text = tweet.text
                        flag = False
                    else:
                        w.write("Tweet: " + tweet.text + "\n")
                        w.write("test_text: " + compare_text + "\n")
                        w.write(fuzz.ratio(tweet.text, compare_text))

            #         w.write('Username:  ' + tweet.author.screen_name + '\n')
            #         w.write("Tweet:  " + tweet.text + "\n")
            w.close()

# Authentication
myStreamListener = myStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['fake'], async=True)

if(__name__) == '__main__':
    app.run(debug=True)