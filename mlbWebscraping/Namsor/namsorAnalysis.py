import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def analysis_of(csv_file):
    data = pd.read_csv(csv_file, encoding='ISO-8859-1')

    # Map the values in the 'raceEthnicity' column to the corresponding categories
    mapping = {
        'W_NL': 'White',
        'B_NL': 'Black',
        'A': 'Asian',
        'HL': 'Other'
    }

    data['Prediction'] = data['raceEthnicity'].map(mapping)

    # true and predicted labels
    true_labels = data['Ground_Truth']
    predicted_labels = data['Prediction']

    # label names for confusion matrix
    label_names = ['White', 'Black', 'Asian', 'Other']

    # confusion matrix, true_labels = x, predicted_labels = y
    cm = confusion_matrix(true_labels, predicted_labels, labels=label_names)

    # Calculate the total number of individuals per race
    race_counts = data['Ground_Truth'].value_counts()
    print("Total individuals per race:")
    print(race_counts)

    # Calculate accuracy and precision per race
    accuracy_per_race = cm.diagonal() / cm.sum(axis=1)
    precision_per_race = cm.diagonal() / cm.sum(axis=0)

    # Print accuracy and precision per race
    print("Accuracy per race:")
    print(accuracy_per_race)
    print("Precision per race:")
    print(precision_per_race)

    # Filter the data to only include rows where the "Prediction" matches the "Ground_Truth"
    matches = data[data['Prediction'] == data['Ground_Truth']]
    pairs = data.groupby(['Prediction', 'Ground_Truth']).size().reset_index(name='count')

    # Return the number of matches
    print(f"{len(matches)}/610 players matched")
    print(pairs)

    # Create a visually appealing confusion matrix using pyplot and seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', xticklabels=label_names, yticklabels=label_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Namsor MLB Analysis Confusion Matrix')
    plt.show()

    return len(matches)

count = analysis_of("C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/Namsor/namsorOutput_withTruth.csv")

print(f"{count}/610 players matched, or {count/610:.2%}")
