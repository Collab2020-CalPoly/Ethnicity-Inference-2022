import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers


# FACE DATAFRAME
df = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/All Photo Data/Machine Learning/Combined_Face_Inferences.csv")

df = df.drop(columns=['First Name', 'Last Name'])

# Convert the remaining columns to numerical data
df[['White', 'Black', 'Asian', 'Other']] = df[['White', 'Black', 'Asian', 'Other']].apply(pd.to_numeric)

# Map "Highest Prob. Score" to numerical values
score_mapping = {'White': 0, 'Black': 1, 'Asian': 2, 'Other': 3}
df['Highest Prob. Score'] = df['Highest Prob. Score'].map(score_mapping)

#drop highest prob.score
#df.drop('Highest Prob. Score', axis=1, inplace=True)




#NAME DATAFRAME
df2 = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/All Photo Data/Machine Learning/Combined_Name_Inferences.csv")

df2 = df2.drop(columns=['First Name', 'Last Name'])


# Map "Highest Prob. Score" to numerical values


df2['Highest Prob. Score'] = df2['Highest Prob. Score'].map(score_mapping)




# Concatenate the two DataFrames
combined_df = pd.concat([df, df2], axis=1)
combined_df.dropna(inplace=True)    
print(combined_df)


#TRUTH DATAFRAME
df3 = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/All Photo Data/Machine Learning/Combined_Truth.csv")
df3 = df3.drop(columns=['First Name', 'Last Name','Image'])
df3['Truth'] = df3['Truth'].map(score_mapping) #map actual to numbers


df3 = df3.loc[combined_df.index]


X = combined_df
y = df3
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



#RANDOM FOREST
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy for the combined data: {accuracy}")




# test on unrelated dataset
def test_model():
    #TEST NAME DATAFRAME
    df4 = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/Olympians/Old Olympians/2022_Olympian_Face_Inferences.csv")
    df4 = df4.drop(columns=['First Name', 'Last Name'])
    # Convert the remaining columns to numerical data
    df4[['White', 'Black', 'Asian', 'Other']] = df4[['White', 'Black', 'Asian', 'Other']].apply(pd.to_numeric)
    df4['Highest Prob. Score'] = df4['Highest Prob. Score'].map(score_mapping)

    #TEST FACE DATAFRAME
    df5 = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/Olympians/Old Olympians/2022_Olympian_Name_Inferences.csv")
    df5 = df5.drop(columns=['First Name', 'Last Name'])
    df5['Race'] = df5['Race'].map(score_mapping)
    df5['Alt'] = df5['Alt'].map(score_mapping)

    combined_test_df = pd.concat([df4, df5], axis=1)

    print(combined_test_df)

    #TRUTH TEST DATAFRAME
    df6 = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/Olympians/Old Olympians/2022_Olympians_Actual.csv")
    df6 = df6.drop(columns=['First Name', 'Last Name'])
    df6['Actual'] = df6['Actual'].map(score_mapping) #map actual to numbers

    y_pred = model.predict(combined_test_df)
    accuracy = accuracy_score(df6, y_pred)

    print(f"Accuracy for the combined data: {accuracy}")


