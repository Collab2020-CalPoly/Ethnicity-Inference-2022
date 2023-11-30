# Fall 2023: Applied Voting Classifier
# Bill Chan
#

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import category_encoders as ce

def main():
    f_n_combined_data = pd.read_csv("C:\CalPolyAcademics\Ethnicity-Inference-2022\Boosting Fall 2023\CombinedDataset.csv")

    x_c = f_n_combined_data.drop(['Truth'], axis=1)
    y_c = f_n_combined_data['Truth']

    X_c_train, X_c_test, y_c_train, y_c_test = train_test_split(x_c, y_c, train_size=0.5, random_state=42)

    combined_encoder = ce.OrdinalEncoder(cols=['First Name', 'Last Name', 'Face', 'Name'])
    X_c_train = combined_encoder.fit_transform(X_c_train)
    X_c_test = combined_encoder.transform(X_c_test)

    # Create individual classifiers
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    # lr_classifier = LogisticRegression(max_iter=1000, random_state=42)
    ab_classifier = AdaBoostClassifier(n_estimators=100, random_state=42)
    gb_classifier = GradientBoostingClassifier(n_estimators=100, random_state=42)


    # Fit and print information for Random Forest Classifier
    rf_classifier.fit(X_c_train, y_c_train)
    rf_accuracy = rf_classifier.score(X_c_test, y_c_test)
    print(f'Random Forest Classifier accuracy score: {rf_accuracy:.4f}')

    # Fit and print information for AdaBoost Classifier
    ab_classifier.fit(X_c_train, y_c_train)
    ab_accuracy = ab_classifier.score(X_c_test, y_c_test)
    print(f'AdaBoost Classifier accuracy score: {ab_accuracy:.4f}')

    # Fit and print information for Gradient Boosting Classifier
    gb_classifier.fit(X_c_train, y_c_train)
    gb_accuracy = gb_classifier.score(X_c_test, y_c_test)
    print(f'Gradient Boosting Classifier accuracy score: {gb_accuracy:.4f}')
    
    # Create a Voting Classifier that combines the individual classifiers
    hard_voting_classifier = VotingClassifier(
        estimators=[
            ('rf', rf_classifier),
            # ('lr', lr_classifier),
            ('adaboost', ab_classifier),
            ('gradientboost', gb_classifier)
        ],
        voting='hard'  # Use 'hard' voting for classification
    )

    # Fit the Voting Classifier to the training data
    hard_voting_classifier.fit(X_c_train, y_c_train)

    # Make predictions using the Voting Classifier
    y_c_pred = hard_voting_classifier.predict(X_c_test)

    # Calculate and print accuracy, confusion matrix, and classification report
    accuracy = accuracy_score(y_c_test, y_c_pred)
    cm = confusion_matrix(y_c_test, y_c_pred)
    report = classification_report(y_c_test, y_c_pred)

    print(f'Voting Classifier accuracy score: {accuracy:.4f}')
    print('Confusion matrix:\n', cm)
    print(report)

if __name__ == "__main__":
    main()
