import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Reading data set in csv format with Pandas library.
# The read data is stored in a data frame called df.
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
label_encoder = preprocessing.LabelEncoder()

df['default_profile'] = label_encoder.fit_transform(df['default_profile'])
df['default_profile_image'] = label_encoder.fit_transform(df['default_profile_image'])
df['geo_enabled'] = label_encoder.fit_transform(df['geo_enabled'])
df['verified'] = label_encoder.fit_transform(df['verified'])
df['account_type'] = label_encoder.fit_transform(df['account_type'])

# Separation of data for testing and training
labels = df["account_type"]
features = df.drop(columns=['account_type'])
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.20, random_state=42)

# Define the decision tree classifier with pre-pruning
clf = DecisionTreeClassifier(max_depth=15)

# Train the classifier
clf.fit(X_train, y_train)

# Evaluate the classifier
score = clf.score(X_test, y_test)
print(f"Accuracy: {score*100:.2f}%")

# Save the trained model to disk

