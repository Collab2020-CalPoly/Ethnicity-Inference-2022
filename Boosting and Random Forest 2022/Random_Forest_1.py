import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import category_encoders as ce

def main():
    f_n_combined_data = pd.read_csv(r'Combined Dataset.csv', header = 0)

    x_c = f_n_combined_data.drop(['Actual'], axis = 1) #featured values/categories for face and name
    y_c = f_n_combined_data['Actual'] #target variable for race

    X_c_train, X_c_test, y_c_train, y_c_test = train_test_split(x_c, y_c, train_size = 0.5, random_state=42) # Alex's combined dataset, test size represents proportion of our test size, random state is the particular seed being tested
    
    # changes classfiers to numerical codes that represent headers{}
    combined_encoder = ce.OrdinalEncoder(cols=['First Name', 'Last Name', 'Face', 'Name'])
    X_c_train = combined_encoder.fit_transform(X_c_train)
    X_c_test = combined_encoder.transform(X_c_test)

    rf_combined = RandomForestClassifier(n_estimators=200, random_state=42) #n_estimators == number of trees tested
    rf_combined.fit(X_c_train, y_c_train) #builds a forest of trees from training set
    y_c_pred = rf_combined.predict(X_c_test) # voting by trees in the forest weighted by probability estimates (predicted class is the one with highest mean probabilty)
    print('Combined model accuracy score: {0:0.4f}'. format(accuracy_score(y_c_test, y_c_pred)))

    #prints confusion matrix for combined dataset
    cm = confusion_matrix(y_c_test,y_c_pred)
    
    print(classification_report(y_c_test, y_c_pred))
    print('Confusion matrix:\n', cm)

    
def test_individ_trees():
    face_data = pd.read_csv(r'Ethnicity_Inferences2.csv', header = 0) #import given face data set
    name_data = pd.read_csv(r'ethnicolr_function_pred_wiki_name.csv', header = 0) #import given name data set

    x_f = face_data.drop(['Highest Prob. Score'], axis = 1) #want all other categories (i.e white, black, east asian, other) except target variable
    y_f = face_data['Highest Prob. Score'] #target variable for face data set
    x_n = name_data.drop(['race'], axis = 1) 
    y_n = name_data['race'] #target variable for name data set

    X_f_train, X_f_test, y_f_train, y_f_test = train_test_split(x_f, y_f, test_size = 0.2, random_state=1) #face, test size represents proportion of our test size, random state is the particular seed being tested
    X_n_train, X_n_test, y_n_train, y_n_test = train_test_split(x_n, y_n, test_size = 0.2, random_state=1) #name, test size represents proportion of our test size, random state is the particular seed being tested

    # changes face classfiers to numerical codes that represent headers
    face_encoder = ce.OrdinalEncoder(cols=['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other'])
    X_f_train = face_encoder.fit_transform(X_f_train)
    X_f_test = face_encoder.transform(X_f_test)

    # changes name classfiers to numerical codes that represent headers
    name_encoder = ce.OrdinalEncoder(cols=['last', 'first', 'Asian_mean', 'Black_mean', 'White_mean', 'Other_mean'])
    X_n_train = name_encoder.fit_transform(X_n_train)
    X_n_test = name_encoder.transform(X_n_test)

    rf_face = RandomForestClassifier(n_estimators=200, random_state=42) #n_estimators == number of trees tested
    rf_face.fit(X_f_train, y_f_train) #builds a forest of trees from training set
    y_f_pred = rf_face.predict(X_f_test) # voting by trees in the forest weighted by probability estimates (predicted class is the one with highest mean probabilty)

    rf_name = RandomForestClassifier(n_estimators=200, random_state=42)
    rf_name.fit(X_n_train, y_n_train)
    y_n_pred = rf_name.predict(X_n_test)

    print('Face model accuracy score with decision-trees : {0:0.4f}'. format(accuracy_score(y_f_test, y_f_pred)))
    print('Name model accuracy score with decision-trees : {0:0.4f}'. format(accuracy_score(y_n_test, y_n_pred)))

    #prints confusion matrices of name and face 
    cm_n = confusion_matrix(y_n_test,y_n_pred)
    cm_f = confusion_matrix(y_f_test,y_f_pred)
    print('Confusion matrix for name:\n', cm_n) 
    print('Confusion matrix for face:\n', cm_f)
    # print(classification_report(y_f_test, y_f_pred)) #uncomment next two lines to give a more in-depth evaluation of both face and name 
    # print(classification_report(y_n_test, y_n_pred))

    # Categories being tested: Black, East Asian, Other, White 
    

if __name__ == "__main__":
    main()
    #test_individ_trees()

#  For confusion matrix: 
#  Values on the diagonal represent the number (or percent, in a normalized confusion matrix) of times where the predicted label matches the true label. 
#  Values in the other cells represent instances where the classifier mislabeled an observation; 
#  the column tells us what the classifier predicted, and the row tells us what the right label was.
# 
#  For classification report:
#  The recall means "how many of this class you find over the whole number of element of this class"
#  The precision will be "how many are correctly classified among that class"
#  The f1-score (used to compare the performance of two classifiers) is the harmonic mean (generally used if data values are ratios of two variables with different measures) 
#  between precision & recall
#  The support is the number of occurence of the given class in your dataset 

#  Note: The reason why I used both metrics is because on its own, a classification report tells us generally what kind of errors the model made, 
#  but it doesn’t give us specifics. The confusion matrix tells us exactly where mistakes were made, but it doesn’t give us summary metrics like precision, 
#  recall, or F1 score. Using both gives a much better understanding of the output and allows us to evaluate the overall performance of the algorithm.
