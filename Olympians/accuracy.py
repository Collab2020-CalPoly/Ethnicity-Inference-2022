import csv
import pandas as pd
from IPython.display import display

#####################################
#Generates Prediction vs Truth Table#
#####################################


# Read truth labels in from csv file
with open('/Users/ethan/Desktop/Research/Olympians/Olympians_Actual.csv', 'r') as file:
    reader = csv.DictReader(file)
    true_labels = [row['Actual'] for row in reader]

# Read the second CSV file for predicted labels
with open('/Users/ethan/Desktop/Research/Olympians/Olympian_Inferences.csv', 'r') as file:
    reader = csv.DictReader(file)
    predicted_labels = [row['Highest Prob. Score'] for row in reader]


#create dictionary for pred and ground truth values
d = {}
correct = 0
size = 0


#Add to dict with count
for i in range(len(true_labels)):
    if (predicted_labels[i],true_labels[i]) in d:
        d[(predicted_labels[i],true_labels[i])] +=1 
    else:
        d[(predicted_labels[i],true_labels[i])] =1 
    

    #Accuracy Counting
    if(predicted_labels[i] == true_labels[i]):
        correct+=1
    size+=1


# generate data for dataframe
data = []
for key,val in d.items():
    data.append([key[0], key[1], val]) 
df = pd.DataFrame(data, columns=['Prediction', 'Truth', 'Count'])

#Printing out truth vs pred value table
display(df)
print('accuracy:' , str((correct/size)*100)[:5]+'%')