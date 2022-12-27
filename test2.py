import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dense, Dropout

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

# Define the model
model = Sequential()
model.add(Dense(256, input_dim=X_train.shape[1], activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, epochs=200, batch_size=32)

# Evaluate the model
_, accuracy = model.evaluate(X_test, y_test)
print('Accuracy: %.2f' % (accuracy*100))


