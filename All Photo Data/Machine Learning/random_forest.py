# Import necessary libraries
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample dataset, you should replace this with your actual data
# X1 and X2 represent the predictions from API1 and API2.
X1 = np.random.rand(100, 1)  # Replace with actual API1 predictions
X2 = np.random.rand(100, 1)  # Replace with actual API2 predictions

# Sample ground truth labels
y = np.random.randint(0, 2, size=100)  # Replace with actual labels

# Combine API1 and API2 predictions as features
X_combined = np.hstack((X1, X2))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Create a Random Forest classifier
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the Random Forest model
random_forest.fit(X_train, y_train)

# Make predictions using the ensemble model
y_pred = random_forest.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
