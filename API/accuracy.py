import csv

def calculate_accuracy(csv_file):
    correct_predictions = 0
    total_predictions = 0

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Name'] == row['Actual']:
                correct_predictions += 1
            total_predictions += 1

    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy

csv_file = 'modelResultsLabeled.csv'  # Replace 'your_csv_file.csv' with the path to your CSV file
accuracy = calculate_accuracy(csv_file)
print("Accuracy: {:.2f}%".format(accuracy))