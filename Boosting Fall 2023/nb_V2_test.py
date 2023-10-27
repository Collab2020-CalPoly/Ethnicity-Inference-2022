from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd

#df = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Boosting Fall 2023\CombinedDataset.csv")
df = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Boosting Fall 2023\ImDB.csv")
# Sample training data (replace this with your own data)
enc = OrdinalEncoder()
X, y = enc.fit_transform(df[['Face', 'Name']]), df['Truth']
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a CountVectorizer to convert text data into numerical features
#vectorizer = CountVectorizer()
#X_train = vectorizer.fit_transform(X_train)
#X_test = vectorizer.transform(X_test)

# Create a Multinomial Naive Bayes classifier
clf = CategoricalNB()

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Calculate accuracy and print the classification report
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=['White', 'Black', 'Asian', 'Other'])

print("Accuracy: {:.2f}%".format(accuracy * 100))
print("-------------------------------------------")
print(report)
print("-------------------------------------------")
print(cm)