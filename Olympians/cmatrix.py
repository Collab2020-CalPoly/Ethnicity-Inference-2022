import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

############################
#Generates Confusion Matrix#
############################



# Read the first CSV file for true labels
with open('/Users/ethan/Desktop/Research/Olympians/Olympians_Actual.csv', 'r') as file:
    reader = csv.DictReader(file)
    true_labels = [row['Actual'] for row in reader]

# Read the second CSV file for predicted labels
with open('/Users/ethan/Desktop/Research/Olympians/Olympian_Inferences.csv', 'r') as file:
    reader = csv.DictReader(file)
    predicted_labels = [row['Highest Prob. Score'] for row in reader]

# Define the classes
classes = ["White", "Black", "Asian", "Other"]

# Create an empty confusion matrix
conf_matrix = np.zeros((len(classes), len(classes)), dtype=int)

# Populate the confusion matrix
for true, pred in zip(true_labels, predicted_labels):
    true_idx = classes.index(true)
    pred_idx = classes.index(pred)
    conf_matrix[true_idx][pred_idx] += 1

# Visualize the confusion matrix
sns.heatmap(conf_matrix, annot=True, fmt="d", xticklabels=classes, yticklabels=classes)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()
