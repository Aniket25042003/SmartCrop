import requests

# Endpoint for getting recommendations
recommend_url = "http://127.0.0.1:5000/api/recommend"

data = {
    "N": 16,
    "P": 70,
    "K": 20,
    "temperature": 25.0,
    "humidity": 40.0,
    "ph": 4.6,
    "rainfall": 122.0
}

# Make a POST request to get recommendations and feature importance plot URL
response = requests.post(recommend_url, json=data)

print("Response Status Code (Recommendation):", response.status_code)

# Check if the response is successful
if response.status_code == 200:
    response_json = response.json()
    
    # Extract top 3 crops and feature importance plot URL
    top_3_crops = response_json.get("top_3_crops", [])
    feature_importance_plot_url = response_json.get("featureImportancePlotUrl", "")
    
    print("Top 3 Crops:", top_3_crops)
    print("Feature Importance Plot URL:", feature_importance_plot_url)
else:
    print("Error:", response.text)


# Now testing the LLM explanation feature
llm_explanation_url = "http://127.0.0.1:5000/api/llm-explanation"

# Assume the first recommended crop is the one to explain
recommended_result = top_3_crops[0]["name"] if top_3_crops else "Wheat"  # Use 'name' key for crop name

# The path to the SHAP plot image
image_path = "static/feature_importance_plot.png"  # Ensure the plot is generated before this request

# Prepare data for the LLM explanation
llm_data = {
    "imagePath": image_path,
    "recommendedResult": recommended_result
}

# Make a POST request to get the LLM explanation
llm_response = requests.post(llm_explanation_url, json=llm_data)

print("\nResponse Status Code (LLM Explanation):", llm_response.status_code)

# Check if the response is successful
if llm_response.status_code == 200:
    llm_response_json = llm_response.json()
    
    # Extract the explanation from LLM
    explanation = llm_response_json.get("explanation", "")
    
    print("LLM Explanation:", explanation)
else:
    print("Error:", llm_response.text)
