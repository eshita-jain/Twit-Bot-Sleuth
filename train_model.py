
#Reading data set in csv format with Pandas library.
# The read data is stored in a data frame called df.
import pandas as pd
df = pd.read_csv("datasets/bots_in_twitter.csv", lineterminator='\n')


# Machine learning algorithms work with categorical or continuous numerical variables.
# We can use 10 features in our dataset for machine learning.
# We extract the relevant columns from the data set we read above.
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

# Then we need to convert categorical expressions such as true or false
# to numeric expressions. We complete the conversion process with the
# labelEncoder class of the sklearn machine learning library.
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()

df['default_profile'] = label_encoder.fit_transform(df['default_profile'])
df['default_profile_image'] = label_encoder.fit_transform(df['default_profile_image'])
df['geo_enabled'] = label_encoder.fit_transform(df['geo_enabled'])
df['verified'] = label_encoder.fit_transform(df['verified'])
df['account_type'] = label_encoder.fit_transform(df['account_type'])


# Separation of data for testing and training
from sklearn.model_selection import train_test_split
labels = df["account_type"]
features = df.drop(columns=['account_type'])
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.20, random_state=42)


# Training of machine learning algorithm
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_train, y_train)

# Calculation of f1 score
predicted = clf.predict(X_test)
from sklearn.metrics import f1_score
print(f1_score(y_test, predicted))

# The trained machine learning model is saved to disk for use in the interface
import pickle
file = open('pickle_variables/machine_learning_model.pickle', 'wb')
pickle.dump(clf, file)
file.close()