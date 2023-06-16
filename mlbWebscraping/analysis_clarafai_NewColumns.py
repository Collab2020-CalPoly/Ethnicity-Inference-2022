import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def analysis_of(csv_file):
    data = pd.read_csv(csv_file, encoding='ISO-8859-1')

    # true and predicted labels
    true_labels = data['Ground_Truth']
    predicted_labels = data['Prediction']

    # label names for confusion matrix
    label_names = ['White', 'Black', 'East Asian', 'Southeast Asian', 'Indian', 'Middle Eastern', 'Latino_Hispanic']

    # confusion matrix, true_labels = x, predicted_labels = y
    cm = confusion_matrix(true_labels, predicted_labels, labels=label_names)

    # Filter the data to only include rows where the "Prediction" matches the "Truth"
    matches = data[data['Prediction'] == data['Ground_Truth']]
    pairs = data.groupby(['Prediction', 'Ground_Truth']).size().reset_index(name='count')

    # Return the number of matches and print the confusion matrix
    print(f"{len(matches)}/1347 players matched")
    print(cm)
    print(pairs)
    
    # Create a visually appealing confusion matrix using pyplot and seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', xticklabels=label_names, yticklabels=label_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()
    
    return len(matches)

count = analysis_of("C:\MAVACResearchMugizi\Winter2023\mlbWebscraping\clarafai_new_cols.csv")

print(f"{count}/1347 players matched, or {count/1347:.2%}")
