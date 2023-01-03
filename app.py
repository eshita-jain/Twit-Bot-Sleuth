from flask import Flask, render_template, request
import numpy
import pickle
import pandas as pd
from scraper import *
from fuctions import *
app = Flask(__name__)

file = open("model/model.pickle", "rb")
clf = pickle.load(file)

bot_avg = get_bot_avg_statistic()

@app.route('/', methods=['GET', 'POST'])
def home_page():  # Home Page
    data = {
        "user_name": "",
        "is_valid_user": "",
        "user": "",
        "url":"",
        "bot_user_avg": bot_avg
    }

    if request.method == "POST":
        if request.form.get("action") == "check":
            user = None
            # Works when querying with tweet url
            if request.form.get("url") != "":
                user = get_user_from_tweet(request.form.get("url"))
                data["url"] = request.form.get("url")

            # Works when querying with username
            elif request.form.get("username") != "":
                user_name = request.form.get("username")
                data["user_name"] = user_name
                user = get_user_data(user_name)

            # Username and tweet may have been entered incorrectly and no users were found.
            # The is_valid_user flag is sent to the frontend to warn the user.
            data["user"] = user
            if user is None:
                data["is_valid_user"] = False
            else:
                data["is_valid_user"] = True

                # If the user is found correctly, the necessary features are obtained
                # for the machine learning algorithm to work.
                features = [
                    default_profile(user),
                    default_profile_image(user),
                    user.favouritesCount,
                    user.followersCount,
                    user.friendsCount,
                    geo_enabled(user),
                    verified(user),
                    average_tweets_per_day(user),
                    account_age_days(user)
                ]

                # feature names for data frame generation
                feature_names = ["default_profile",
                                "default_profile_image",
                                "favourites_count",
                                "followers_count",
                                "friends_count",
                                "geo_enabled",
                                "verified",
                                "average_tweets_per_day",
                                "account_age_days"]
                feature_df = pd.DataFrame([features], columns=feature_names)

                # User's attribute information converted from pandas
                # df to dictionary to be sent to frontend.
                data["features"] = feature_df.to_dict('records')[0]

                # Machine learning prediction was performed with the attribute information of the user.
                proba = clf.predict_proba(feature_df)

                # Data between 0 and 1 converted to percentage
                data["proba"] = round(proba[0][0]*100)

                # value rounded to 3 decimal places for UI
                data["features"]["average_tweets_per_day"] = round(data["features"]["average_tweets_per_day"], 3)

                # The colors that should appear on the front face were calculated according to
                # the user's bot percentage.
                data["border"] = get_border(data["proba"])

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
