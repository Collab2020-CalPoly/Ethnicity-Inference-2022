from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd

# Load your dataset and split it into training and testing sets
enc = OrdinalEncoder() # Transforms categorical features ("White", "Black", etc.) into numerical data
df = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Boosting Fall 2023\CombinedDataset.csv")
X, y = enc.fit_transform(df[['Face', 'Name']]), df['Truth']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the base estimator (e.g., Decision Tree)
base_estimator = DecisionTreeClassifier() # max_depth most likely around 100000000

# Initialize the AdaBoost classifier
adaboost_classifier = AdaBoostClassifier(
    base_estimator=base_estimator,
    n_estimators=50,  # Number of weak classifiers (adjust as needed)
    learning_rate=1.0  # Learning rate (adjust as needed)
)

# Train the AdaBoost classifier on the training data
adaboost_classifier.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = adaboost_classifier.predict(X_test)

# Evaluate the performance of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
