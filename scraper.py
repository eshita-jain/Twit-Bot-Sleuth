import snscrape.modules.twitter as sntwitter

"""
In this file, the data that the snscrape library does not give us directly is calculated.

5 data cannot be obtained directly by the sns library.These data are:
    - default_profile
    - default_profile_image
    - geo_enabled
    - account_age_days
    - average_tweets_per_day

There is also a function called get_user_data to make it easier to use for the rest of the program. 
This function allows us to obtain the profile data of the user. If there is no user, it returns None.
"""

# The get_user_data function allows us to get the username and tweeter information.
# This function returns us a user object.
# Get user data, returns None value when if there aren't any user.
def get_user_data(username):
    try:
        profile = sntwitter.TwitterUserScraper(username)
        results = profile.get_items()
    except:
        return None

    null_user = True
    item = None
    try:
        for item_ in results:
            item = item_
            null_user = False
            break
    except:
        null_user = False

    if null_user:
        return None
    return item.user

# In the program, query can also be made with the tweet url. The get_user_from_tweet function takes a url.
# Split this url by the "/" character to get the id of the tweet. With this id,
# information about the tweet is obtained. The user_name property is obtained from the tweet object.
def get_user_from_tweet(url=""):
    url = url.split("/")[-1]
    tweet = sntwitter.TwitterTweetScraper(url)
    username = ""
    try:
        for i in tweet.get_items():
            username = i.username

    except:
        pass

    return get_user_data(username)


# Check customization on profile, user object must be sns user class.
def default_profile(user):
    # Default Banner Photo Links
    default_banner_photos = ["https://abs.twimg.com/images/themes/theme1/bg.png",
                             "https://abs.twimg.com/images/themes/theme14/bg.gif",
                             None]

    if user.profileBannerUrl in default_banner_photos:
        return 0
    else:
        return 1


# Check customization on profile photo, user object must be sns user class.
def default_profile_image(user):
    # Default Profile Photo Links
    default_profile_photos = ["https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
                              None]

    if user.profileImageUrl in default_profile_photos:
        return 0
    else:
        return 1


# Check location information
def geo_enabled(user):
    if user.location == "":
        return 0
    return 1


# Calculates how many days the account has been active.
def account_age_days(user):
    from datetime import date

    sign_date = user.created.date()
    now = date.today()
    days = (now - sign_date).days
    return days


# Calculates the average number of tweets the account sends per day.
def average_tweets_per_day(user):
    tweets_count = user.statusesCount
    account_age = account_age_days(user)
    return tweets_count / account_age


# Transform verified data from True/False to 1/0
def verified(user):
    if user.verified:
        return 1
    return 0




