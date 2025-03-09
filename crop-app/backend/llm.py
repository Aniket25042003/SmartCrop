import pytesseract
from PIL import Image
import requests
from shap import generate_feature_importance_plot

# Path to the Tesseract executable (for your system)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# The URL of the Nebius AI Studio endpoint for the Llama model
LLM_API_URL = "https://api.studio.nebius.ai/v1/chat/completions"

# Replace with your actual API key or authentication method
API_KEY = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnaXRodWJ8OTQxNTUyNDEiLCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyIsImlzcyI6ImFwaV9rZXlfaXNzdWVyIiwiYXVkIjpbImh0dHBzOi8vbmViaXVzLWluZmVyZW5jZS5ldS5hdXRoMC5jb20vYXBpL3YyLyJdLCJleHAiOjE4OTkwNzIzNjksInV1aWQiOiJiYzY4NDI0Zi04YTA5LTRhZWUtOTkzZC03NTBiODhiMGU4NGYiLCJuYW1lIjoiY3JvcC1yZWNvbW1lbmRhdGlvbiIsImV4cGlyZXNfYXQiOiIyMDMwLTAzLTA3VDAwOjA2OjA5KzAwMDAifQ.PtDjmeFbVTBUgyrilTs1t_aLswBgCuCwPu1bDg_It_4"

def extract_features_from_shap_plot(image_path):
    """
    Extract feature names and their importances from the SHAP plot image using OCR.
    Assumes that the SHAP plot contains feature names and corresponding importances.
    """
    # Open the image using Pillow
    img = Image.open(image_path)

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img)

    # Process the extracted text to find features and importances
    feature_importance_data = []
    
    # Example format assumption: "Feature1: 0.25, Feature2: 0.15, ..."
    lines = text.split("\n")
    for line in lines:
        # Try to match lines with a feature name and its corresponding importance
        parts = line.split(":")
        if len(parts) == 2:
            feature = parts[0].strip()
            try:
                importance = float(parts[1].strip())
                feature_importance_data.append((feature, importance))
            except ValueError:
                continue  # Ignore lines where importance is not a valid float

    return feature_importance_data

def get_explanation_from_llm(image_path, recommended_result):
    features_and_importances = extract_features_from_shap_plot(image_path)
    feature_details = "\n".join([f"{feature}: {importance}" for feature, importance in features_and_importances])
    
    # Ensure at least three crops are included
    top_crops = recommended_result

    prompt = f"""
    You are an AI that explains how features contribute to the results of a model's prediction.

    The following are the features in the dataset:
    - N: Nitrogen content in the soil
    - P: Phosphorus content in the soil
    - K: Potassium content in the soil
    - ph: pH level of the soil
    - Humidity: Moisture present in the air
    - Rainfall: Amount of rainfall received
    - Temperature: Atmospheric temperature

    For each feature, provide the following details:
    - **Feature Name**: [Feature]
    - **Description**: Explain what this feature represents and why it is important in the context of crop recommendations.
    - **Importance Level**: High/Medium/Low (based on SHAP values)

    After detailing each feature, provide an overall summary of the model's recommendations based on the feature importance, highlighting which features are most influential across all predictions.

    Finally, include a description of how the model was trained:
    - **Model Description**: Explain the training process, including the algorithm used, the dataset characteristics, and any relevant parameters.

    Ensure the response is clear, concise, and easy to understand. Do not use any special styling, bold, italics, or other formatting other than plain text.
    Each new sentence should start on a new line for better readability.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.2-1B-Instruct",  # Update to use the correct model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }

    response = requests.post(LLM_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        explanation = response_data.get("choices", [])[0].get("message", {}).get("content", "")
        return explanation
    else:
        return f"Error: {response.status_code} - {response.text}"
