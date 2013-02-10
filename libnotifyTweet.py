# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

import notify2
import json
import ConfigParser
import os

class LibNotifyListener(StreamListener):
    def on_data(self, data):
        dat = json.loads(data)
        if "text" in dat:
            # Seems to be a tweet
            notify2.Notification(dat["user"]["screen_name"], dat["text"], dat["user"]["profile_image_url"]).show()
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == "__main__":
    cfg = ConfigParser.RawConfigParser()
    cfg.read(os.path.expanduser("~/.libnotifyTweet.cfg"))

    notify2.init(cfg.get("libnotifyTweet", "appname"))
    l = LibNotifyListener()
    auth = OAuthHandler(cfg.get("libnotifyTweet", "consumer_key"), cfg.get("libnotifyTweet", "consumer_secret"))
    auth.set_access_token(cfg.get("libnotifyTweet", "access_token"), cfg.get("libnotifyTweet", "access_token_secret"))

    stream = Stream(auth, l)
    stream.userstream()
