import numpy as np
from sklearn.preprocessing import StandardScaler

def recommend_crops(model, features):
    scaler = StandardScaler()
    
    # Ensure the features are in the correct shape (2D array with one sample)
    features_array = np.array(features).reshape(1, -1)  # Reshape to 2D (1 row, n columns)
    
    # Fit the scaler and then transform
    scaler.fit(features_array)  # Fit the scaler using the features
    sample_data_scaled = scaler.transform(features_array)  # Now apply transform
    
    # Use `predict_proba` to get probabilities for all classes
    probabilities = model.predict_proba(sample_data_scaled)[0]
    
    # Get the indices of the top 3 highest probabilities
    top_3_indices = probabilities.argsort()[-3:][::-1]
    
    # Get the corresponding crop names and probabilities
    top_3_crops = []
    for idx in top_3_indices:
        crop_name = model.classes_[idx]  # Get the crop name (class)
        crop_prob = probabilities[idx]  # Get the probability for that crop
        top_3_crops.append({
            'name': crop_name,
            'probability': crop_prob,
            'description': f"Best crop based on input parameters: {crop_name}.",
            'imgUrl': f"{crop_name.lower()}.jpg",  # Assumes image filenames match crop names
        })
    
    return top_3_crops
