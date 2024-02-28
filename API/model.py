import joblib
model = joblib.load('./Model/combined_model.pkl')


# Input: Name: ['White', 'Black', 'Asian', 'Other'], Face: ['White', 'Black', 'Asian', 'Other']
# Output: ['White', 'Black', 'Asian', 'Other']
def predict(face, name):
    score_mapping = {'White': 0, 'Black': 1, 'Asian': 2, 'Other': 3}
    face = score_mapping[face]
    name = score_mapping[name]
    prediction = model.predict([[face, name]])
    

    # invert the mapping
    reverse_mapping = {0: 'White', 1: 'Black', 2: 'Asian', 3: 'Other'}
    return reverse_mapping[prediction[0]]






    
