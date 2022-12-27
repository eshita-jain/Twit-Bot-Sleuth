# Reading data set in csv format with Pandas library.
# The read data is stored in a data frame called df.
import pandas as pd
from sklearn.metrics import f1_score
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

# Training of machine learning algorithms
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

classifiers = {
    "Random Forest": RandomForestClassifier(n_estimators=10),
    "AdaBoost": AdaBoostClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    # "SVM": SVC(kernel="linear"),
    "NuSVC": NuSVC(nu=0.1, kernel="rbf", degree=3, gamma="scale"),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "Gaussian Naive Bayes": GaussianNB(),
    "Multinomial Naive Bayes": MultinomialNB(),
    "Bernoulli Naive Bayes": BernoulliNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SGD": SGDClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Multi-layer Perceptron": MLPClassifier(alpha=1, max_iter=1000)
}

for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    predicted = clf.predict(X_test)
    f1 = f1_score(y_test, predicted)
    print(f"F1 score for {name}: {f1}")
