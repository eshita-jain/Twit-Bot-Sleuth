import pickle

import pandas as pd

file = open("pickle_variables/machine_learning_model.pickle", "rb")
clf = pickle.load(file)

from scraper import *
username = "bakgelsin"
user_data = get_user_data(username)


column_names = ["default_profile",
                "default_profile_image",
                "favourites_count",
                "followers_count",
                "friends_count",
                "geo_enabled",
                "verified",
                "average_tweets_per_day",
                "account_age_days"]

features = [
    default_profile(user_data),
    default_profile_image(user_data),
    user_data.favouritesCount,
    user_data.followersCount,
    user_data.friendsCount,
    geo_enabled(user_data),
    verified(user_data),
    average_tweets_per_day(user_data),
    account_age_days(user_data)
]

data = pd.DataFrame([features], columns=column_names)
proba = clf.predict_proba(data)
print(proba)