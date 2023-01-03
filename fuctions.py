"""
Users may wonder why they are classified as bots.
We want to provide users with the opportunity to compare the average values of bot
accounts with their own values.
"""
def get_bot_avg_statistic():
    import pandas as pd
    df = pd.read_csv("datasets/bots_in_twitter.csv", lineterminator='\n')

    df = df[["default_profile",
             "default_profile_image",
             "favourites_count",
             "followers_count",
             "friends_count",
             "geo_enabled",
             "verified",
             "average_tweets_per_day",
             "account_age_days",
             "account_type"]]

    from sklearn import preprocessing
    label_encoder = preprocessing.LabelEncoder()

    df['default_profile'] = label_encoder.fit_transform(df['default_profile'])
    df['default_profile_image'] = label_encoder.fit_transform(df['default_profile_image'])
    df['geo_enabled'] = label_encoder.fit_transform(df['geo_enabled'])
    df['verified'] = label_encoder.fit_transform(df['verified'])
    df['account_type'] = label_encoder.fit_transform(df['account_type'])

    result = df.groupby(by="account_type", dropna=False).mean()
    result = result.iloc[0]

    result["default_profile"] = round(result["default_profile"])
    result["default_profile_image"] = round(result["default_profile_image"])
    result["geo_enabled"] = round(result["geo_enabled"])
    result["verified"] = round(result["verified"])
    result["favourites_count"] = int(round(result["favourites_count"]))
    result["followers_count"] = int(round(result["followers_count"]))
    result["friends_count"] = int(round(result["friends_count"]))
    result["average_tweets_per_day"] = int(round(result["average_tweets_per_day"]))
    result["account_age_days"] = int(round(result["account_age_days"]))

    return result

# The place where the distribution of bootstrap color codes according to the bot ratio
# in order to avoid complexity in the interface.
def get_border(proba):
    if proba <= 30:
        return "primary"
    elif proba <= 60:
        return "warning"
    else:
        return "danger"



