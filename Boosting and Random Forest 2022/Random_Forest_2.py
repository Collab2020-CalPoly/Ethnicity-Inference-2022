import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline

#Used for k-nearest neighbors classifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

#Used for random forest classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV

#Used for k-means clustering
from sklearn.cluster import KMeans

ethnicolr_df = pd.read_csv(r"ethnicolr_function_pred_fl_reg_name_five_cat.csv")
ethnicolr_df = ethnicolr_df.drop(columns=['Unnamed: 0','rowindex', 'asian_std', 'asian_lb', 'asian_ub', 'hispanic_std','hispanic_lb','hispanic_ub', 'nh_black_std','nh_black_lb', 'nh_black_ub','nh_white_std','nh_white_lb','nh_white_ub', 'other_std','other_lb','other_ub']).dropna()

ethnicolr_df = ethnicolr_df.rename(columns={"asian_mean":"name_pred_asian","hispanic_mean":"name_pred_hispanic", "nh_black_mean":"name_pred_black","nh_white_mean":"name_pred_white","other_mean":"name_pred_other", "race":"true_race"})

face_pred_df = pd.read_csv(r"Ethnicity_Inferences2.csv")

face_pred_df = face_pred_df.rename(columns={"First Name":"first","Last Name":"last","White":"face_pred_white", "Black":"face_pred_black","Asian":"face_pred_asian", "Other":"face_pred_other", "Highest Prob. Score":"final_face_pred"})

merged_df = ethnicolr_df.merge(face_pred_df, how = 'inner', on = ['last', 'first'])
merged_df = merged_df.dropna()

merged_df["final_face_pred"] = merged_df["final_face_pred"].map({
    "Asian":"asian",
    "Other":"other",
    "White":"white",
    "Black":"black"
})
merged_df["true_race"] = merged_df["true_race"].map({
    "asian":"asian",
    "other":"other",
    "nh_white":"white",
    "nh_black":"black",
    "hispanic":"other"
})
merged_df["name_pred_other"] = merged_df["name_pred_other"] + merged_df["name_pred_hispanic"]
merged_df = merged_df.drop(columns={"name_pred_hispanic"})

y_fin = merged_df[["true_race"]]
y_train = y_fin[0:100]
X_train_cat = merged_df.drop(columns={"true_race", "first", "last", "__name"})
X_fin = pd.get_dummies(X_train_cat, columns={"final_face_pred"})

X_train_quant = X_fin[0:100]
X_train_quant = X_train_quant.reset_index().drop(columns={'index'})

X_test = X_fin[100:]
X_test = X_test.reset_index().drop(columns={'index'})

# define a pipeline that scales the values in the dataframe before running the model with n = sqrt(len(dataframe))
pipeline = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=10)
)

# fit the pipeline (using X_train and y_train defined above)
pipeline.fit(X_train_quant, y_train)

X_test_predictions = pd.DataFrame()
X_test_predictions['k-NN predictions'] = pipeline.predict(X_test).tolist()

res_df = pd.DataFrame(pipeline.predict_proba(X_test).tolist())
res_df = res_df.rename(columns = {0:'asian', 1:'black', 2:'other', 3:'white'})

#dictionary of all of our possible hyperparameter values
random_grid = {'bootstrap': [True, False],
 'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None], #performance indicator
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]} # performance indicator

#create the random forest classifier model and run it through randomized search CV package to get the best possible model
rf_model = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator = rf_model, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)

#fit our training and target datasets to the given model
rf_random.fit(X_train_quant, y_train)
#display best parameters
rf_random.best_params_

# run the model on the test observation
rf_res_list = rf_random.predict(X_test)
X_test_predictions["random forest predictions"] = rf_res_list

# four clusters because we only have 4 classifications
kmeans_model = KMeans(n_clusters=4)
#fit just the training dataset to the model, clustering is intuitive
kmeans_model.fit(X_train_quant)

#get cluster centroids by getting the values for the cluster centers
centroids = kmeans_model.cluster_centers_
#the list of all training data points labeled by cluster (1-4)
clusters = kmeans_model.labels_

clusters = pd.Series(clusters).map({
    0: "r", #other
    1: "b", #white
    2: "y", #black
    3: "g"  #asian
})

X_train_quant.plot.scatter(x="name_pred_black", y="face_pred_black", 
                     c=clusters, marker="x", alpha=.5)

X_train_quant.plot.scatter(x="name_pred_white", y="face_pred_white", 
                     c=clusters, marker="x", alpha=.5)

X_train_quant.plot.scatter(x="name_pred_other", y="face_pred_other", 
                     c=clusters, marker="x", alpha=.5)

kmeans_res_quant = kmeans_model.predict(X_test)
kmeans_res_cat = pd.Series(kmeans_res_quant).map({
    0: "other", #other
    1: "white", #white
    2: "black", #black
    3: "asian"  #asian
})
X_test_predictions['kmeans predictions'] = kmeans_res_cat
X_test_predictions