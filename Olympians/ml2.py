import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier




# FACE DATAFRAME
df = pd.read_csv("Olympians.csv")

df = df.drop(columns=['First Name', 'Last Name'])

# Convert the remaining columns to numerical data

# Map "Highest Prob. Score" to numerical values
score_mapping = {'White': 0, 'Black': 1, 'Asian': 2, 'Other': 3}
df['Face'] = df['Face'].map(score_mapping)
df['Name'] = df['Name'].map(score_mapping)
df['Truth'] = df['Truth'].map(score_mapping)




#NAME DATAFRAME


df2 = df.drop(columns = ['Truth'])


X = df2
y = df['Truth']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)





base_estimator = DecisionTreeClassifier() 

# Initialize the AdaBoost classifier
adaboost_classifier = AdaBoostClassifier(
    base_estimator=base_estimator,
    n_estimators=50,  
    learning_rate=1.0  
)

# Train the AdaBoost classifier on the training data
adaboost_classifier.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = adaboost_classifier.predict(X_test)

# Evaluate the performance of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)






    

