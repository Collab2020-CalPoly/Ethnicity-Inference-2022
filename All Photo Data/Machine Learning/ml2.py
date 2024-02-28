import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def generate_dataset():
     # FACE DATAFRAME
    df = pd.read_csv("CombinedDataset.csv")
    df = df.drop(columns=['First Name', 'Last Name'])


    # Map "Highest Prob. Score" to numerical values
    score_mapping = {'White': 0, 'Black': 1, 'Asian': 2, 'Other': 3}
    df['Face'] = df['Face'].map(score_mapping)
    df['Name'] = df['Name'].map(score_mapping)
    df['Truth'] = df['Truth'].map(score_mapping)
    df = df.dropna()


    X = df.drop(columns=['Truth'])
    y = df['Truth']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test



def train_model(X_train, X_test, y_train, y_test):

    #RANDOM FOREST
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy for the combined data: {accuracy}")
    joblib.dump(model, 'combined_model.pkl')


def test_model():
    df = pd.read_csv("CombinedDataset.csv")
    df = df.drop(columns=['First Name', 'Last Name'])


    # Map "Highest Prob. Score" to numerical values
    score_mapping = {'White': 0, 'Black': 1, 'Asian': 2, 'Other': 3}
    df['Face'] = df['Face'].map(score_mapping)
    df['Name'] = df['Name'].map(score_mapping)
    df['Truth'] = df['Truth'].map(score_mapping)
    df = df.dropna()


    X = df.drop(columns=['Truth'])
    y = df['Truth']

    model = joblib.load('combined_model.pkl')
    
    # Make predictions on the test data
    y_pred = model.predict(X)

    # Evaluate the model
    accuracy = accuracy_score(y, y_pred)

    print(f"Accuracy for the combined data: {accuracy}")




def main():
    # X_train, X_test, y_train, y_test = generate_dataset()
    # train_model(X_train, X_test, y_train, y_test)

    test_model()








if __name__ == "__main__":
    main()
    