import joblib
model = joblib.load('./Model/combined_model.pkl')


def predict(name, face):
    score_mapping = {'White': 0, 'Black': 1, 'Asian': 2, 'Other': 3}
    face = score_mapping[face]
    name = score_mapping[name]
    prediction = model.predict([[name, face]])
    

    # invert the mapping
    reverse_mapping = {0: 'White', 1: 'Black', 2: 'Asian', 3: 'Other'}
    return reverse_mapping[prediction[0]]




    
