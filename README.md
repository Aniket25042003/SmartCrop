# Crop Recommendation System

A customizable and transparent crop-recommendation system that provides personalized crop recommendations based on environmental factors. The system allows users to input various environmental data and customize the weight of each feature to fine-tune the recommendations. The backend uses a machine learning model to generate the top 3 crop recommendations and provides a detailed explanation of how the model arrived at its conclusion using SHAP values, OCR, and LLaMA 3.2.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: React + Vite (JavaScript, HTML, CSS)
- **Machine Learning**: Pre-trained crop recommendation model (scikit-learn)
- **Model Explainability**: SHAP (SHapley Additive exPlanations)
- **OCR**: Tesseract OCR (for extracting explanations from SHAP plots)
- **Language Model**: LLaMA 3.2 - 1B Instruct (for generating model explanations)

## How It Works

1. **User Input**: The user can input the following 7 features:
   - **Nitrogen (N)**
   - **Phosphorous (P)**
   - **Potassium (K)**
   - **Rainfall**
   - **Temperature**
   - **pH**
   - **Humidity**

2. **Feature Weight Customization**: The user can customize the weight of each feature on a scale from 1 to 5 to prioritize the factors that are most important to them.

3. **Crop Recommendations**: Based on the input values and feature weights, the backend uses a **Random Forest Classifier** model to calculate and recommend the top 3 crops for the user.

4. **Model Explanation**: Users can click on the **Model Explanation** button to see how the model arrived at its recommendation:
   - The backend generates a SHAP plot, which highlights how each feature contributed to the recommendation.
   - This SHAP plot is passed through **Tesseract OCR** to extract the textual explanation.
   - The extracted explanation is then fed into **LLaMA 3.2 - 1B Instruct** to generate a natural language explanation that describes the model’s decision-making process.

## Features

- **Customizable Weights**: Users can assign weights to each environmental feature to influence crop recommendations.
- **Top 3 Recommendations**: The system provides the top 3 crop recommendations based on the input data and feature weights.
- **Model Explainability**: Using SHAP, Tesseract OCR, and LLaMA 3.2, users receive a detailed explanation of how the model made its prediction.
- **Interactive Dashboard**: The React-based frontend provides a user-friendly interface to input data, view recommendations, and see the model explanation.

## Setup & Running the Application

### Backend Setup

1. Navigate to the `backend` directory:

```bash
cd crop-app/backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask backend:
```bash
python3 app.py
```
The backend will run on ```http://127.0.0.1:5000``` by default.

### Fronted Setup
1. Navigate to the ```crop-app``` directory:
```bash
cd crop-app
```

2. Install Node.js dependencies:
```bash
npm install
```

4. Run the fronted using Vite:
```bash
npm run dev
```

The fronted will be accessible at ```http://localhost:3000```

### Machine Learning Model
The machine learning model is a Random Forest Classifier trained on the provided dataset and saved as ```crop.pkl```. It is used by the Flask backend for making predictions based on user inputs.

## Key Components
### Backend (Flask)
- **app.py**: Main entry point for the backend API.
- **crop_model.py**: Contains the Random Forest Classifier model for crop prediction.
- **shap.py**: Implements SHAP for explaining model predictions.
- **llm.py**: Contains logic for interacting with the LLaMA 3.2 language model for generating natural language explanations.
- **crop.pkl**: The trained Random Forest model file used by the backend for prediction.

### Fronted (React+Vite)
- **Dashboard.jsx**: Displays the crop recommendations and user data.
- **ModelExplanation.jsx**: Provides a detailed explanation of how the model works and its predictions.
- **Home.jsx**: The landing page where users input their data and customize feature weights.
- **Help.jsx**: Provides additional guidance and instructions for users.
- **Header.jsx**: The navigation header component.

### License
This project is licensed under the MIT License

### Acknowledgments
- Thanks to **Vite** for providing a fast and modern build tool for the React frontend.
- **SHAP** for providing model explainability in a simple and interpretable format.
- **Flask** for being a lightweight framework for the backend API.
- **Tesseract OCR** for text extraction from SHAP plots.
- **LLaMA** for providing natural language explanations using the LLaMA 3.2 - 1B Instruct model.
- **Random Forest Classifier** for being the model used to generate crop recommendations.
- We would like to extend our gratitude to **Nebius** for providing access to the LLaMA model through their API, which was instrumental in generating the model explanations for this project.
- 
### Contributors
- **Aniket Patel** (Discord: patelaniket12)
- **Watermelon** (Discord: melonwaterbottle)
