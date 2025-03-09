from flask import Flask, jsonify, request, send_from_directory, g
from flask_cors import CORS
from model import recommend_crops
from shap import generate_feature_importance_plot  # Import the new function
from llm import get_explanation_from_llm  # Import the function to interact with LLM
import joblib  # Assuming you're using joblib to load your model
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for frontend-backend communication

# Load the model once when the app starts
model = joblib.load("crop.pkl")  # Adjust the model loading according to your format

@app.route('/')
def home():
    return "Backend is running!"

CROP_DESCRIPTIONS = {
    "rice": "Rice is a staple food crop grown in warm climates with high humidity.",
    "maize": "Maize, also known as corn, is a versatile crop used for food and fodder.",
    "jute": "Jute is a fiber crop used for making ropes, bags, and textiles.",
    "cotton": "Cotton is a soft fiber crop used in textiles and fabrics.",
    "coconut": "Coconut trees provide nutritious fruit, oil, and fiber-rich husks.",
    "papaya": "Papaya is a tropical fruit rich in vitamins and digestive enzymes.",
    "orange": "Oranges are citrus fruits known for their high vitamin C content.",
    "apple": "Apples are widely grown temperate fruits, known for their crisp texture.",
    "muskmelon": "Muskmelon is a sweet, juicy fruit grown in warm climates.",
    "watermelon": "Watermelon is a hydrating summer fruit rich in antioxidants.",
    "grapes": "Grapes are small, juicy fruits used in winemaking and fresh consumption.",
    "mango": "Mangoes are tropical fruits loved for their sweet and tangy taste.",
    "banana": "Bananas are energy-rich fruits with high potassium content.",
    "pomegranate": "Pomegranates are nutritious fruits with edible seeds packed with antioxidants.",
    "lentil": "Lentils are protein-rich legumes widely consumed in various cuisines.",
    "blackgram": "Black gram is a legume commonly used in Indian cuisine.",
    "mungbean": "Mung beans are nutritious legumes used in soups, curries, and sprouts.",
    "mothbeans": "Moth beans are drought-resistant legumes rich in protein.",
    "pigeonpeas": "Pigeon peas are protein-rich legumes used in various cuisines.",
    "kidneybeans": "Kidney beans are high-protein legumes used in diverse dishes.",
    "chickpea": "Chickpeas are protein-packed legumes, a key ingredient in hummus.",
    "coffee": "Coffee plants produce beans used for brewing aromatic beverages."
}

@app.route("/api/recommend", methods=["POST"])
def recommend_crop():
    data = request.json  # Receive input from frontend

    try:
        N = float(data.get("N"))
        P = float(data.get("P"))
        K = float(data.get("K"))
        temperature = float(data.get("temperature"))
        humidity = float(data.get("humidity"))
        ph = float(data.get("ph"))
        rainfall = float(data.get("rainfall"))
        
        # Get weights
        weights = data.get("weights", {})
        weightN = float(weights.get("N", 1))
        weightP = float(weights.get("P", 1))
        weightK = float(weights.get("K", 1))
        weightTemperature = float(weights.get("temperature", 1))
        weightHumidity = float(weights.get("humidity", 1))
        weightPh = float(weights.get("ph", 1))
        weightRainfall = float(weights.get("rainfall", 1))

    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input data format: {str(e)}"}), 400

    # Apply weights to features
    features = [
        N * weightN,
        P * weightP,
        K * weightK,
        temperature * weightTemperature,
        humidity * weightHumidity,
        ph * weightPh,
        rainfall * weightRainfall,
    ]
    
    top_3_crops = recommend_crops(model, features)
    
    # Update this part to include the correct descriptions
    top_3_crops_with_descriptions = [
        {
            "name": crop['name'],
            "description": CROP_DESCRIPTIONS.get(crop['name'], "No description available.")
        }
        for crop in top_3_crops if isinstance(crop, dict)
    ]

    g.top_3_crops = top_3_crops
    # Ensure the "static" directory exists
    file_path = "static/top_3_crops.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Overwrite the file each time the model is called
    with open(file_path, "w") as file:
        crops_text = "\n".join([f"{crop['name']}: {crop['description']}" for crop in top_3_crops_with_descriptions])
        file.write(crops_text)

    feature_importance_plot_url = generate_feature_importance_plot(model, ["N", "P", "K", "Temperature", "Humidity", "pH", "Rainfall"])

    return jsonify({
        "top_3_crops": top_3_crops_with_descriptions,  # Return crops with descriptions
        "featureImportancePlotUrl": feature_importance_plot_url,
        "cropsFileUrl": "/static/top_3_crops.txt"
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename, as_attachment=False)

@app.route('/api/shap', methods=['GET'])
def shap_explanation():
    return jsonify({
        "explanation": "SHAP (Shapley Additive Explanations) helps us understand the contribution of each feature to the model's predictions.",
        "shapPlotUrl": "static/feature_importance_plot.png"  # Path to the saved feature importance plot
    })

@app.route('/api/model-explanation', methods=['GET'])
def model_explanation():
    return jsonify({
        "explanation": "This model predicts the most suitable crops based on environmental factors like soil type, humidity, and sunlight."
    })

@app.route('/api/llm-explanation', methods=['POST'])
def llm_explanation():
    # Receive the SHAP plot image URL or the file path from the frontend
    data = request.json
    image_path = data.get("imagePath")  # Example: "static/feature_importance_plot.png"
    
    if not image_path:
        return jsonify({"error": "Image path is required"}), 400

    # Optionally, we can also send the recommended result to the LLM (if needed)
    top_3_crops = g.get('top_3_crops', [])
    recommended_result = "Crop recommendation not provided"
    if top_3_crops:
        recommended_result = "\n".join([f"{crop['name']}: {crop['description']}" for crop in top_3_crops])

    # Get the detailed explanation from the LLM using the SHAP plot and recommended result
    explanation = get_explanation_from_llm(image_path, recommended_result)

    return jsonify({
        "explanation": explanation
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)